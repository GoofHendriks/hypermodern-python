import requests


def get_api_url(lang="en"):
    """Generate Wikipedia API URL for a given language."""
    return f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"


def random_page(lang="en"):
    """Fetch a random Wikipedia page summary in the given language."""
    url = get_api_url(lang)  # ✅ Ensure it correctly uses the lang parameter
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
