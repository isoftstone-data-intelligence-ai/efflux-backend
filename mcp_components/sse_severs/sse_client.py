import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    while True:
        expression = await asyncio.get_event_loop().run_in_executor(None,input, 'Expression:')

        print(expression)
        try:
            async with sse_client("http://localhost:8002/math_eval_server") as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    tools = await load_mcp_tools(session)
                    result = await session.call_tool('math_eval', arguments={'expression':expression})
                    print(result)
        except Exception as e:
            print('can not connect to mcp_server')

asyncio.run(main())