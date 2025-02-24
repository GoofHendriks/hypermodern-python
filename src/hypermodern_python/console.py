import textwrap
import click
import requests

from . import __version__
from .wikipedia import random_page, get_api_url  # Import both functions

@click.command()
@click.option("--count", default=1, type=int, help="Number of articles to fetch (default: 1)")
@click.option("--lang", default="en", help="Wikipedia language code (e.g., 'en', 'fr', 'es')")
@click.version_option(version=__version__, prog_name="hypermodern-python")
def main(count, lang):
    """The hypermodern Python project."""
    for i in range(count):
        # Update API_URL dynamically in wikipedia.py via get_api_url
        try:
            data = random_page()
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
