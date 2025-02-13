from pydantic import BaseModel

class LLMTemplateDTO(BaseModel):
    """LLM模板 DTO"""
    id: int
    provider: str
    model_display_name: str
    api_key_variable: str = 'API Key'
    base_url_variable: str = 'Base URL'
    model_variable: str = 'Model' 