import requests
import json

# Base URL - adjust if your server runs on a different port
BASE_URL = "http://localhost:5000"

def test_api_without_user_agent():
    # Test single title endpoint
    title_response = requests.get(f"{BASE_URL}/api/Category:Yemen")
    print("\nTesting /api/<title> without User-Agent:")
    print(f"Status Code: {title_response.status_code}")
    print(f"Response: {title_response.json()}")

    # Test titles list endpoint
    data = {"titles": ["test_title1", "test_title2"]}
    list_response = requests.post(
        f"{BASE_URL}/api/list",
        json=data
    )
    print("\nTesting /api/list without User-Agent:")
    print(f"Status Code: {list_response.status_code}")
    print(f"Response: {list_response.json()}")

if __name__ == "__main__":
    test_api_without_user_agent()