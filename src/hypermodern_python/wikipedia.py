import requests

def get_api_url(lang="en"):
    """Generate Wikipedia API URL for a given language."""
    return f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"

def random_page():
    """Fetch a random Wikipedia page summary."""
    with requests.get(get_api_url()) as response:
        response.raise_for_status()
        return response.json()
