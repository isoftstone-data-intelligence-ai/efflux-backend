from typing import List, Optional
from sqlalchemy.future import select
from datetime import datetime
from model.chat_window import ChatWindow


# 会话记录DAO
class ChatWindowDAO:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def create_chat_window(self, user_id, summary, content: Optional[str] = None):
        async with self._session_factory() as session:
            new_chat_window = ChatWindow(
                user_id=user_id,
                summary=summary,
                content=content,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        session.add(new_chat_window)
        await session.commit()
        return new_chat_window

    async def delete_chat_window(self, chat_window_id):
        async with self._session_factory() as session:
            chat_window = session.query(ChatWindow).get(chat_window_id)
            if chat_window:
                session.delete(chat_window)
                await session.commit()
                return chat_window_id

    async def update_chat_window(self, chat_window_id, summary, content):
        async with self._session_factory() as session:
            result = await session.execute(
                select(ChatWindow).where(ChatWindow.id == chat_window_id)
            )
            chat_window = result.scalar_one_or_none()

            if chat_window:
                if summary:
                    chat_window.summary = summary
                chat_window.content = content
                chat_window.updated_at = datetime.now()
                await session.commit()
                return chat_window_id

    async def get_user_chat_windows(self, user_id) -> List[ChatWindow]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(
                    ChatWindow.id,
                    ChatWindow.user_id,
                    ChatWindow.summary,
                    ChatWindow.created_at,
                    ChatWindow.updated_at
                ).where(ChatWindow.user_id == user_id)
                .order_by(ChatWindow.id.desc())
            )
            return result.all()

    async def get_chat_window_by_id(self, chat_window_id: int) -> ChatWindow:
        async with self._session_factory() as session:
            result = await session.execute(
                select(ChatWindow).where(ChatWindow.id == chat_window_id)
            )
            return result.scalar_one_or_none()
