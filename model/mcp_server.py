from sqlalchemy import Column, String, JSON, TIMESTAMP, TEXT, ARRAY, BigInteger
from extensions.ext_database import Base
from datetime import datetime

class McpServer(Base):
    __tablename__ = 'mcp_servers'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    server_name = Column(String(100), nullable=False)
    command = Column(String(100), nullable=False)
    args = Column(ARRAY(TEXT), nullable=False)
    env = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)

    def model_dump(self) -> dict:
        """将模型序列化为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "server_name": self.server_name,
            "command": self.command,
            "args": self.args,
            "env": self.env
        }

    def to_mcp_config(self) -> dict:
        """将服务器配置转换为标准MCP服务器配置格式
        
        Returns:
            dict: MCP服务器配置字典,格式如:
            {
                "server_name": {
                    "command": "command",
                    "args": ["arg1", "arg2"],
                    "env": {"key": "value"}  # env字段在没有环境变量时会被省略
                }
            }
        """
        return {
            self.server_name: {
                "command": self.command,
                "args": self.args,
                **({"env": self.env} if self.env else {})  # 如果self.env为空，则解包空字典{}，相当于不添加任何字段或键值对，env字段不会出现
            }
        }


