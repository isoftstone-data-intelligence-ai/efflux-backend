from pydantic import BaseModel
from typing import Optional

# 会话用DTO
class ChatDTO(BaseModel):
    # 会话id
    chat_id: Optional[int] = None
    # system_message 系统提示词
    prompt: Optional[str] = None
    # mcp server name，选择已经加载的mcp sever执行任务
    server_id: Optional[int] = None
    # 用户输入的内容
    query: str
    # 对话历史记录
    history: Optional[dict] = None
    user_id: int