from typing import List
from dao.chat_window_dao import ChatWindowDAO
from dto.chat_window_dto import ChatWindowDTO
from model.chat_window import ChatWindow


class ChatWindowService:
    def __init__(self, chat_window_dao: ChatWindowDAO):
        self.chat_window_dao = chat_window_dao


    async def add_code_history(self, chat_window: ChatWindow) -> bool:
        """
        新增代码模式历史记录
        :param chat_window:
        :return: bool
        """


    async def get_user_chat_windows(self, user_id: int) -> List[ChatWindowDTO]:
        result = await self.chat_window_dao.get_user_chat_windows(user_id)
        return await self.convert_models_to_chat_windows(result)

    async def convert_models_to_chat_windows(self, chat_windows: List[ChatWindow]) -> List[ChatWindowDTO]:
        return [self.convert_model_to_chat_window_dto(chat_window) for chat_window in chat_windows]

    @staticmethod
    def convert_model_to_chat_window_dto(chat_window: ChatWindow) -> ChatWindowDTO:
        # 确保 content 字段有值，如果为 None 则使用空列表
        chat_messages = chat_window.content if chat_window.content else []
        
        return ChatWindowDTO(
            id=chat_window.id,
            user_id=chat_window.user_id,
            summary=chat_window.summary,
            chat_messages=chat_messages,
            created_at=chat_window.created_at,
            updated_at=chat_window.updated_at
        )