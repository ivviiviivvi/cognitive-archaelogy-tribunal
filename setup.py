"""
Setup script for Cognitive Archaeology Tribunal
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="cognitive-tribunal",
    version="0.1.0",
    author="Cognitive Tribunal Team",
    description="Comprehensive archaeological dig tool for multi-layer cognitive ecosystems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivi374forivi/cognitive-archaelogy-tribunal",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyGithub>=2.1.1",
        "requests>=2.31.0",
        "python-dateutil>=2.8.2",
        "pathspec>=0.11.2",
        "watchdog>=3.0.0",
        "pandas>=2.0.0",
        "networkx>=3.1",
        "click>=8.1.7",
        "rich>=13.7.0",
        "pyyaml>=6.0.1",
        "xxhash>=3.4.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cognitive-tribunal=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
