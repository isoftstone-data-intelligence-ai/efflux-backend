from starlette.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from exception.exception_dict import ExceptionType
from utils import result_utils


# 基础API异常，特定异常须继承此类进行拓展
class BaseAPIException(HTTPException):
    """基础 API 异常类"""

    def __init__(
            self,
            status_code: int = ExceptionType.UNKNOWN_ERROR.code,
            detail: str = ExceptionType.UNKNOWN_ERROR.message
    ):
        super().__init__(status_code=status_code, detail=detail)


# 全局异常处理
async def global_exception_handler(request, exception):
    """处理通用 HTTP 异常"""
    return result_utils.build_error_response(
        sub_code=exception.status_code,
        sub_message=exception.detail
    )


# 请求数据无效异常处理
async def validate_exception_handler(request, exception):
    """处理请求参数验证异常"""
    err = exception.errors()[0]
    sub_code = 400
    return result_utils.build_validation_error_response(
        sub_code=sub_code,
        errors=exception.errors()
    )


# 指定异常对应的处理函数
global_exception_handlers = {
    HTTPException: global_exception_handler,
    RequestValidationError: validate_exception_handler
}
