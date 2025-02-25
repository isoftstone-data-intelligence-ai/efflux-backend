"""数学工具模块
这个模块提供了一系列可以被 LangChain ReAct Agent 直接调用的数学工具函数。
"""

import math
from typing import Union, List
import numpy as np
from langchain_core.tools import tool, ToolException
from pydantic import BaseModel, Field, field_validator

# class MathToolInput(BaseModel):
#     expression: str = Field(
#         description="单个数学表达式字符串",
#         examples="123 + 456 + 789 + 321",
#     )
#
#     @field_validator('expression')
#     @classmethod
#     def validate_expression(cls, v: str) -> str:
#         # 确保输入是字符串且不为空
#         if not isinstance(v, str) or not v.strip():
#             raise ValueError("表达式必须是非空字符串")
#         # 检查是否包含多个表达式（通过分号或换行符分隔）
#         if ";" in v or "\n" in v:
#             raise ValueError("一次只能计算一个表达式")
#         return v.strip()


def math_eval(expression: str) -> float:
    """数学表达式计算器：计算一个数学表达式的结果

    Args:
        expression (str): 需要计算的数学表达式字符串

    Returns:
        float: 表达式的计算结果

    Raises:
        ValueError: 当输入多个表达式或表达式格式不正确时抛出异常
        ToolException: 当计算出错时抛出异常

    Example:
        math_eval.invoke(expression="1 + 2 * 3") 返回 7.0
        math_eval.invoke(expression="math.sqrt(16) + 2") 返回 6.0
        math_eval.invoke(expression="max(1, 2, 3) + min(4, 5, 6)") 返回 7.0
    """
    try:
        # 创建一个包含必要函数的安全环境
        safe_dict = {
            "math": math,
            "sorted": sorted,
            "max": max,
            "min": min,
            "sum": sum,
            "abs": abs,
            "round": round,
            "pow": pow,
        }
        # 使用 eval 安全地计算表达式
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return float(result)
    except Exception as e:
        raise ToolException(f"计算错误: {str(e)}")

@tool
def statistical_analysis(numbers: List[float]) -> dict:
    """统计分析：计算一组数字的基本统计指标
    
    Args:
        numbers (List[float]): 需要分析的数字列表
    
    Returns:
        dict: 包含统计指标的字典，包括均值、中位数、标准差、最小值和最大值
        
    Raises:
        ToolException: 当输入无效或计算失败时抛出异常
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
            
        return {
            "mean": float(np.mean(numbers)),
            "median": float(np.median(numbers)),
            "std": float(np.std(numbers)),
            "min": float(np.min(numbers)),
            "max": float(np.max(numbers))
        }
    except Exception as e:
        raise ToolException(f"统计分析错误: {str(e)}")

@tool
def solve_quadratic_equation(a: float, b: float, c: float) -> List[Union[float, complex]]:
    """二次方程求解器：解决形如 ax² + bx + c = 0 的方程
    
    Args:
        a (float): x²的系数
        b (float): x的系数
        c (float): 常数项
    
    Returns:
        List[Union[float, complex]]: 方程的解（可能是实数或复数）
        
    Raises:
        ToolException: 当方程无效或求解失败时抛出异常
    """
    try:
        if a == 0:
            raise ToolException("a不能为0，这不是二次方程")
            
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return [x1, x2]
        elif discriminant == 0:
            x = -b / (2*a)
            return [x]
        else:
            real = -b / (2*a)
            imag = math.sqrt(abs(discriminant)) / (2*a)
            return [complex(real, imag), complex(real, -imag)]
    except Exception as e:
        raise ToolException(f"求解错误: {str(e)}")

@tool
def vector_operations(vector1: List[float], vector2: List[float], operation: str) -> Union[List[float], float]:
    """向量运算：执行基本的向量运算
    
    Args:
        vector1 (List[float]): 第一个向量
        vector2 (List[float]): 第二个向量
        operation (str): 运算类型 ('add', 'subtract', 'dot_product')
    
    Returns:
        Union[List[float], float]: 向量运算结果。对于加减法返回向量，对于点积返回标量
        
    Raises:
        ToolException: 当向量维度不匹配或运算类型无效时抛出异常
    """
    try:
        if len(vector1) != len(vector2):
            raise ToolException("两个向量的维度必须相同")
            
        v1 = np.array(vector1)
        v2 = np.array(vector2)
        
        if operation == "add":
            return list(v1 + v2)
        elif operation == "subtract":
            return list(v1 - v2)
        elif operation == "dot_product":
            return float(np.dot(v1, v2))
        else:
            raise ToolException("不支持的运算类型，只支持 'add'、'subtract' 或 'dot_product'")
    except Exception as e:
        raise ToolException(f"向量运算错误: {str(e)}")

@tool
def add_numbers(a: Union[int, float], b: Union[int, float]) -> float:
    """加法计算器：计算两个数字的和
    
    Args:
        a (Union[int, float]): 第一个数字
        b (Union[int, float]): 第二个数字
    
    Returns:
        float: 两数之和
        
    Raises:
        ToolException: 当输入无效或计算失败时抛出异常
        
    Example:
        add_numbers(2, 3) 返回 5.0
    """
    try:
        return float(a + b)
    except Exception as e:
        raise ToolException(f"加法计算错误: {str(e)}")

@tool
def subtract_numbers(a: Union[int, float], b: Union[int, float]) -> float:
    """减法计算器：计算两个数字的差
    
    Args:
        a (Union[int, float]): 被减数
        b (Union[int, float]): 减数
    
    Returns:
        float: a - b 的结果
        
    Raises:
        ToolException: 当输入无效或计算失败时抛出异常
        
    Example:
        subtract_numbers(5, 3) 返回 2.0
    """
    try:
        return float(a - b)
    except Exception as e:
        raise ToolException(f"减法计算错误: {str(e)}")

@tool
def multiply_numbers(a: Union[int, float], b: Union[int, float]) -> float:
    """乘法计算器：计算两个数字的积
    
    Args:
        a (Union[int, float]): 第一个数字
        b (Union[int, float]): 第二个数字
    
    Returns:
        float: 两数之积
        
    Raises:
        ToolException: 当输入无效或计算失败时抛出异常
        
    Example:
        multiply_numbers(2, 3) 返回 6.0
    """
    try:
        return float(a * b)
    except Exception as e:
        raise ToolException(f"乘法计算错误: {str(e)}")

@tool
def divide_numbers(a: Union[int, float], b: Union[int, float]) -> float:
    """除法计算器：计算两个数字的商
    
    Args:
        a (Union[int, float]): 被除数
        b (Union[int, float]): 除数
    
    Returns:
        float: a ÷ b 的结果
        
    Raises:
        ToolException: 当除数为0或输入无效时抛出异常
        
    Example:
        divide_numbers(6, 2) 返回 3.0
    """
    try:
        if b == 0:
            raise ToolException("除数不能为0")
        return float(a / b)
    except Exception as e:
        raise ToolException(f"除法计算错误: {str(e)}")

@tool
def sum_numbers(numbers: List[Union[int, float]]) -> float:
    """求和计算器：计算一组数字的总和

    Args:
        numbers (List[Union[int, float]]): 需要求和的数字列表

    Returns:
        float: 所有数字的总和

    Raises:
        ToolException: 当输入列表为空或包含无效数字时抛出异常

    Example:
        sum_numbers.invoke(numbers=[1, 2, 3, 4]) 返回 10.0
        sum_numbers.invoke(numbers=[1.5, 2.5, 3.0]) 返回 7.0
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
        return float(sum(numbers))
    except Exception as e:
        raise ToolException(f"求和计算错误: {str(e)}")

@tool
def avg_numbers(numbers: List[Union[int, float]]) -> float:
    """求平均值计算器：计算一组数字的平均值

    Args:
        numbers (List[Union[int, float]]): 需要计算平均值的数字列表

    Returns:
        float: 所有数字的平均值

    Raises:
        ToolException: 当输入列表为空或包含无效数字时抛出异常

    Example:
        avg_numbers.invoke(numbers=[1, 2, 3, 4]) 返回 2.5
        avg_numbers.invoke(numbers=[1.5, 2.5, 3.0]) 返回 2.33...
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
        return float(sum(numbers)) / len(numbers)
    except Exception as e:
        raise ToolException(f"求平均值计算错误: {str(e)}")

@tool
def median_numbers(numbers: List[Union[int, float]]) -> float:
    """求中位数计算器：计算一组数字的中位数

    Args:
        numbers (List[Union[int, float]]): 需要计算中位数的数字列表

    Returns:
        float: 所有数字的中位数

    Raises:
        ToolException: 当输入列表为空或包含无效数字时抛出异常

    Example:
        median_numbers.invoke(numbers=[1, 2, 3, 4, 5]) 返回 3.0
        median_numbers.invoke(numbers=[1, 2, 3, 4]) 返回 2.5
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
        sorted_numbers = sorted(numbers)
        length = len(sorted_numbers)
        if length % 2 == 0:
            # 偶数个数字,中位数是中间两个数的平均值
            mid1 = sorted_numbers[length // 2 - 1]
            mid2 = sorted_numbers[length // 2]
            return (mid1 + mid2) / 2
        else:
            # 奇数个数字,中位数是中间那个数
            return sorted_numbers[length // 2]
    except Exception as e:
        raise ToolException(f"求中位数计算错误: {str(e)}")

@tool
def max_numbers(numbers: List[Union[int, float]]) -> float:
    """求最大值计算器：计算一组数字的最大值

    Args:
        {"numbers": List[Union[int, float]]}
        List为需要计算最大值的数字列表

    Returns:
        float: 所有数字的最大值

    Raises:
        ToolException: 当输入列表为空或包含无效数字时抛出异常
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
        return max(numbers)
    except Exception as e:
        raise ToolException(f"求最大值计算错误: {str(e)}")

@tool
def min_numbers(numbers: List[Union[int, float]]) -> float:
    """求最小值计算器：计算一组数字的最小值

    Args:
        {"numbers": List[Union[int, float]]}
        List为需要计算最小值的数字列表

    Returns:
        float: 所有数字的最小值

    Raises:
        ToolException: 当输入列表为空或包含无效数字时抛出异常
    """
    try:
        if not numbers:
            raise ToolException("输入列表不能为空")
        return min(numbers)
    except Exception as e:
        raise ToolException(f"求最小值计算错误: {str(e)}")


# input = "109+173+237+301+813+365+429+493+557+621+685+749+877+941+1005"
# i = "(109 / 107 * 100 + 173 / 171 * 100 + 237 / 235 * 100 + 301 / 299 * 100 + 813 / 811 * 100 + 365 / 363 * 100 + 429 / 427 * 100 + 493 / 491 * 100 + 557 / 555 * 100 + 621 / 619 * 100 + 685 / 683 * 100 + 749 / 747 * 100 + 877 / 875 * 100 + 941 / 939 * 100 + 1005 / 1003 * 100) / 15"
# i = "sorted([109, 173, 237, 301, 813, 365, 429, 493, 557, 621, 685, 749, 877, 941, 1005])[7]"


# input2 = [109, 173, 237, 301, 813, 365, 429, 493, 557, 621, 685, 749, 877, 941, 1005]
# result = sum_numbers.invoke({"numbers": input2})
# print(result)