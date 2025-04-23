from collections import namedtuple
from copy import deepcopy
from math import ceil

from celery import shared_task

from sqlalchemy import and_

from sqlalchemy.orm import Session

from document.service import _label_str, snapshot
from et import enums
from et.enums import Status
from et.models import UserBase
from et.settings import DB, REDIS
from libs.utils import TaskClassFactory

from taskdispatcher.models import Document, Task, TaskAssignee, SnapshotDocument
from taskdispatcher.core.task_definition.task import Task as TaskDefine


@shared_task
def dispatcher(task_data: dict):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:

            task = TaskClassFactory(task_type=task_data.get("spec"), data=task_data)
            # _document = _session.query(Document).filter_by(id=task.document_id()).first()
            _document = Document.doc(_session, id=task.document_id())
            _snapshot = _document.snapshots[-1]
            _create_by = UserBase.user(_session, name="System").id if not task.create_by() else task.create_by()
            if task.match(_document):
                _new_task = Task(task_type=task.task_type(),
                                 status=enums.Status.Task.Todo,
                                 snapshot_id=_snapshot.id,
                                 description=task.shortcut_language,
                                 comment=task_data.get("comment", ""),
                                 create_by=_create_by)
                if task_data.get("from_id"):
                    _new_task.prev_id = task_data.get("from_id")
                _user = UserBase.user(_session, id=task.assignee_user_id())
                _assignee = TaskAssignee(user_id=task.assignee_user_id(), name=_user.name)
                _new_task.assignee = _assignee
                _document.tasks.append(_new_task)
                _session.flush()
                if task_data.get("from_id"):
                    _prev = _session.query(Task).filter_by(id=task_data.get("from_id")).first()
                    _prev.next_id = _new_task.id
                    _session.flush()
                REDIS.increment_page_total(type_=REDIS.Key.DocTabTask, user_id=task.assignee_user_id())


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
                   TaskAssignee.user_id == user_id,
                Task.document_id == Document.id,
                Document.is_delete == False)
        ).join(TaskAssignee,
               and_(
                   TaskAssignee.task_id == Task.id,
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
            _old_task = _session.query(Task).filter_by(id=task_id).first()
            _user = _session.query(UserBase).filter_by(id=new_assignee_user_id).first()

            task_spec = TaskDefine.common_spec(document_id=_old_task.document_id,
                                               create_user_id=old_assignee_id,
                                               assign_user_id=new_assignee_user_id,
                                               current_task_id=_old_task.id)
            task_spec["spec"] = _old_task.task_type
            task_spec["comment"] = comment
            _old_task.status = enums.Status.Task.TransferToOther
            dispatcher(task_spec)
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
            _task = _session.query(Task).filter_by(id=task_id).first()
            if _task.prev_id != Status.TaskNode.Start:
                _back_task = _session.query(Task).filter_by(id=_task.prev_id).first()
                _back_task.status = Status.Task.Todo
                _back_task.comment = comment
                _session.query(TaskAssignee).filter_by(task_id=_task.id).first().is_delete = True
                _task.is_delete = True
