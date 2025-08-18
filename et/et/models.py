from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import validates

from alchemy.base_model import BaseModel as Base
from et.exceptions.business_error import InValidUserInfoError


class DocumentBase(Base):
    Draft = 0

    __tablename__ = 'et_document_docs'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    author = Column(String(50))
    status = Column(Integer)

    @classmethod
    def doc(cls, session, **kwargs):
        return cls._fetch(session, **kwargs)

class PageBase(Base):
    __tablename__ = 'et_document_pages'
    id = Column(Integer, primary_key=True)
    name = Column(String(1000))
    order = Column(Integer)
    document_id = Column(Integer, ForeignKey('et_document_docs.id'))


class ParagraphBase(Base):
    __tablename__ = 'et_document_paragraphs'
    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    paragraph_type = Column(String(15))
    page_id = Column(Integer, ForeignKey('et_document_pages.id'))
    blockno = Column(String(50))
    fileno = Column(String(50))


class HisContentBase(Base):
    __tablename__ = 'et_document_his_contents'
    id = Column(Integer, primary_key=True)
    blockno = Column(String(50))
    fileno = Column(String(50))
    paragraph_id = Column(Integer, ForeignKey('et_document_paragraphs.id'))


class LabelCategoryBase(Base):
    __tablename__ = 'et_document_label_categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    category_type = Column(String(10))


class LabelBae(Base):
    __tablename__ = 'et_document_labels'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    category_id = Column(Integer, ForeignKey('et_document_label_categories.id'))


class LabelOn(Base):
    __tablename__ = 'et_document_label_on'
    id = Column(Integer, primary_key=True)
    on = Column(String(30))
    on_id = Column(Integer)


class DocumentLabelBase(Base):
    __tablename__ = 'et_document_doc_labels'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('et_document_docs.id'))
    label_id = Column(Integer, ForeignKey('et_document_labels.id'))


class SnapshotDocumentBase(Base):
    __tablename__ = 'et_document_snapshot_docs'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('et_document_docs.id'))
    labels = Column(String(1000))
    description = Column(String(1000), nullable=False)
    name = Column(String(70), nullable=False)


class SnapshotPageBase(Base):
    __tablename__ = 'et_document_snapshot_pages'
    id = Column(Integer, primary_key=True)
    snapshot_document_id = Column(Integer, ForeignKey('et_document_snapshot_docs.id'))
    page_name = Column(String(100))
    order = Column(Integer)


class SnapshotParagraphBase(Base):
    __tablename__ = 'et_document_snapshot_paragraphs'
    id = Column(Integer, primary_key=True)
    snapshot_page_id = Column(Integer, ForeignKey('et_document_snapshot_pages.id'))
    blockno = Column(String(50))
    fileno = Column(String(50))


class UserBase(Base):
    __tablename__ = 'et_admin_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    token = Column(String(200))

    @validates("name", "password")
    def valid_null(self, key, value):
        if value is None or not value.strip():
            raise InValidUserInfoError(message=f'{key} 不能为空', code=InValidUserInfoError.Code)
        return value

    @classmethod
    def user(cls, session, **kwargs):
        return cls._fetch(session, **kwargs)

class UserFingerPrintBase(Base):
    __tablename__ = 'et_admin_user_fingerprints'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('et_admin_users.id'))
    finger_print = Column(String(100))

    @classmethod
    def fingerPrint(cls, session, **kwargs):
        return cls._fetch(session, **kwargs)



class TaskBase(Base):
    __tablename__ = 'et_document_tasks'
    id = Column(Integer, primary_key=True)
    status = Column(Integer)
    business_status = Column(Integer)
    task_type = Column(String(20))
    document_id = Column(Integer, ForeignKey('et_document_docs.id'))
    snapshot_id = Column(Integer)
    create_by = Column(Integer)
    comment = Column(String(500))
    description = Column(String(500))
    prev_id = Column(Integer, default=-1)
    next_id = Column(Integer, default=-1)

    @classmethod
    def task(cls, session, **kwargs):
        return cls._fetch(session, **kwargs)


class TaskAssigneeBase(Base):
    __tablename__ = 'et_document_task_assignees'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('et_document_tasks.id'))
    user_id = Column(Integer)
    name = Column(String(100), nullable=False)

    @classmethod
    def task_assignee(cls, session, **kwargs):
        return cls._fetch(session, **kwargs)


class DocumentAuditBase(Base):
    # " ".join[{action},{action_object},{prepositions},{action_target}] by {who} at {when}
    __tablename__ = 'et_document_doc_audits'
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('et_document_docs.id'))
    when = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    who = Column(String(100))
    action = Column(String(100))
    action_object = Column(String(100))
    prepositions = Column(String(10))
    action_target = Column(String(100))
