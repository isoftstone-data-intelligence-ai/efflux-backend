import uvicorn
import math
import logging as logger

from mcp.server.sse import SseServerTransport
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route, Mount

mcp_server = FastMCP(name="math eval server")
sse_transport = SseServerTransport('/messages/')


@mcp_server.tool(name="math_eval", description="Math Evaluator")
async def math_eval(expression: str) -> float:
    print(expression)
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
        logger.info(f"Math Evaluation result: {float(result)}")
        return float(result)
    except Exception as e:
        raise Exception(f"计算错误: {str(e)}")


async def sse_handler(request):
    async with sse_transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp_server._mcp_server.run(streams[0], streams[1], mcp_server._mcp_server.create_initialization_options())


app = Starlette(
    debug=True,
    routes=[
        Route("/math_eval_server", endpoint=sse_handler),
        Mount("/messages/", app=sse_transport.handle_post_message),
    ]
)

uvicorn.run(app, host="127.0.0.1", port=8002)
