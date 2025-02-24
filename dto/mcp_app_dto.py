from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class MCPAppDTO(BaseModel):
    """用于返回数据和更新操作的 DTO"""
    id: int
    name: str
    description: str
    icon_url: str
    
    # GitHub 仓库信息
    github_repo_id: int
    github_repo_name: str
    github_repo_full_name: str
    github_html_url: str
    github_url: str
    github_created_at: datetime
    github_updated_at: datetime
    github_pushed_at: datetime
    
    # MCP 服务器配置
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None
    
    # 通用字段
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateMCPAppDTO(BaseModel):
    """仅用于创建操作的 DTO"""
    name: str
    description: str
    icon_url: str
    
    # GitHub 仓库信息
    github_repo_id: int
    github_repo_name: str
    github_repo_full_name: str
    github_html_url: str
    github_url: str
    github_created_at: datetime
    github_updated_at: datetime
    github_pushed_at: datetime
    
    # MCP 服务器配置
    server_name: str
    command: str
    args: List[str] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None