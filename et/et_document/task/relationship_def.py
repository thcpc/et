from sqlalchemy.orm import relationship
import et.models as MetaModel


# Create your models here.

class Document(MetaModel.DocumentBase):
    labels = relationship('et_document.task.relationship_def.DocumentLabel',
                          back_populates='parent_doc')

    snapshots = relationship('et_document.task.relationship_def.SnapshotDocument',
                             back_populates='base_doc')

    tasks = relationship('et_document.task.relationship_def.Task',
                         back_populates='parent_doc')


class DocumentLabel(MetaModel.DocumentLabelBase):
    parent_doc = relationship('et_document.task.relationship_def.Document',
                              back_populates='labels')
    detail = relationship('et_document.task.relationship_def.Label',
                          back_populates='ref_doc_label', uselist=False, lazy="joined")


class Label(MetaModel.LabelBae):
    parent_cat = relationship('et_document.task.relationship_def.LabelCategory',
                              back_populates='labels')
    ref_doc_label = relationship('et_document.task.relationship_def.DocumentLabel',
                                 back_populates='detail')


class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('et_document.task.relationship_def.Label',
                          back_populates='parent_cat',
                          order_by="et.models.LabelBae.name")


class SnapshotDocument(MetaModel.SnapshotDocumentBase):
    base_doc = relationship('et_document.task.relationship_def.Document',
                            back_populates='snapshots')


class Task(MetaModel.TaskBase):
    parent_doc = relationship('et_document.task.relationship_def.Document',
                              back_populates='tasks')
    assignee = relationship('et_document.task.relationship_def.TaskAssignee',
                            back_populates='task', uselist=False)


class TaskAssignee(MetaModel.TaskAssigneeBase):
    task = relationship('et_document.task.relationship_def.Task',
                        back_populates='assignee')
