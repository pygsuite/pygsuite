import nox
import os
import shutil

DEFAULT_PYTHON_VERSION = "3.8"


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""

    session.install(
        "-e",
        ".",
    )
    session.install(
        "sphinx", "alabaster", "sphinx-autodoc-typehints", "recommonmark", "sphinx-markdown-builder"
    )

    shutil.rmtree(
        os.path.join("docs", "reference"),
        ignore_errors=True,
    )
    session.run("sphinx-build", "-M", "markdown", "./docs_src", "./docs/reference")
