import abc

from sqlalchemy.orm import Session


from et import enums
from et.models import UserBase
from taskdispatcher.core.task_definition.task_define import TaskDefine
from taskdispatcher.models import Task, TaskAssignee,Document


class TaskGenerator(abc.ABC):
    def __init__(self, session: Session, task_define: TaskDefine):
        self._task_define = task_define
        self._session = session
        self._work_on_doc = Document.doc(self._session, id=self.task_define.document_id)

    def new_task(self):
        _task = self.create_task()
        self.create_task_assignee(_task)
        self.create_task_link(_task)

    def create_task(self):
        _snapshot = self._work_on_doc.snapshots[-1]
        _create_by = UserBase.user(self._session,
                                   name="System").id if not self.task_define.create_user_id else self.task_define.create_user_id
        _new_task = Task(task_type=self.task_define.task_type,
                         status=enums.Status.Task.Todo,
                         snapshot_id=_snapshot.id,
                         description=self.shortcut_language(),
                         comment=self.task_define.comment or "",
                         create_by=_create_by)

        self.create_task_assignee(_new_task)
        self._session.flush()
        return _new_task

    def create_task_link(self, task):
        task.prev_id = self.task_define.current_task_id
        _prev = Task.task(self._session, id=self.task_define.current_task_id)
        _prev.next_id = task.id
        self._session.flush()

    def create_task_assignee(self, task):
        _user = UserBase.user(self._session, id=self.task_define.new_assign_user_id)
        _assignee = TaskAssignee(user_id=self.task_define.new_assign_user_id, name=_user.name)
        task.assignee = _assignee
        self._work_on_doc.tasks.append(task)


    @property
    def task_define(self):
        return self._task_define

    @abc.abstractmethod
    def shortcut_language(self) -> str: ...

    @abc.abstractmethod
    def match(self) -> bool:
        ...

    @abc.abstractmethod
    def dispatcher(self, document, assignee):
        ...



    @classmethod
    def definition(cls, task_define: TaskDefine) -> dict:
        return {
            "document_id": task_define.document_id,
            "new_assign_user_id": task_define.new_assign_user_id,
            "create_user_id": task_define.create_user_id,
            "comment": task_define.comment,
            "current_task_id": task_define.current_task_id,
            "old_assign_user_id": task_define.old_assign_user_id,
            "task_type": task_define.task_type
        }

