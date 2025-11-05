"""Setup script for DSA practice repository."""

from setuptools import setup, find_packages

setup(
    name="dsa-practice",
    version="0.1.0",
    description="Data Structures and Algorithms practice problems",
    packages=find_packages(exclude=["tests", "templates"]),
    python_requires=">=3.8",
    install_requires=[],
)
