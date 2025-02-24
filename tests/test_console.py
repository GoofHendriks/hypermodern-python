import click.testing
import pytest
import responses

from hypermodern_python import console

@pytest.fixture
def runner():
    return click.testing.CliRunner()

def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_version(runner):
    result = runner.invoke(console.main, ["--version"])
    assert result.exit_code == 0
    assert "hypermodern-python, version 0.1.0" in result.output

@responses.activate
def test_random_summary(runner):
    # Mock the Wikipedia API response
    summary_data = {
        "title": "Python (programming language)",
        "extract": "Python is a high-level, general-purpose programming language."
    }
    responses.add(
        responses.GET,
        "https://en.wikipedia.org/api/rest_v1/page/random/summary",
        json=summary_data,
        status=200
    )

    result = runner.invoke(console.main)
    assert result.exit_code == 0
    assert "Python (programming language)" in result.output
    assert "Python is a high-level, general-purpose programming language." in result.output
