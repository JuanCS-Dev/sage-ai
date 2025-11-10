#!/usr/bin/env python3
"""
SAGE - AI Personal Assistant - Setup Script
============================================
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("sqlite3")
        ]

setup(
    name="sage-ai",
    version="2.0.0",
    author="MAXIMUS AI",
    author_email="contact@maximus-ai.com",
    description="SAGE - Wise AI Personal Assistant with Consciousness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JuanCS-Dev/sage-ai",
    project_urls={
        "Bug Tracker": "https://github.com/JuanCS-Dev/sage-ai/issues",
        "Documentation": "https://github.com/JuanCS-Dev/sage-ai/docs",
        "Source Code": "https://github.com/JuanCS-Dev/sage-ai",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.4.0",
        ],
        "automation": [
            "playwright>=1.40.0",
            "selenium>=4.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sage=sage.cli:cli_main",
        ],
    },
    include_package_data=True,
    package_data={
        "sage": [
            "data/*.db",
            "data/*.json",
        ],
    },
    keywords=[
        "ai",
        "assistant",
        "personal-assistant",
        "automation",
        "consciousness",
        "sage",
        "claude",
        "task-management",
        "productivity",
    ],
)
