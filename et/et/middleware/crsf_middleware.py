from django.middleware.csrf import get_token


class CSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        _response = self.get_response(request)
        _csrf_token = get_token(request)
        _response.set_cookie(
            key="csrftoken",  # Cookie 名称
            value=_csrf_token,  # Token 值
            max_age=3600 * 24 * 7,  # 过期时间（7天，单位：秒）
            httponly=False,  # 仅 HTTP 访问，防止 XSS
            secure=False,  # 仅 HTTPS 传输
            samesite='Lax'  # 防止 CSRF
        )
        return _response