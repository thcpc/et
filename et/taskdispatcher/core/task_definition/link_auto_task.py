from et import enums
from et.enums import Status
from taskdispatcher.core.task_definition.task import Task
from taskdispatcher.models import Document


class LinkAutoTask(Task):

    def __init__(self, task_data: dict):
        super().__init__(task_data)

    def dispatcher(self, document, assignee):
        return dict(doc_id=document.id, ref_user_id=assignee)

    def match(self, document: Document) -> bool:
        if document.status >= Status.Document.Submit:
            for label in document.labels:
                if label.detail.name == enums.Name.DocumentType.AutoZh:
                    return True
        return False

    @property
    def shortcut_language(self):
        return "请关联自动化用例"

    @classmethod
    def spec(cls, document_id, assign_user_id, create_user_id, current_task_id) -> dict:
        _spec = cls.common_spec(document_id, assign_user_id, create_user_id, current_task_id)
        _spec["spec"] = enums.Name.TaskType.LinkAutoTask
        return _spec
