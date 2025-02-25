from fastmcp import FastMCP
import httpx
from typing import Dict, Any, List

# 初始化 FastMCP 服务器
mcp = FastMCP("ip-geolocation")

@mcp.tool()
async def ip_geolocation(ip: str) -> Dict[str, Any]:
    """
    获取 IP 地址的地理位置和网络信息
    
    Args:
        ip: 要查询的 IP 地址
        
    Returns:
        包含位置信息的字典
    """
    try:
        # 使用 httpx 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
        
        # 检查响应状态
        if data.get("status") != "success":
            raise Exception("IP 查询失败")
            
        # 构建返回结果
        return {
            "content": [{
                "type": "text",
                "text": f"""IP Location Information for {ip}:
• Location: {data['city']}, {data['regionName']}, {data['country']}
• Coordinates: {data['lat']}, {data['lon']}
• Timezone: {data['timezone']}
• Network: {data['isp']}({data['org']})
• AS Number: {data['as']}"""
            }],
            "metadata": {
                "raw": data
            }
        }
        
    except Exception as error:
        print(f"工具执行错误: {error}")
        raise

if __name__ == "__main__":
    mcp.run(transport="stdio")