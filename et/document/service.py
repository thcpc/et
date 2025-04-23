import uuid

from math import ceil

from sqlalchemy import and_
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import Session
from win32con import FILE_SHARE_DELETE

from document.models import HisContent, SnapshotDocument, SnapshotPage, SnapshotParagraph
from document.models import Document
from document.models import Page
from document.models import Paragraph
from document.models import DocumentLabel
from et import settings
from et.enums import Status
from et.settings import DB, REDIS

from libs.file_handle import FileHandle
import logging

# 配置日志记录器（可选，通常会在项目的某个配置文件中设置）
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# 添加一个处理器来将日志输出到控制台（可选）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def _label_str(label):
    if label.detail.parent_cat.category_type == "business":
        return f'#{label.detail.parent_cat.name}#{label.detail.name}'
    else:
        return f'@{label.detail.name}'


def get_all_documents(page_no=1, per_count=20):
    with DB.session() as session:
        _session: Session = session

        total_documents = REDIS.get_page_total(type_=REDIS.Key.DocTabAll, user_id="et_dev")
        if total_documents is None:
            total_documents = _session.query(Document).filter_by(is_delete=False).count()
            REDIS.set_page_total(type_=REDIS.Key.DocTabAll, user_id="et_dev", count=total_documents)
        _documents = _session.query(Document).filter_by(is_delete=False).limit(per_count).offset(
            (page_no - 1) * per_count).all()
        _documents_list = []
        for document in _documents:
            _document_dict = document.as_dict()
            _document_dict["labels"] = [_label_str(label) for label in [e for e in document.labels if not e.is_delete]]
            _documents_list.append(_document_dict)
        return {"documents": _documents_list, "totalPage": ceil(total_documents / per_count)}
        # return [document.as_dict() for document in _session.query(Document).filter_by(is_delete=False).all()]


def get_user_documents(user_name, page_no=1, per_count=20):
    with DB.session() as session:
        _session: Session = session

        total_documents = REDIS.get_page_total(type_=REDIS.Key.DocTabUser, user_id=user_name)
        if total_documents is None:
            total_documents = _session.query(Document).filter(
                and_(Document.is_delete == False, Document.author == user_name)).count()
            REDIS.set_page_total(type_=REDIS.Key.DocTabUser, user_id=user_name, count=total_documents)
        _documents = _session.query(Document).filter(
            and_(Document.is_delete == False, Document.author == user_name)).limit(per_count).offset(
            (page_no - 1) * per_count).all()
        _documents_list = []
        for document in _documents:
            _document_dict = document.as_dict()
            _document_dict["labels"] = [_label_str(label) for label in [e for e in document.labels if not e.is_delete]]
            _documents_list.append(_document_dict)
        return {"documents": _documents_list, "totalPage": ceil(total_documents / per_count)}


def get_task_documents(user_id, status, condition, page_no=1, per_count=20): ...


def get_document(doc_id, include_page=True):
    with DB.session() as session:
        _session: Session = session
        _document = _session.query(Document).filter(and_(Document.id == doc_id, Document.is_delete is not True)).first()
        _document_data = _document.as_dict()
        _document_data["labels"] = [e.label_id for e in _document.labels if not e.is_delete]
        _page_data = [page.as_dict() for page in _document.pages] if include_page else []
        return _document_data, _page_data


def new_document(author, name, labels):
    resp = None
    with DB.session(autoflush=True, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _new_document = Document(name=name, author=author)
            for _name in ["前置条件", "触发页面", "请求接口", "接口验证", "数据库验证"]:
                _new_document.pages.append(Page(name=_name))
            for label in labels:
                _new_document.labels.append(DocumentLabel(label_id=label))
                _new_document.status = Status.Document.Draft

            _session.add(_new_document)
            _session.flush()
            resp = _new_document.as_dict()
    if resp:
        REDIS.increment_page_total(type_=REDIS.Key.DocTabAll, user_id="et_dev")
        REDIS.increment_page_total(type_=REDIS.Key.DocTabUser, user_id=author)

    return resp


def update_document(document_updated: dict):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _document = _session.query(Document).filter(
                and_(Document.id == document_updated.get("id"), Document.is_delete is not True)).first()
            if _document:
                _document.name = document_updated.get("name")

            _update_labels = document_updated.get("labels")
            _old_labels = [e.label_id for e in _document.labels if not e.is_delete]
            _new_labels = list(filter(lambda id_: id_ not in _old_labels, _update_labels))
            _removed_labels = list(filter(lambda id_: id_ not in _update_labels, _old_labels))
            for label_id in _new_labels:
                _document.labels.append(DocumentLabel(document_id=_document.id, label_id=label_id))
            _session.query(DocumentLabel).where(
                and_(
                    DocumentLabel.label_id.in_(_removed_labels),
                    DocumentLabel.document_id == _document.id)
            ).update(
                {
                    DocumentLabel.is_delete: True
                }
            )
            _session.flush()
            return {}


def new_paragraph(page_id, contents, paragraph_type):
    # background_task.delay(a="1", b="2")
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        _file_no = None
        try:
            _session.begin()
            _page = _session.query(Page).filter_by(id=page_id).first()
            _order = len(_page.paragraphs) + 1
            _file_no = uuid.uuid4().hex
            _new_paragraph = Paragraph(order=_order, page_id=_page.id,
                                       paragraph_type=paragraph_type, fileno=_file_no, blockno="")
            FileHandle.write_data(settings.DATA_URL.joinpath(_file_no), contents)
            _session.add(_new_paragraph)
            _session.flush()
            _new_paragraph_data = _new_paragraph.as_dict(paragraph_type="paragraphType")
            _session.commit()
            return _new_paragraph_data
        except Exception as e:
            _session.rollback()
            if _file_no:
                FileHandle.rm_data(settings.DATA_URL.joinpath(_file_no))
            raise e


def get_paragraphs(page_id):
    with DB.session() as session:
        _session: Session = session
        _page = _session.query(Page).filter(and_(Page.id == page_id, Page.is_delete is not True)).first()
        _paragraphs_list = []

        for paragraph in [e for e in _page.paragraphs if e.is_delete is False]:
            _file_no = paragraph.fileno
            _contents = FileHandle.read_data(settings.DATA_URL.joinpath(_file_no))
            _paragraph_data = paragraph.as_dict(paragraph_type="paragraphType")
            _paragraph_data["contents"] = _contents
            _paragraphs_list.append(_paragraph_data)

        return _paragraphs_list


def update_paragraph(paragraph_id, contents):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        _old_file_no = None
        resp_data = dict()
        with _session.begin() as transaction:
            # 把修改前的文档文件,移动至历史库
            _paragraph = _session.query(Paragraph).filter_by(id=paragraph_id).first()

            _old_file_no = _paragraph.fileno

            _his_content = HisContent(blockno=_paragraph.blockno, fileno=_paragraph.fileno)
            _paragraph.his_contents.append(_his_content)
            # 更新新的文档文件
            _new_file_no = uuid.uuid4().hex
            FileHandle.write_data(settings.DATA_URL.joinpath(_new_file_no), contents)
            _paragraph.fileno = _new_file_no
            resp_data = _paragraph.as_dict()
            _session.flush()
            _session.commit()
            FileHandle.move_data(settings.DATA_URL.joinpath(_old_file_no), settings.DATA_URL.joinpath("history"))
        return resp_data


def snapshot(document_id, name, description):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _document: Document = _session.query(Document).filter_by(id=document_id).first()
            _snapshot_doc = SnapshotDocument(name=name, description=description)
            _snapshot_doc.labels = "^&*".join([f'#{label.detail.parent_cat.name}#{label.detail.name}' for label in
                                               [e for e in _document.labels if not e.is_delete]])
            for page in _document.pages:
                _snapshot_page = SnapshotPage(page_name=page.name, order=page.order)
                for paragraph in page.paragraphs:
                    _fileno = paragraph.fileno
                    _contents = FileHandle.read_data(settings.DATA_URL.joinpath(_fileno))
                    _snapshot_fileno = uuid.uuid4().hex
                    FileHandle.write_data(settings.DATA_URL.joinpath("snapshot").joinpath(_snapshot_fileno), _contents)
                    _snapshot_paragraph = SnapshotParagraph(blockno="", fileno=_snapshot_fileno)
                    _snapshot_page.paragraphs.append(_snapshot_paragraph)
                _snapshot_doc.pages.append(_snapshot_page)
            _document.snapshots.append(_snapshot_doc)
            _document.status = Status.Document.Submit
            _session.flush()




def move_paragraph(change_orders):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            for change_order in change_orders:
                _paragraph = _session.query(Paragraph).filter_by(id=change_order.get("id")).first()
                _paragraph.order = change_order.get("order")
            _session.flush()
            _session.commit()


def delete_paragraph(paragraph_id):
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _paragraph = _session.query(Paragraph).filter_by(id=paragraph_id).first()
            _paragraph.is_delete = True
            for his_content in _paragraph.his_contents:
                his_content.is_delete = True
            _session.flush()
            _session.commit()


def delete_document(document_id):
    _author = ""
    with DB.session(autoflush=False, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _document = _session.query(Document).filter_by(id=document_id).first()
            _document.is_delete = True
            for page in _document.pages:
                page.is_delete = True
                for paragraph in page.paragraphs:
                    paragraph.is_delete = True
                    for his_content in paragraph.his_contents:
                        his_content.is_delete = True
            _author = _document.author
            _session.flush()
            _session.commit()
            REDIS.increment_page_total(REDIS.Key.DocTabAll, 'et_dev', -1)
            REDIS.increment_page_total(REDIS.Key.DocTabUser, _author, -1)
            return dict()
