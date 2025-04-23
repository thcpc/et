from et.exceptions.call_back import CallBack


class BusinessError(Exception):
    def __init__(self, message, code, **kwargs):
        self.err = message
        self.code = code
        self.extra = kwargs
        self._call_back = None

    def body(self):
        return dict(code=self.code, err=self.err)

    @property
    def call_back(self) -> CallBack:
        return self._call_back

    def exception_invoke(self):
        if self.call_back:
            self.call_back.invoke()

    @call_back.setter
    def call_back(self, call_back_):
        self._call_back = call_back_


class InValidLoginError(BusinessError):
    Code = -101

    def __init__(self, message, code, **kwargs):
        super().__init__(message, code, **kwargs)


class InValidUserInfoError(BusinessError):
    Code = -104

    def __init__(self, message, code, **kwargs):
        super().__init__(message, code, **kwargs)


class InValidTokenError(BusinessError):
    Code = -102

    def __init__(self, message, code, **kwargs):
        super().__init__(message, code, **kwargs)


class TokenTimeOutError(BusinessError):
    Code = -103

    def __init__(self, message, code, **kwargs):
        super().__init__(message, code, **kwargs)
