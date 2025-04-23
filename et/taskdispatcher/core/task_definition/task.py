import abc

from et import enums


class Task(abc.ABC):
    def __init__(self, task_data: dict):
        self._task_data = task_data

    def task_type(self):
        return self._task_data.get("spec")

    def document_id(self):
        return self._task_data.get("document_id")

    def assignee_user_id(self):
        return self._task_data.get("assign_user_id")

    def create_by(self):
        return self._task_data.get("create_user_id")

    @abc.abstractmethod
    def match(self, document) -> bool: ...

    @abc.abstractmethod
    def dispatcher(self, document, assignee): ...

    @classmethod
    def common_spec(cls, document_id, assign_user_id, create_user_id, current_task_id) -> dict:
        _spec = {
            "document_id": document_id,
            "assign_user_id": assign_user_id,
            "create_user_id": create_user_id
        }
        if current_task_id:
            _spec["from_id"] = current_task_id
        return _spec


