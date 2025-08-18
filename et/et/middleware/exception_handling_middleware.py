# middleware/exception_handler.py
import sentry_sdk
from django.http import JsonResponse

from et.exceptions.business_error import BusinessError


import logging

logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        # # 记录异常日志
        # logger.error(f"Unhandled exception: {str(exception)}", exc_info=True)

        # 根据异常类型返回不同的响应
        if isinstance(exception, BusinessError):
            exception.exception_invoke()
            return JsonResponse(exception.body())

        logger.critical(
            f"SYSTEM ERROR: {exception}",
            exc_info=True,
            extra={'request': request}
        )
        sentry_sdk.capture_exception(exception)
        # 默认错误响应
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error',
            'detail': str(exception)
        }, status=500)