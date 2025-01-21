from extensions.ext_database import Base
from sqlalchemy import Column, JSON, TIMESTAMP, BigInteger, String
from datetime import datetime

class ChatWindow(Base):
    __tablename__ = 'chat_window'

    # 主键
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    # 用户id
    user_id = Column(BigInteger, nullable=False, index=True)
    # 会话概要
    summary = Column(String(100), nullable=False)
    # 会话内容
    content = Column(JSON, nullable=True)
    # 创建时间
    created_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now)
    # 更新时间
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, default=datetime.now, onupdate=datetime.now)
