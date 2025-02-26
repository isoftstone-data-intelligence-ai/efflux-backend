from typing import List
from dao.chat_window_dao import ChatWindowDAO
from dto.chat_window_dto import ChatWindowDTO
from model.chat_window import ChatWindow


class ChatWindowService:
    def __init__(self, chat_window_dao: ChatWindowDAO, chat_message_dao: ChatWindowDAO):
        self._session_factory = session_factory
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


    async def get_chat_window_by_id(self, chat_window_id: int) -> ChatWindowDTO:
        # 获取聊天窗口基本信息
        chat_window = await self.chat_window_dao.get_chat_window_by_id(chat_window_id)
        if not chat_window:
            return None
        
        # 获取该窗口的所有聊天消息
        messages = await self.chat_message_dao.get_messages_by_window_id(chat_window_id)
        
        # 将消息转换为 DTO 格式
        chat_messages = []
        for message in messages:
            content_list = []
            for content_item in message.content:
                content_list.append(ContentDTO(
                    type=content_item.get('type'),
                    text=content_item.get('text'),
                    image=content_item.get('image')
                ))
            
            # 如果存在代码解析器对象，则转换它
            code_object = None
            if message.code_object:
                code_object = CodeInterpreterObjectDTO(**message.code_object)
            
            chat_messages.append(ChatMessageDTO(
                role=message.role,
                content=content_list,
                object=code_object
            ))
        
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