from datetime import datetime, timezone, timedelta

import jwt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from et import settings
from et.models import UserFingerPrintBase, UserBase
from et.settings import REDIS, USER_TIMEOUT, DB



def get_header_token(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Bearer '):
        fingerprint = request.META.get("fingerprint", '')
        if fingerprint:
            return token_by_fingerprint(fingerprint)
        else:
            return None
    else:
        return auth_header.split(' ')[1]


def token_by_fingerprint(self, fingerprint):
    with DB.session(autoflush=True, autobegin=False) as session:
        _session: Session = session
        _user_finger_print = _session.query(UserFingerPrintBase).filter(
            and_(UserFingerPrintBase.finger_print == fingerprint,
                 UserFingerPrintBase.is_delete is not True)).first()
        if _user_finger_print:
            _token = REDIS.get_token(_user_finger_print.user_id)
            if _token:
                return _token
            else:
                _user = _session.query(UserBase).filter_by(id=_user_finger_print.user_id).first()
                if _user.token:
                    return _user.token
        return ""


def encode_jwt(user_id, username) -> str:
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': int((datetime.now(tz=timezone.utc) + timedelta(seconds=USER_TIMEOUT)).timestamp()),
        'iat': int(datetime.now(tz=timezone.utc).timestamp())
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def get_user_id(token):
    return decode_jwt(token, verify=False)["user_id"]


def decode_jwt(token, verify=True) -> dict:
    if verify:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    else:
        options = {
            "verify_signature": False,  # 忽略签名验证
            "verify_exp": False,  # 忽略过期时间验证
            "verify_nbf": False,  # 忽略"not before"时间验证
            "verify_iat": False,  # 忽略签发时间验证
            "verify_aud": False,  # 忽略受众验证
            "verify_iss": False  # 忽略签发者验证
        }
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options=options)


def refresh_token_if_active(old_token, user_id, username):
    last_active = REDIS.get_last_active(user_id)
    last_active = last_active if last_active else 0
    active_time = int(datetime.now(tz=timezone.utc).timestamp()) - int(last_active)
    iat_last = int(datetime.now(tz=timezone.utc).timestamp()) - old_token.get("iat")
    if last_active and active_time < 10 * 60 and 50 * 60 < iat_last < 60 * 60:
        # 10分钟内活跃过 并且 过期时间剩余10分钟
        # 更新并延长1小时
        new_token = encode_jwt(user_id, username)
        return new_token
    return None
