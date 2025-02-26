from typing import List

from dao.chat_message_dao import ChatMessageDAO
from dao.chat_window_dao import ChatWindowDAO
from dto.chat_window_dto import ChatWindowDTO, ContentDTO, CodeInterpreterObjectDTO, ChatMessageDTO
from model.chat_window import ChatWindow


class ChatWindowService:
    def __init__(self, chat_window_dao: ChatWindowDAO, chat_message_dao: ChatMessageDAO):
        self.chat_window_dao = chat_window_dao
        self.chat_message_dao = chat_message_dao


    async def add_code_history(self, chat_window: ChatWindow) -> bool:
        """
        新增代码模式历史记录
        :param chat_window:
        :return: bool
        """


    async def get_user_chat_windows(self, user_id: int) -> List[ChatWindowDTO]:
        result = await self.chat_window_dao.get_user_chat_windows(user_id)
        return await self.convert_models_to_chat_windows(result)


    async def get_chat_window_by_id(self, chat_window_id: int) -> ChatWindowDTO | None:
        # 获取聊天窗口基本信息
        chat_window = await self.chat_window_dao.get_chat_window_by_id(chat_window_id)
        if not chat_window:
            return None
        
        # 获取该窗口的所有聊天消息
        messages = await self.chat_message_dao.get_messages_by_window_id(chat_window_id)
        
        # 转换消息格式
        chat_messages = []
        for message in messages:
            # 转换 content 列表
            content_dtos = []
            if isinstance(message.content, list):
                for content_item in message.content:
                    if isinstance(content_item, dict):
                        content_dto = ContentDTO(
                            type=content_item["type"],
                            text=content_item["text"] if "text" in content_item else None,
                            image=content_item["image"] if "image" in content_item else None
                        )
                        content_dtos.append(content_dto)
            
            # 转换 code_object（如果存在）
            code_object = None
            if message.code_object:
                code_object = CodeInterpreterObjectDTO(**message.code_object)
            
            # 创建 ChatMessageDTO
            chat_message = ChatMessageDTO(
                role=message.role,
                content=content_dtos,
                object=code_object
            )
            chat_messages.append(chat_message)
            
        # 创建并返回 ChatWindowDTO
        return ChatWindowDTO(
            id=chat_window.id,
            user_id=chat_window.user_id,
            summary=chat_window.summary,
            chat_messages=chat_messages,
            created_at=chat_window.created_at,
            updated_at=chat_window.updated_at
        )


    async def convert_models_to_chat_windows(self, chat_windows: List[ChatWindow]) -> List[ChatWindowDTO]:
        return [self.convert_model_to_chat_window_dto(chat_window) for chat_window in chat_windows]

    @staticmethod
    def convert_model_to_chat_window_dto(chat_window: ChatWindow) -> ChatWindowDTO:
        return ChatWindowDTO(
            id=chat_window.id,
            user_id=chat_window.user_id,
            summary=chat_window.summary,
            created_at=chat_window.created_at,
            updated_at=chat_window.updated_at
        )