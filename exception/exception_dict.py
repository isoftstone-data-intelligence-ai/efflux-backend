from enum import Enum

class ExceptionType(Enum):
    UNKNOWN_ERROR = (1, "未知的异常")
    INVALID_PARAM = (2, "参数校验异常")
    RESOURCE_NOT_FOUND = (3, "资源未找到")
    DUPLICATE_ENTRY = (4, "检测到重复条目")
    AUTHENTICATION_FAILED = (5, "身份验证失败")
    AUTHORIZATION_FAILED = (6, "授权失败")
    SERVER_UPDATE_FAILED = (7, "服务器更新失败")
    SERVER_DELETE_FAILED = (8, "服务器删除失败")
    DUPLICATE_SERVER_NAME = (9, "服务器名称已存在")
    # 追加自定义异常




    def __new__(cls, code, message):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        obj.code = code
        obj.message = message
        return obj

"""
在业务判断中，声明BaseAPIException，传入ExceptionType的code和message
代码示例:

async def get_id_by_user(user_id: int):
    if user_id != 1:
        raise BaseAPIException(
            status_code=ExceptionDict.INVALID_PARAM.code,
            detail=ExceptionDict.INVALID_PARAM.message
            )
    return {"user_id": user_id}
"""