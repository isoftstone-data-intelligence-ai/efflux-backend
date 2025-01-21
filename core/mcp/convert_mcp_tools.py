from langchain_core.tools import BaseTool, ToolException
from typing import Type, List
from jsonschema_pydantic import jsonschema_to_pydantic
from pydantic import BaseModel
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


def create_langchain_tool(
        tool_schema: types.Tool,
        server_params: StdioServerParameters
) -> BaseTool:
    """Create a LangChain tool from MCP tool schema."""
    input_model = jsonschema_to_pydantic(tool_schema.inputSchema)

    class McpTool(BaseTool):
        name: str = tool_schema.name
        description: str = tool_schema.description
        args_schema: Type[BaseModel] = input_model
        mcp_server_params: StdioServerParameters = server_params

        def _run(self, **kwargs):
            raise NotImplementedError("Only async operations are supported")

        async def _arun(self, **kwargs):
            async with stdio_client(self.mcp_server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(self.name, arguments=kwargs)
                    if result.isError:
                        raise ToolException(result.content)
                    return result.content

    return McpTool()


async def convert_mcp_to_langchain_tools(server_params: List[StdioServerParameters]) -> List[BaseTool]:
    """Convert MCP tools to LangChain tools."""
    langchain_tools = []

    for server_param in server_params:
        # cached_tools = get_cached_tools(server_param)
        #
        # if cached_tools:
        #     for tool in cached_tools:
        #         langchain_tools.append(create_langchain_tool(tool, server_param))
        #     continue

        async with stdio_client(server_param) as (read, write):
            async with ClientSession(read, write) as session:
                print(f"Gathering capability of {server_param.command} {' '.join(server_param.args)}")
                await session.initialize()
                tools: types.ListToolsResult = await session.list_tools()
                #save_tools_cache(server_param, tools.tools)

                for tool in tools.tools:
                    langchain_tools.append(create_langchain_tool(tool, server_param))

    return langchain_tools