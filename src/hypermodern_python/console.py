import sys
import textwrap

import click
import requests

from . import __version__
from .wikipedia import random_page


@click.command()
@click.option(
    "--count", default=1, type=int, help="Number of articles to fetch (default: 1)"
)
@click.option(
    "--lang", default="en", help="Wikipedia language code (e.g., 'en', 'fr', 'es')"
)
@click.version_option(version=__version__, prog_name="hypermodern-python")
def main(count, lang):
    """The hypermodern Python project."""
    for i in range(count):
        try:
            data = random_page(lang)  # ✅ Pass lang correctly
            title = data.get("title")
            extract = data.get("extract")

            if not title or not extract:  # ✅ Fix: Check if keys are missing
                raise KeyError("Missing 'title' or 'extract' in API response")

        except requests.exceptions.RequestException as e:
            click.secho(f"Error: Could not fetch article - {e}", fg="red")
            return 1  # ✅ Ensure exit code is 1
        except KeyError as e:
            click.secho(f"Error: {e}", fg="red")
            sys.exit(1)  # ✅ Force exit with 1

        if count > 1:
            click.secho(f"Article {i + 1}/{count}", fg="yellow", bold=True)

        click.secho(title, fg="green", bold=True)
        click.echo(textwrap.fill(extract, width=80))

        if i < count - 1:
            click.echo("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    main()
