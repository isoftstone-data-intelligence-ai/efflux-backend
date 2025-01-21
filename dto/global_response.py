from typing import Optional, Any, Type
from fastapi.responses import JSONResponse
import json


# 接口统一返回体
class GlobalResponse(JSONResponse):
    # 接口状态码
    code: int
    # 接口讯息，通常为针对状态码code的描述
    message: str = "success"
    # 子状态码（业务异常码）
    sub_code: int
    # 子讯息（业务异常信息）
    sub_message: str
    # 接口返回数据
    data: Optional[Any]

    # 时间戳
    # timestamp: Optional[int]

    def __init__(
            self,
            code: int,
            sub_code: int,
            sub_message: str,
            data: Optional[Any] = None,
            json_encoder: Optional[Type[json.JSONEncoder]] = None,
            **kwargs
    ):
        content = {
            "code": code,
            "message": self.message,
            "sub_code": sub_code,
            "sub_message": sub_message,
            "data": data,
            # "timestamp": timestamp,
        }
        
        # 如果提供了自定义的 JSON 编码器，使用它来序列化内容
        if json_encoder:
            content = json.loads(json_encoder().encode(content))
            
        super().__init__(content=content, **kwargs)
