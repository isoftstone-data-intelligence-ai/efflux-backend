from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class MCPAppDTO(BaseModel):
    """用于返回数据和更新操作的 DTO"""
    id: int
    name: str
    description: str
    icon_url: Optional[str] = None
    requires_configuration: bool = False
    desktop_app: bool = False  # 新增字段：是否为桌面应用
    
    # GitHub 仓库信息
    github_repo_id: Optional[int] = None
    github_repo_name: Optional[str] = None
    github_repo_full_name: Optional[str] = None
    github_html_url: Optional[str] = None
    github_url: Optional[str] = None
    github_created_at: Optional[datetime] = None
    github_updated_at: Optional[datetime] = None
    github_pushed_at: Optional[datetime] = None
    github_stars: Optional[int] = None  # 新增字段：GitHub 仓库星数
    
    # MCP 服务器配置
    server_name: str
    command: str
    args: Optional[List[str]] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None
    
    # 通用字段
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CreateMCPAppDTO(BaseModel):
    """仅用于创建操作的 DTO"""
    name: str
    description: str
    icon_url: str
    requires_configuration: bool
    desktop_app: bool = False
    
    # GitHub 仓库信息
    github_repo_id: Optional[int] = None
    github_repo_name: Optional[str] = None
    github_repo_full_name: Optional[str] = None
    github_html_url: Optional[str] = None
    github_url: Optional[str] = None
    github_created_at: Optional[datetime] = None
    github_updated_at: Optional[datetime] = None
    github_pushed_at: Optional[datetime] = None
    github_stars: Optional[int] = None
    
    # MCP 服务器配置
    server_name: str
    command: str
    args: Optional[List[str]] = Field(default_factory=list)
    env: Optional[Dict[str, str]] = None