import textwrap
import click
import requests
from . import __version__

def get_api_url(lang="en"):
    """Generate Wikipedia API URL for a given language."""
    return f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"

@click.command()
@click.option("--count", default=1, type=int, help="Number of articles to fetch (default: 1)")
@click.option("--lang", default="en", help="Wikipedia language code (e.g., 'en', 'fr', 'es')")
@click.version_option(version=__version__)
def main(count, lang):
    """The hypermodern Python project."""
    API_URL = get_api_url(lang)

    for i in range(count):
        try:
            with requests.get(API_URL) as response:
                response.raise_for_status()
                data = response.json()
        except requests.exceptions.RequestException as e:
            click.secho(f"Error: Could not fetch article - {e}", fg="red")
            return

        title = data["title"]
        extract = data["extract"]

        # Print article number if fetching multiple
        if count > 1:
            click.secho(f"Article {i + 1}/{count}", fg="yellow", bold=True)

        click.secho(title, fg="green", bold=True)
        click.echo(textwrap.fill(extract, width=80))

        # Add separator between articles (except the last one)
        if i < count - 1:
            click.echo("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    main()
