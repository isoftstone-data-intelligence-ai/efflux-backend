from typing import Any, Optional
import httpx
from urllib.parse import quote
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("geocode")

# Constants for OpenCage Geocoder API
OPENCAGE_API_BASE = "https://api.opencagedata.com/geocode/v1/json"
API_KEY = "83a8c5d729224cddbf7cf56e4a4e8d55"  # Replace with your actual API key


async def make_opencage_request(address: str) -> Optional[dict[str, Any]]:
    """Make a request to the OpenCage Geocoder API."""
    query = quote(address)  # URL encode the address
    url = f"{OPENCAGE_API_BASE}?q={query}&key={API_KEY}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error during geocoding request: {e}")
            return None


def format_geocode_result(result: dict) -> str:
    """Format a geocode result into a readable string."""
    if not result['results']:
        return "No results found."

    location = result['results'][0]['geometry']
    components = result['results'][0]['components']
    formatted_address = result['results'][0].get('formatted', 'Address not available')
    confidence = result['results'][0].get('confidence', 'Unknown')

    output = f"""
Formatted Address: {formatted_address}
Latitude: {location['lat']}
Longitude: {location['lng']}
Confidence: {confidence}
Country: {components.get('country', 'Unknown')}
City: {components.get('city', 'Unknown')}
State: {components.get('state', 'Unknown')}
Postcode: {components.get('postcode', 'Unknown')}
Road: {components.get('road', 'Unknown')}
Road Type: {components.get('road_type', 'Unknown')}
"""
    return output


@mcp.tool()
async def get_coordinates(address: str) -> str:
    """Get coordinates (latitude and longitude) for an address.

    Args:
        address: The address you want to geocode.
    """
    data = await make_opencage_request(address)

    if not data or 'results' not in data or len(data['results']) == 0:
        return "Unable to fetch coordinates or no results found."

    # Format the first result
    return format_geocode_result(data)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')