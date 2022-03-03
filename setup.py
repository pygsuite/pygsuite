# type: ignore
import ast
import re
import sys

import setuptools

_version_re = re.compile(r"__version__\s+=\s+(.*)")
with open("pygsuite/__init__.py", "rb") as f:
    _match = _version_re.search(f.read().decode("utf-8"))
    if _match is None:
        print("No version found")
        raise SystemExit(1)
    version = str(ast.literal_eval(_match.group(1)))

# for windows machines, we need to update the python-magic requirement
# python-magic-bin should be installed on windows, which includes DLLs
# reference: https://github.com/ahupp/python-magic#installation
windows = sys.platform in ["win32", "cygwin"]

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f.readlines()]
    if windows:
        install_requires[install_requires.index("python-magic")] = "python-magic-bin"

setuptools.setup(
    name="pygsuite",
    version=version,
    url="https://github.com/greenmtnboy/pygsuite",
    author="greenmtnboy",
    author_email="ethan.dickinson@gmail.com",
    description="Package for working with the Gsuite set of tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[install_requires],
    extras_require={"images": ["google-cloud-storage", "pyopenssl"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
