from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class LLMConfigDTO(BaseModel):
    """用于返回数据和更新操作的 DTO"""
    id: int
    user_id: Optional[int] = None
    template_id: int
    provider: str
    api_key: str
    base_url: str
    model: str
    model_nickname: str
    extra_config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CreateLLMConfigDTO(BaseModel):
    """仅用于创建操作的 DTO"""
    user_id: Optional[int] = None
    template_id: int
    provider: str
    api_key: str
    base_url: str
    model: str
    model_nickname: str
    extra_config: Optional[Dict[str, Any]] = Field(default_factory=dict) 