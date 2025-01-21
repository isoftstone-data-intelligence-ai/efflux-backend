from pydantic import BaseModel

class LLMMessage(BaseModel):
    type: str
    content: str