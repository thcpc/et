from sqlalchemy.orm import relationship
import et.models as MetaModel


# Create your models here.

class Document(MetaModel.DocumentBase):
    labels = relationship('taskdispatcher.models.DocumentLabel',
                          back_populates='parent_doc')

    snapshots = relationship('taskdispatcher.models.SnapshotDocument',
                             back_populates='base_doc')

    tasks = relationship('taskdispatcher.models.Task',
                         back_populates='parent_doc')


class DocumentLabel(MetaModel.DocumentLabelBase):
    parent_doc = relationship('taskdispatcher.models.Document',
                              back_populates='labels')
    detail = relationship('taskdispatcher.models.Label',
                          back_populates='ref_doc_label', uselist=False, lazy="joined")


class Label(MetaModel.LabelBae):
    parent_cat = relationship('taskdispatcher.models.LabelCategory',
                              back_populates='labels')
    ref_doc_label = relationship('taskdispatcher.models.DocumentLabel',
                                 back_populates='detail')


class LabelCategory(MetaModel.LabelCategoryBase):
    labels = relationship('taskdispatcher.models.Label',
                          back_populates='parent_cat',
                          order_by="et.models.LabelBae.name")


class SnapshotDocument(MetaModel.SnapshotDocumentBase):
    base_doc = relationship('taskdispatcher.models.Document',
                            back_populates='snapshots')


class Task(MetaModel.TaskBase):
    parent_doc = relationship('taskdispatcher.models.Document',
                              back_populates='tasks')
    assignee = relationship('taskdispatcher.models.TaskAssignee',
                            back_populates='task', uselist=False)


class TaskAssignee(MetaModel.TaskAssigneeBase):
    task = relationship('taskdispatcher.models.Task',
                        back_populates='assignee')
