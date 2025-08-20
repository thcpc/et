from functools import wraps

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from et.exceptions.business_error import InValidUserInfoError, InValidLoginError
from et.exceptions.decorators import handle_db_exceptions
from et.models import UserBase
from et.settings import DB, REDIS, USER_TIMEOUT
from libs.jwt_utils import encode_jwt, decode_jwt, get_user_id
from et_admin.user.relationship_def import User, UserFingerPrint


@handle_db_exceptions(exceptions=(
    (IntegrityError, 1062, InValidUserInfoError, "f'{args[0]} 已注册'", True),
    (IntegrityError, 1048, InValidUserInfoError, "username 和 password 不能为空", False),
))
def register(name, password):
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        _new_user = User(name=name, password=password)
        _session.add(_new_user)
        _session.commit()
        return {}


def RedisToken(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        resp = func(*args, **kwargs)
        REDIS.add_token(resp.get("id"), resp.get("token"), ex=USER_TIMEOUT)
        return {"token": resp.get("token")}

    return wrapped


def valid_user(user, password):
    return user and user.password == password

@RedisToken
def login_by_name(name, password, finger_print):
    with DB.session(autoflush=True, autobegin=False) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _user = User.user(_session, name=name)
            if valid_user(_user, password):
                _user.token = encode_jwt(_user.id, _user.name)
                if finger_print and finger_print not in [p.finger_print for p in _user.finger_prints]:
                    _user.finger_prints.append(UserFingerPrint(finger_print=finger_print))
                return {"token": _user.token, "id": _user.id}
    raise InValidLoginError(code=InValidLoginError.Code, message="用户名,密码错误")


@RedisToken
def login_by_finger(old_token, finger_print, password):
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _finger_print = UserFingerPrint.fingerPrint(_session, finger_print=finger_print)
            _user = _finger_print.ref_user if _finger_print else User.user(_session, id=get_user_id(old_token))
            if valid_user(_user, password):
                _user.token = encode_jwt(_user.id, _user.name)
                return {"token": _user.token, "id": _user.id}
    raise InValidLoginError(code=InValidLoginError.Code, message="用户名,密码错误")


def device(finger_print):
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _finger_print = UserFingerPrint.fingerPrint(_session, finger_print=finger_print)
            return {"username": _finger_print.ref_user.name if _finger_print else ""}


@RedisToken
def quick_login(finger_print):
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        with _session.begin() as transaction:
            _finger_print = UserFingerPrint.fingerPrint(_session, finger_print=finger_print)
            if _finger_print is not None:
                _user = _finger_print.ref_user
                token = encode_jwt(_user.id, _user.name)
                _user.token = token
                return {"token": token, "id": _user.id}
    raise InValidLoginError(code=InValidLoginError.Code, message="未记录该设备,登录失败")


def users(self_user_id):
    with DB.session(autoflush=True, autobegin=True) as session:
        _session: Session = session
        _users = _session.query(UserBase).filter(and_(UserBase.is_delete == False, UserBase.id != self_user_id)).all()
        return [u.as_dict() for u in _users]
