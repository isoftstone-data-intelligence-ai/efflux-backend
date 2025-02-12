from extensions.ext_database import Base
from sqlalchemy import Column, BigInteger, String

class LlmTemplate(Base):
    """LLM 模型模板表，用于前端展示可用的模型列表及其对应的配置变量名"""

    __tablename__ = 'llm_template'

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    provider = Column(String(50), nullable=False)  # 模型提供商名称 (azure, qwen, doubao, moonshot, ollama)
    model_name = Column(String(100), nullable=False)  # 展示给用户的 Model 名称
    api_key_variable = Column(String(50), default='API Key')  # 存储 API Key 的配置变量名 (如: API_KEY)
    base_url_variable = Column(String(50), default='Base URL')  # 存储 Base URL/Endpoint 的配置变量名 (如: BASE_URL, ENDPOINT, etc)
    model_variable = Column(String(50), default='Model')  # 存储模型名称/版本号的配置变量名 (如: MODEL, API_VERSION, etc)

    def model_dump(self) -> dict:
        """将模型序列化为字典"""
        return {
            "id": self.id,
            "provider": self.provider,
            "model_name": self.model_name,
            "api_key_variable": self.api_key_variable,
            "base_url_variable": self.base_url_variable,
            "model_variable": self.model_variable
        }




