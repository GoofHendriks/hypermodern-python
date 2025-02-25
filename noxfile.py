import nox
import tempfile

nox.options.sessions = "lint", "safety", "tests"

@nox.session(python=["3.13.2"])
def tests(session):
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", external=True)
    install_with_constraints(session, "pytest", "pytest-cov", "pytest-mock", "coverage[toml]")
    session.run("pytest", *args)


locations = "src", "tests", "noxfile.py"


@nox.session(python=["3.13.2"])
def lint(session):
    args = session.posargs or locations
    install_with_constraints(session, "flake8", "flake8-bandit", "flake8-black", "flake8-bugbear", "flake8-import-order")
    session.run("flake8", *args)


@nox.session(python="3.13.2")
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python="3.13.2")
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "scan", f"--file={requirements.name}", "--full-report")


import nox
import tempfile
import os

def install_with_constraints(session, *args, **kwargs):
    """Install dependencies using Poetry's constraints file."""
    requirements_path = "requirements.txt"

    try:
        # Try to export requirements from Poetry
        with tempfile.NamedTemporaryFile(delete=False) as requirements:
            session.run(
                "poetry",
                "export",
                "--dev",
                "--format=requirements.txt",
                f"--output={requirements.name}",
                external=True,
                silent=True,  # Prevent excessive logging
            )
            requirements_path = requirements.name
    except:
        session.log("⚠️ Failed to export dependencies with Poetry. Using existing requirements.txt.")

    # Install dependencies with constraints
    session.install(f"--constraint={requirements_path}", *args, **kwargs)

