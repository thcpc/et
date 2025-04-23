from functools import wraps
from gc import is_finalized

from et.settings import CELERY_TASK_SERIALIZER


def handle_db_exceptions(exceptions):
    def decorator(func):
        ori, code, covert, eval_str, dynamic = 0, 1, 2, 3, 4

        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                for exception in exceptions:
                    if isinstance(e, exception[ori]) and e.orig.args[0] == exception[code]:
                        message = eval(exception[eval_str]) if exception[dynamic] else exception[eval_str]
                        raise exception[covert](message, exception[covert].Code)
                raise e

        return wrapped

    return decorator
