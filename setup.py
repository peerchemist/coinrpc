import re
from pathlib import Path
from typing import List

from setuptools import setup


def get_version(package: str) -> str:
    """
    Extract package version, located in the `src/package/__version__.py`.
    """
    version = Path("src", package, "__version__.py").read_text()
    pattern = r"__version__ = ['\"]([^'\"]+)['\"]"
    return re.match(pattern, version).group(1)  # type: ignore


def get_requirements(req_file: str) -> List[str]:
    """
    Extract requirements from provided file.
    """
    req_path = Path(req_file)
    requirements = req_path.read_text().split("\n") if req_path.exists() else []
    return requirements


def get_long_description(readme_file: str) -> str:
    """
    Extract README from provided file.
    """
    readme_path = Path(readme_file)
    long_description = (
        readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    )
    return long_description


setup(
    name="coinrpc",
    python_requires=">=3.8",
    version=get_version("coinrpc"),
    description="Lightweight JSON-RPC Python asynchronous client for Satoshi clients.",
    long_description=get_long_description("README.md"),
    long_description_content_type="text/markdown",
    keywords="peercoin bitcoin async json-rpc",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="https://github.com/peercoin/coinrpc",
    author="Peerchemist",
    author_email="peerchemist@protonmail.ch",
    package_dir={"": "src"},
    packages=["coinrpc"],
    install_requires=get_requirements("requirements.txt"),
)
