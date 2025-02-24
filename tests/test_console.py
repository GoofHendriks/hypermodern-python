import click.testing
import pytest
from unittest.mock import MagicMock

from hypermodern_python import console

@pytest.fixture
def runner():
    return click.testing.CliRunner()

@pytest.fixture
def mock_requests_get(mocker):
    """Mock requests.get() to return a Wikipedia response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }

    mock = mocker.patch("requests.get", return_value=mock_response)
    return mock

def test_main_succeeds(runner, mock_requests_get):
    """Test if CLI runs successfully."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0

def test_version(runner):
    """Test if --version displays correctly."""
    result = runner.invoke(console.main, ["--version"])
    assert result.exit_code == 0
    assert "hypermodern-python, version 0.1.0" in result.output

def test_main_prints_title(runner, mock_requests_get):
    """Ensure Wikipedia article title appears."""
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output

def test_main_invokes_requests_get(runner, mock_requests_get):
    """Test if CLI calls requests.get()."""
    runner.invoke(console.main)
    mock_requests_get.assert_called_once()

def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    """Test if default language is English Wikipedia."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]

def test_main_uses_specified_language(runner, mock_requests_get):
    """Test that the CLI correctly uses the language option."""
    runner.invoke(console.main, ["--lang", "fr"])
    args, _ = mock_requests_get.call_args
    assert "fr.wikipedia.org" in args[0]  # ✅ Fix: Now checks correct URL

def test_main_multiple_articles(runner, mock_requests_get):
    """Test fetching multiple articles prints separators."""
    result = runner.invoke(console.main, ["--count", "2"])
    assert "-" * 40 in result.output  # ✅ Fix: Ensures separator prints correctly


def test_script_execution():
    """Test that the script runs as expected when executed."""
    import subprocess
    result = subprocess.run(
        ["python3", "-m", "hypermodern_python.console", "--help"],
        capture_output=True, text=True
    )
    assert "Usage:" in result.stdout

