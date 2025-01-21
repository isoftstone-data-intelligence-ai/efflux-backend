from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MCPServerDTO(BaseModel):
    """用于返回数据和更新操作的 DTO"""
    id: int
    user_id: int
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)  # Pydantic会自动处理可变默认值的问题，为每个实例创建一个深拷贝
    env: Optional[Dict[str, str]] = None           # Pylint不了解Pydantic的这个特性，所以有红线，可以忽略


class CreateMCPServerDTO(BaseModel):
    """仅用于创建操作的 DTO"""
    user_id: int
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None