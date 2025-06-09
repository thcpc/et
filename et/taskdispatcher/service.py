import abc

from copy import deepcopy
from math import ceil

from celery import shared_task
from requests import session

from sqlalchemy import and_

from sqlalchemy.orm import Session

from document.service import _label_str, snapshot
from et import enums
from et.enums import Status
from et.models import UserBase
from et.settings import DB, REDIS
from libs.utils import TaskGeneratorFactory
from taskdispatcher.core.task_definition.task_define import TaskDefine
from taskdispatcher.core.task_definition.taskgenerator import TaskGenerator
from taskdispatcher.models import Document, Task, TaskAssignee, SnapshotDocument


class Dispatcher(abc.ABC):
    def __init__(self, task_define: dict):
        self.task_define = TaskDefine(**task_define)

    def execute(self):
        with DB.session(autoflush=False, autobegin=False) as session:
            _session: Session = session
            with _session.begin() as transaction:
                _task_generator = TaskGeneratorFactory(session=_session, task_define=self.task_define)
                if _task_generator.match():
                    _new_task = _task_generator.new_task()
                    self.update_cache_count()

    @abc.abstractmethod
    def update_cache_count(self): ...


class NewDispatcher(Dispatcher):
    @classmethod
    def name(cls): return enums.Name.Dispatcher.New

    def update_cache_count(self):
        REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=self.task_define.new_assign_user_id)


class TransferDispatcher(Dispatcher):
    @classmethod
    def name(cls): return enums.Name.Dispatcher.Transfer

    def update_cache_count(self):
        REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=self.task_define.new_assign_user_id)
        REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=self.task_define.old_assign_user_id, number=-1)


class RollBackDispatcher(Dispatcher):
    @classmethod
    def name(cls): return enums.Name.Dispatcher.Rollback

    def update_cache_count(self):
        REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=self.task_define.new_assign_user_id)
        REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=self.task_define.old_assign_user_id, number=-1)

    def execute(self):
        with DB.session(autoflush=False, autobegin=False) as session:
            _session: Session = session
            with _session.begin() as transaction:
                _task = Task.task(session=session, id=self.task_define.current_task_id)
                if _task.prev_id != Status.TaskNode.Start:
                    _back_task = Task.task(session=session, id=_task.prev_id)
                    _back_task.status = Status.Task.Todo
                    _back_task.comment = self.task_define.comment
                    TaskAssignee.task_assignee(session, task_id=_task.id).is_delete = True
                    _task.is_delete = True
                    self.update_cache_count()


# @shared_task
def dispatcher(operate: dict):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            for Dispatcher_ in [NewDispatcher, TransferDispatcher, RollBackDispatcher]:
                if Dispatcher_.name() == operate.get("op"):
                    Dispatcher_(task_define=operate.get("task_define")).execute()


def get_tasks(user_id, page_no=1, per_count=20):
     with (DB.session(autoflush=True, autobegin=True) as session):
        _session: Session = session
        _total_tasks = REDIS.get_page_total(type_=REDIS.Key.DocTabTask, user_id=user_id)
        if _total_tasks is None:

            _total_tasks = _session.query(Task, TaskAssignee).join(TaskAssignee,
                                                                   and_(TaskAssignee.user_id == user_id,
                                                                        TaskAssignee.task_id == Task.id,
                                                                        TaskAssignee.is_delete == False)).filter(
                and_(Task.status != enums.Status.Task.Finished,
                     Task.status != enums.Status.Task.TransferToOther)
            ).count()
            REDIS.set_page_total(type_=REDIS.Key.DocTabTask, user_id=user_id, count=_total_tasks)
        results = _session.query(Document, Task, TaskAssignee, SnapshotDocument).join(
            Task,
            and_(
                Task.status != enums.Status.Task.Finished,
                Task.status != enums.Status.Task.TransferToOther,
                Task.document_id == Document.id,
                Document.is_delete == False)
        ).join(TaskAssignee,
               and_(
                   TaskAssignee.task_id == Task.id,
                   TaskAssignee.user_id == user_id,
                   TaskAssignee.is_delete == False)).join(
            SnapshotDocument, and_(Task.snapshot_id == SnapshotDocument.id)).limit(
            per_count).offset(
            (page_no - 1) * per_count).all()
        _cache_label = {}
        _cache_id = {}
        _document_list = []
        for document, task, assignee, snapshot in results:
            if _cache_label.get(document.id) is None:
                _document_dict = document.as_dict()
                _document_dict["labels"] = [_label_str(label) for label in
                                            [e for e in document.labels if not e.is_delete]]
                _cache_label[document.id] = _document_dict
            _document = deepcopy(_cache_label.get(document.id))
            _document["task"] = task.as_dict()
            if _cache_id.get(_document["task"]["create_by"]) is None:
                _cache_id[_document["task"]["create_by"]] = _session.query(UserBase).filter_by(
                    id=_document["task"]["create_by"]).first().name
            _document["task"]["create_by"] = _cache_id[_document["task"]["create_by"]]
            _document["assignee"] = assignee.as_dict()
            _document["snapshot"] = snapshot.as_dict()
            _document_list.append(_document)
        return {"documents": _document_list, "totalPage": ceil(_total_tasks / per_count)}


def re_assign(task_id, old_assignee_id, new_assignee_user_id, comment):
    """
    任务转给其它人

    """
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _old_task = Task.task(session, id=task_id)
            _user = UserBase.user(session, id=new_assignee_user_id)
            task_define = TaskGenerator.definition(TaskDefine(document_id=_old_task.document_id,
                                                              create_user_id=old_assignee_id,
                                                              old_assign_user_id=_old_task.assignee.id,
                                                              new_assign_user_id=new_assignee_user_id,
                                                              current_task_id=_old_task.id,
                                                              comment=comment,
                                                              task_type=_old_task.task_type))
            _old_task.status = enums.Status.Task.TransferToOther
            dispatcher_operate = dict(op=enums.Name.Dispatcher.Transfer, task_define=task_define)
            dispatcher(dispatcher_operate)
    return {}


def roll_back(task_id, comment):
    """
    打回任务给上一个处理人
    task_id: 当前任务ID
    判断 当前任务是否有上个任务
    如有
    1. 修改前一个任务的状态为 Status.Task.Todo
    2. 删除当前任务
    3. 删除当前任务的处理人

    """
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        with _session.begin() as transaction:
            task_define = TaskGenerator.definition(TaskDefine(document_id=None,
                                                              create_user_id=None,
                                                              old_assign_user_id=None,
                                                              new_assign_user_id=None,
                                                              current_task_id=task_id,
                                                              comment=comment,
                                                              task_type=None))
            dispatcher_operate = dict(op=enums.Name.Dispatcher.Rollback, task_define=task_define)
            dispatcher(dispatcher_operate)
