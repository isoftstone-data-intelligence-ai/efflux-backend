from pydantic import BaseModel
from typing import Optional, List

# 会话内容
class Content(BaseModel):
    type: Optional[str] = None
    text: Optional[str] = None


# 会话用DTO
class ChatDTO(BaseModel):
    # 会话id
    chat_id: Optional[int] = None
    # system_message 系统提示词
    prompt: Optional[str] = None
    # mcp server name，选择已经加载的mcp sever执行任务
    server_id: Optional[int] = None
    # 用户输入的会话内容
    query: List[Content]
    # 对话历史记录
    history: Optional[dict] = None
    user_id: int
    model_id: int


