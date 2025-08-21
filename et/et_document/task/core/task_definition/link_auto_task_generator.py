from et import enums
from et.enums import Status
from et_document.task.core.task_definition.taskgenerator import TaskGenerator
# from taskdispatcher.models import Document


class LinkAutoTaskGenerator(TaskGenerator):

    def dispatcher(self, document, assignee):
        return dict(doc_id=document.id, ref_user_id=assignee)

    def match(self) -> bool:
        if self._work_on_doc.status >= Status.Document.Submit:
            for label in self._work_on_doc.labels:
                if label.detail.name == enums.Name.DocumentType.AutoZh:
                    return True
        return False

    @property
    def shortcut_language(self):
        return "请关联自动化用例"

    # @classmethod
    # def name(cls):
    #     return enums.Name.TaskType.LinkAutoTask

    # @classmethod
    # def spec(cls, document_id, assign_user_id, create_user_id, current_task_id) -> dict:
    #     _spec = cls.definition(document_id, assign_user_id, create_user_id, current_task_id)
    #     _spec["spec"] = enums.Name.TaskType.LinkAutoTask
    #
    #     return _spec
