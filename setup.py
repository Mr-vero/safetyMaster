#!/usr/bin/env python3
"""
Setup script for SafetyMaster Pro
Real-time safety equipment detection system
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="safetymaster-pro",
    version="1.0.0",
    author="SafetyMaster Team",
    author_email="support@safetymaster.pro",
    description="Real-time AI-powered safety equipment detection system",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/safetymaster/safetymaster-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={
        "": ["*.pt", "*.html", "*.css", "*.js", "*.md"],
    },
    entry_points={
        "console_scripts": [
            "safetymaster=web_interface:main",
            "safetymaster-test=high_fps_test:test_high_fps",
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
        "gpu": [
            "torch>=1.9.0+cu111",
            "torchvision>=0.10.0+cu111",
        ],
    },
    zip_safe=False,
) 