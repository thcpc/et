
from datetime import datetime, timezone

import jwt
from django.http import JsonResponse


from et.exceptions.business_error import InValidTokenError, TokenTimeOutError
from et.models import UserBase, UserFingerPrintBase
from et.settings import DB, REDIS, USER_TIMEOUT
from libs.jwt_utils import refresh_token_if_active, get_header_token, decode_jwt


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):

        excluded_paths = ['/user/api/login', '/user/api/register', '/user/api/device']
        if request.path in excluded_paths:
            return self.get_response(request)

        # 从请求头获取 Token
        token = get_header_token(request)
        if not token:
            return JsonResponse(InValidTokenError(message="", code=InValidTokenError.Code).body())

        try:
            # 验证 Token, 解析 Token 并判断超时
            payload = decode_jwt(token)
            # 验证是否合法
            _cache_token = REDIS.get_token(payload['user_id'])
            if _cache_token:
            # 如果能从 Redis 获取到 Token, 则对比
                if _cache_token != token:
                    raise jwt.InvalidTokenError()
            else:
            # 如果不能从 Redis 获取到 Token, 则与数据库中存储的Token对比
                with DB.session(autoflush=True, autobegin=True) as session:
                    _user = session.query(UserBase).filter_by(id=payload['user_id']).first()
                    if not _user: raise jwt.InvalidTokenError()
                    if _user.token != token: raise jwt.InvalidTokenError()
                    # 如果没有超时,也是正确的,则补充回 Redis
                    # 计算还剩下的超时时间
                    ex = USER_TIMEOUT - (int(datetime.now(tz=timezone.utc).timestamp())-payload["iat"])
                    REDIS.add_token(payload['user_id'], token, ex)
            # 验证通过, 判断是否需要延时
            new_token = refresh_token_if_active(payload, user_id=payload['user_id'], username=payload["username"])
            if new_token:
                REDIS.add_token(payload['user_id'], new_token,USER_TIMEOUT)
                with DB.session(autoflush=True, autobegin=True) as session:
                    _user = session.query(UserBase).filter_by(id=payload['user_id']).first()
                    _user.token = new_token
            REDIS.set_last_active(payload['user_id'], USER_TIMEOUT)
            request.user = dict(user_id=payload['user_id'], username=payload["username"])  # 将用户对象附加到请求
        except jwt.ExpiredSignatureError:
            return JsonResponse(TokenTimeOutError(message="", code=TokenTimeOutError.Code).body())
            # raise JsonResponse({'error': '令牌已过期'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse(InValidTokenError(message="", code=InValidTokenError.Code).body())

            # raise JsonResponse({'error': '无效令牌'}, status=401)

        return self.get_response(request)


