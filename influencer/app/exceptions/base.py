"""全局异常处理
"""
import logging

from app.core.response import HttpCode, HttpResp

__all__ = ['AppException']

logger = logging.getLogger(__name__)


class AppException(Exception):
    """应用异常基类
    """

    def __init__(self, exc: HttpCode = None, code: int = None, msg: str = None, echo_exc: bool = False, *args, **kwargs):
        super().__init__()
        _code = HttpResp.FAILED.code
        _message = HttpResp.FAILED.msg
        if code:
            _code = code
        elif exc and exc.code:
            _code = exc.code
        if msg:
            _message = msg
        elif exc and exc.msg:
            _message = exc.msg

        self._code = _code
        self._message = _message
        self.echo_exc = echo_exc
        self.args = args or []
        self.kwargs = kwargs or {}

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._message

    def __str__(self):
        return '{}: {}'.format(self.code, self.msg)
