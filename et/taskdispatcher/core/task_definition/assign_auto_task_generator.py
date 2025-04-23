from et import enums
from et.enums import Status
from taskdispatcher.core.task_definition.taskgenerator import TaskGenerator
from taskdispatcher.models import Document


class AssignAutoTaskGenerator(TaskGenerator):

    def dispatcher(self, document, assignee):
        return dict(doc_id=document.id, ref_user_id=assignee)

    def match(self) -> bool:
        if self._work_on_doc.status >= Status.Document.Submit:
            for label in self._work_on_doc.labels:
                if label.detail.name == enums.Name.DocumentType.AutoZh:
                    return True
        return False

    def shortcut_language(self):
        return "请分配人关联自动化用例"
