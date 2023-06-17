# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from io import open

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="hrbot",
    version="0.1.0",
    author="MuoDosta",
    author_email="MuoDostaWork@gmail.com",
    description="The hrbot is a wrapper on top of the "
                "HighRise Python Bot SDK that makes it easy to create bots in HighRise.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/muodosta/hrbot",
    license="MIT License",
    packages=find_packages(),
    install_requires=["highrise-bot-sdk==23.1.0b12", "redis==4.5.5", "wheel"],
    python_requires=">=3.10,<4.0"
)
