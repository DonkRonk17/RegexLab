"""
Setup script for RegexLab
Interactive regex tester and pattern library
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="regexlab",
    version="1.0.0",
    description="Interactive regex tester and pattern library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Logan Smith / Metaphy LLC",
    author_email="",
    url="https://github.com/DonkRonk17/RegexLab",
    py_modules=["regexlab"],
    python_requires=">=3.7",
    install_requires=[
        # Zero dependencies - pure Python stdlib
    ],
    entry_points={
        "console_scripts": [
            "regexlab=regexlab:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="regex regular-expression pattern-matching text-processing testing developer-tools",
    project_urls={
        "Bug Reports": "https://github.com/DonkRonk17/RegexLab/issues",
        "Source": "https://github.com/DonkRonk17/RegexLab",
    },
)
