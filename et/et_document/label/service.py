from sqlalchemy.orm import Session

from et.settings import DB
from et_document.label.relationship_def import Label, LabelCategory
# from label.models import Label, LabelCategory


def new_label(categoryId, name):
    with DB.session(autoflush=True, autobegin=False) as session:
        _session: Session = session
        with _session.begin():
            _new_label = Label(name=name, category_id=categoryId)
            _session.add(_new_label)
            _session.flush()
            return _new_label.as_dict()


def get_labels():
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        _resp_data = []
        # with _session.begin() as transaction:
        # 把修改前的文档文件,移动至历史库
        _categories = _session.query(LabelCategory).order_by("id").all()
        for category in _categories:
            _category_data = category.as_dict()
            _category_data["labels"] = [label.as_dict() for label in category.labels]
            _resp_data.append(_category_data)
        return _resp_data
