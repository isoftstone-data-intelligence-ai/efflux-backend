import os
import httpx
from typing import Dict, List, Optional, TypedDict, Union
from fastmcp import FastMCP

# 定义类型
class Genre(TypedDict):
    id: int
    name: str

class Movie(TypedDict):
    id: int
    title: str
    release_date: str
    vote_average: float
    overview: str
    poster_path: Optional[str]
    genres: Optional[List[Genre]]

class CastMember(TypedDict):
    name: str
    character: str

class CrewMember(TypedDict):
    name: str
    job: str

class Review(TypedDict):
    author: str
    content: str
    rating: Optional[float]

class MovieDetails(Movie):
    credits: Optional[Dict[str, Union[List[CastMember], List[CrewMember]]]]
    reviews: Optional[Dict[str, List[Review]]]

# 初始化常量和 FastMCP
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"
# TMDB_API_KEY = "0589ef0e07ea3d9ce742f46e81051f18"

mcp = FastMCP("tmdb")

async def fetch_from_tmdb(endpoint: str, params: Dict[str, str] = None) -> Dict:
    """从TMDB API获取数据"""
    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TMDB_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

async def get_movie_details(movie_id: str) -> MovieDetails:
    """获取电影详细信息"""
    return await fetch_from_tmdb(f"/movie/{movie_id}", 
                                {"append_to_response": "credits,reviews"})

@mcp.tool()
async def list_resources(cursor: Optional[str] = None) -> Dict:
    """列出热门电影资源
    
    Args:
        cursor: 分页游标，默认为第一页
        
    Returns:
        包含电影资源列表的字典
    """
    params = {"page": cursor or "1"}
    data = await fetch_from_tmdb("/movie/popular", params)
    
    return {
        "resources": [{
            "uri": f"tmdb:///movie/{movie['id']}",
            "mimeType": "application/json",
            "name": f"{movie['title']} ({movie['release_date'].split('-')[0]})"
        } for movie in data['results']],
        "nextCursor": str(data['page'] + 1) if data['page'] < data['total_pages'] else None
    }

@mcp.tool()
async def read_resource(uri: str) -> Dict:
    """读取特定电影资源
    
    Args:
        uri: 电影资源的 URI
        
    Returns:
        包含电影详细信息的字典
    """
    movie_id = uri.replace("tmdb:///movie/", "")
    movie = await get_movie_details(movie_id)
    
    movie_info = {
        "title": movie["title"],
        "releaseDate": movie["release_date"],
        "rating": movie["vote_average"],
        "overview": movie["overview"],
        "genres": ", ".join(g["name"] for g in movie.get("genres", [])),
        "posterUrl": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else "No poster available",
        "cast": [f"{actor['name']} as {actor['character']}" for actor in movie.get("credits", {}).get("cast", [])[:5]],
        "director": next((person["name"] for person in movie.get("credits", {}).get("crew", []) 
                         if person["job"] == "Director"), None),
        "reviews": [{
            "author": review["author"],
            "content": review["content"],
            "rating": review.get("rating")
        } for review in movie.get("reviews", {}).get("results", [])[:3]]
    }
    
    return {
        "contents": [{
            "uri": uri,
            "mimeType": "application/json",
            "text": movie_info
        }]
    }

# @mcp.tool()
# async def search_movies(query: str) -> str:
#     """搜索电影
#
#     Args:
#         query: 搜索关键词
#     """
#     data = await fetch_from_tmdb("/search/movie", {"query": query})
#
#     results = []
#     for movie in data["results"]:
#         year = movie["release_date"].split("-")[0] if movie["release_date"] else "N/A"
#         results.append(
#             f"{movie['title']} ({year}) - ID: {movie['id']}\n"
#             f"Rating: {movie['vote_average']}/10\n"
#             f"Overview: {movie['overview']}\n"
#         )
#
#     return f"Found {len(data['results'])} movies:\n\n" + "\n---\n".join(results)

@mcp.tool()
async def get_recommendations(movie_id: str) -> str:
    """获取电影推荐
    
    Args:
        movie_id: TMDB电影ID
    """
    data = await fetch_from_tmdb(f"/movie/{movie_id}/recommendations")
    
    recommendations = []
    for movie in data["results"][:5]:
        year = movie["release_date"].split("-")[0] if movie["release_date"] else "N/A"
        recommendations.append(
            f"{movie['title']} ({year})\n"
            f"Rating: {movie['vote_average']}/10\n"
            f"Overview: {movie['overview']}\n"
        )
    
    return "Top 5 recommendations:\n\n" + "\n---\n".join(recommendations)

@mcp.tool()
async def get_trending(time_window: str) -> str:
    """获取趋势电影
    
    Args:
        time_window: 时间窗口 ('day' 或 'week')
    """
    if time_window not in ["day", "week"]:
        raise ValueError("time_window must be 'day' or 'week'")
        
    data = await fetch_from_tmdb(f"/trending/movie/{time_window}")
    
    trending = []
    for movie in data["results"][:10]:
        year = movie["release_date"].split("-")[0] if movie["release_date"] else "N/A"
        trending.append(
            f"{movie['title']} ({year})\n"
            f"Rating: {movie['vote_average']}/10\n"
            f"Overview: {movie['overview']}\n"
        )
    
    return f"Trending movies for the {time_window}:\n\n" + "\n---\n".join(trending)

if __name__ == "__main__":
    if not TMDB_API_KEY:
        raise ValueError("TMDB_API_KEY environment variable is required")
    
    mcp.run(transport='stdio')
