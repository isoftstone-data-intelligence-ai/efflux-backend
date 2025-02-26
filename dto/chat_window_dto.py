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

# 代码解释器对象
class CodeInterpreterObjectDTO(BaseModel):
    commentary: str
    template: str
    title: str
    description: str
    additional_dependencies: List[str] = []
    has_additional_dependencies: bool = False
    install_dependencies_command: str = ""
    port: Optional[int] = None
    file_path: str
    code: str

    def model_dump(self, **kwargs):
        return {
            "commentary": self.commentary,
            "template": self.template,
            "title": self.title,
            "description": self.description,
            "additional_dependencies": self.additional_dependencies,
            "has_additional_dependencies": self.has_additional_dependencies,
            "install_dependencies_command": self.install_dependencies_command,
            "port": self.port,
            "file_path": self.file_path,
            "code": self.code
        }

# 对话信息记录
class ChatMessageDTO(BaseModel):
    role: str # user | assistant
    content: List[ContentDTO]
    object: Optional[CodeInterpreterObjectDTO] = None

    def model_dump(self, **kwargs):
        return {
            "role": self.role,
            "content": [c.model_dump() for c in self.content],
            "object": self.object.model_dump() if self.object else None
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






