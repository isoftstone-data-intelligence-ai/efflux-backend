from typing import Optional
from sqlalchemy.future import select
from datetime import datetime
from model.chat_message import ChatMessage


class ChatMessageDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def add_chat_message(
        self,
        chat_window_id: int,
        role: str,
        content: dict,
        code_object: Optional[dict] = None
    ):
        async with self._session_factory() as session:
            new_chat_message = ChatMessage(
                chat_window_id=chat_window_id,
                role=role,
                content=content,
                code_object=code_object,
                created_at=datetime.now()
            )
            session.add(new_chat_message)
            await session.commit()
            return new_chat_message

    async def get_messages_by_window_id(self, chat_window_id: int):
        async with self._session_factory() as session:
            query = select(ChatMessage).where(
                ChatMessage.chat_window_id == chat_window_id
            ).order_by(ChatMessage.created_at.desc())
            
            result = await session.execute(query)
            messages = result.scalars().all()
            return messages
