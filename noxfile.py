import nox

@nox.session(python=["3.13.2"])
def tests(session):
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=hypermodern_python", *session.posargs)
