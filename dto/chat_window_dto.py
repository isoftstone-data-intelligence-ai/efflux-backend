from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# 对话信息内容
class ContentDTO(BaseModel):
    type: str  # text | image | code | file
    text: Optional[str] = None
    image: Optional[str] = None
    
    def model_dump(self, **kwargs):
        return {
            "type": self.type,
            "text": self.text,
            "image": self.image
        }

# 对话信息记录
class ChatMessageDTO(BaseModel):
    role: str # user | assistant
    content: List[ContentDTO]
    
    def model_dump(self, **kwargs):
        return {
            "role": self.role,
            "content": [c.model_dump() for c in self.content]
        }

# 会话DTO
class ChatWindowDTO(BaseModel):
    # 主键
    id: int
    # 用户id
    user_id: int
    # 概要
    summary: Optional[str] = None
    # 对话信息记录
    chat_messages: List[ChatMessageDTO] = []
    created_at: datetime
    updated_at: datetime
    
    def model_dump(self, **kwargs):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "summary": self.summary,
            "chat_messages": [m.model_dump() for m in self.chat_messages],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }






