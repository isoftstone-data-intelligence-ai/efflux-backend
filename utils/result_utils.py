from typing import Optional, Any
from dto.global_response import GlobalResponse
from pydantic import BaseModel
from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    """自定义JSON编码器，用于处理datetime对象"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def build_response(data: Optional[Any] = None) -> GlobalResponse:
    """构建成功响应
    
    Args:
        data: 响应数据，可以是 BaseModel、dict、list 或 None
        
    Returns:
        GlobalResponse: 统一的成功响应格式
    """
    # 如果是 Pydantic 模型或包含 Pydantic 模型的列表，转换为字典
    if isinstance(data, BaseModel):
        data = data.model_dump()
    elif isinstance(data, list):
        data = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        
    return GlobalResponse(
        code=200,
        sub_code=200,
        sub_message="success",
        data=data,
        json_encoder=DateTimeEncoder
    )


def build_error_response(sub_code: int, sub_message: str, data: Optional[Any] = None) -> GlobalResponse:
    """构建错误响应
    
    Args:
        sub_code: 错误码
        sub_message: 错误信息
        data: 可选的额外错误数据
        
    Returns:
        GlobalResponse: 统一的错误响应格式
    """
    return GlobalResponse(
        code=500,
        sub_code=sub_code,
        sub_message=sub_message,
        data=data,
        json_encoder=DateTimeEncoder
    )


def build_validation_error_response(sub_code: int, errors: list) -> GlobalResponse:
    """构建参数验证错误响应
    
    Args:
        sub_code: 子状态码
        errors: 验证错误列表
        
    Returns:
        GlobalResponse: 统一的验证错误响应格式
    """
    return GlobalResponse(
        code=400,
        sub_code=sub_code,
        sub_message="参数验证错误",
        data=errors,
        json_encoder=DateTimeEncoder
    )

def build_page_response(data: list, page: int, page_size: int, total: int) -> GlobalResponse:
    """构建分页响应
    
    Args:
        data: 分页数据列表
        page: 当前页码
        page_size: 每页数量
        total: 总记录数
        
    Returns:
        GlobalResponse: 统一的分页响应格式
    """
    # 如果是 Pydantic 模型列表，转换为字典列表
    if data and isinstance(data[0], BaseModel):
        data = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
    
    return GlobalResponse(
        code=200,
        sub_code=200,
        sub_message="success",
        data={
            "records": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size  # 计算总页数
        },
        json_encoder=DateTimeEncoder
    )
