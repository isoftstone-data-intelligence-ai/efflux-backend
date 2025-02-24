from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MCPAppDTO(BaseModel):
    """用于返回数据和更新操作的 DTO"""
    id: int
    app_name: str
    description: str
    source_link: str
    icon_url: str
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None

class CreateMCPAppDTO(BaseModel):
    """仅用于创建操作的 DTO"""
    app_name: str
    description: str
    source_link: str
    icon_url: str
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None