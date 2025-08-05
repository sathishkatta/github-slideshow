#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README_APP.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="app-version-checker",
    version="1.0.0",
    author="System Administrator",
    author_email="admin@example.com",
    description="A tool to identify older versions of applications installed on the system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/app-version-checker",
    py_modules=["app_version_checker"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "app-version-checker=app_version_checker:main",
            "check-app-versions=app_version_checker:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)