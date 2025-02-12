from extensions.ext_database import Base
from sqlalchemy import Column, JSON, TIMESTAMP, BigInteger, String, Boolean
from datetime import datetime

class LlmConfig(Base):
    """LLM模型配置表，用于存储所有用户的LLM配置信息"""

    __tablename__ = 'llm_config'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    provider = Column(String(50), nullable=False)  # 模型提供商名称 (azure, qwen, doubao, moonshot, ollama)
    api_key = Column(String(200), nullable=False)
    base_url = Column(String(500), nullable=False)
    model = Column(String(100), nullable=False)  # 模型名称 (azure: deployment name, qwen: qwen-max等, doubao/moonshot: ep-xxx, ollama: deepseek-r1:8b等)
    extra_config = Column(JSON, nullable=True)  # 额外配置参数（如temperature等）
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)

    def model_dump(self) -> dict:
        """将模型序列化为字典"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "model": self.model,
            "extra_config": self.extra_config,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

