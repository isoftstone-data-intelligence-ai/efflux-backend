from typing import Type, Dict
from core.llm.llm_chat import LLMChat


class LLMManager:
    """
    管理多个语言模型（LLMChat）实例的管理器。

    该管理器允许通过名称获取特定的语言模型实现，并可以方便地在不同模型之间切换或访问。

    Attributes:
        llm_map (Dict[str, Type[LLMChat]]): 映射了语言模型名称到其实现类的字典。
    """

    def __init__(self, llm_map: Dict[str, Type[LLMChat]]):
        """
        初始化LLMManager类并设置语言模型映射。

        Args:
            llm_map (Dict[str, Type[LLMChat]]): 包含语言模型名称和对应实现类的映射。
        """
        self.llm_map = llm_map

    def get_llm(self, name: str) -> Type[LLMChat]:
        """
        根据给定的名称获取相应的语言模型实现类。

        如果提供的名称不在 `llm_map` 中，则会引发 KeyError 异常。

        Args:
            name (str): 要获取的语言模型的名称。

        Returns:
            Type[LLMChat]: 对应名称的语言模型实现类。

        Raises:
            KeyError: 如果提供的名称不在 `llm_map` 中。
        """
        return self.llm_map[name]

