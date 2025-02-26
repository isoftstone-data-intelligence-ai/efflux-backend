from datetime import datetime
from sqlalchemy import Column, BigInteger, JSON, String, TIMESTAMP
from extensions.ext_database import Base


class ChatMessage(Base):
    """
    "content": [
            {
                "type": "text",
                "text": "xxxxxxxxx",
                "image": null
            },
            {
                "type": "code",
                "text": "yyyyyyyy",
                "image": null
            }
        ]
    """
    __tablename__ = 'chat_message'

    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    # 会话id
    chat_window_id = Column(BigInteger, nullable=False, index=True)
    # 角色
    role = Column(String, nullable=False)
    # 内容
    content = Column(JSON)
    # 代码解析器内容
    code_object = Column(JSON)
    # 通用字段
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)

