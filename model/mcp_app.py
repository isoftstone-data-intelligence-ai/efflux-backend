from datetime import datetime

from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ARRAY, TEXT, JSON, Boolean

from extensions.ext_database import Base


class MCPApp(Base):
    """MCP 应用模型
    
    该模型用于存储 MCP 应用的基本信息、GitHub 仓库信息以及对应的 MCP 服务器配置。
    
    Attributes:
        基础信息:
            id: 应用唯一标识
            name: 应用名称
            description: 应用描述
            icon_url: 应用图标URL
            requires_configuration: 是否需要配置
            desktop_app: 是否为桌面应用
            
        GitHub 仓库信息:
            github_repo_id: GitHub 仓库唯一标识
            github_repo_name: 仓库名称（不包含所有者）
            github_repo_full_name: 仓库完整名称（owner/repo 格式）
            github_html_url: GitHub 仓库的 Web 页面地址
            github_url: GitHub 仓库的 API 访问地址
            github_created_at: 仓库创建时间
            github_updated_at: 仓库最后更新时间
            github_pushed_at: 最后一次代码推送时间
            
        MCP 服务器配置:
            server_name: MCP 服务器名称
            command: 服务启动命令
            args: 命令行参数列表
            env: 环境变量配置（可选）
            
        通用字段:
            created_at: 记录创建时间
            updated_at: 记录更新时间
    """
    __tablename__ = 'mcp_app'

    # 基础信息
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    icon_url = Column(String(100))
    requires_configuration = Column(Boolean, nullable=False, default=False)
    desktop_app = Column(Boolean, nullable=False, default=False)
    
    # GitHub 仓库信息
    github_repo_id = Column(BigInteger)
    github_repo_name = Column(String(100))
    github_repo_full_name = Column(String(100))
    github_html_url = Column(String(100))
    github_url = Column(String(100))
    github_created_at = Column(TIMESTAMP)
    github_updated_at = Column(TIMESTAMP)
    github_pushed_at = Column(TIMESTAMP)
    github_stars = Column(BigInteger)

    # MCP 服务器配置
    server_name = Column(String(100))
    command = Column(String(100))
    args = Column(ARRAY(TEXT))
    env = Column(JSON)

    # 通用字段
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)

