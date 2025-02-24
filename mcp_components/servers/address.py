from typing import Any, Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("geocode")

# Constants for Google Maps Geocoding API
GOOGLE_GEOCODE_API_BASE = "https://maps.googleapis.com/maps/api/geocode/json"
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your actual API key

async def make_google_geocode_request(address: str) -> Optional[dict[str, Any]]:
    """Make a request to the Google Geocoding API."""
    params = {
        "address": address,
        "key": API_KEY,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GOOGLE_GEOCODE_API_BASE, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error during geocoding request: {e}")
            return None

def format_geocode_result(result: dict) -> str:
    """Format a geocode result into a readable string."""
    location = result['geometry']['location']
    formatted_address = result.get('formatted_address', 'Address not available')
    return f"""
Formatted Address: {formatted_address}
Latitude: {location['lat']}
Longitude: {location['lng']}
"""

@mcp.tool()
async def get_coordinates(address: str) -> str:
    """Get coordinates (latitude and longitude) for an address.

    Args:
        address: The address you want to geocode.
    """
    data = await make_google_geocode_request(address)

    if not data or 'results' not in data or len(data['results']) == 0:
        return "Unable to fetch coordinates or no results found."

    # Format the first result
    return format_geocode_result(data['results'][0])

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')