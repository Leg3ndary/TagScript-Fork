import re

from setuptools import setup

requirements = []
with open("requirements.txt", "r", encoding="utf8") as file:
    requirements = file.read().splitlines().remove("git+https://github.com/Rapptz/discord.py")

version = ""
with open("bTagScript/__init__.py", "r", encoding="utf8") as file:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', file.read(), re.MULTILINE
    ).group(1)

readme = ""
with open("README.md", "r", encoding="utf8") as file:
    readme = file.read()

packages = [
    "bTagScript",
    "bTagScript.adapter",
    "bTagScript.block",
    "bTagScript.interface"
]

setup(
    name="bTagScript",
    version=version,
    author="Leg3ndary",
    author_email="bleg3ndary@gmail.com",
    maintainer="Leg3ndary",
    maintainer_email="bleg3ndary@gmail.com",
    url="https://github.com/Leg3ndary/bTagScript",
    project_urls={
        "Documentation": "https://btagscript.readthedocs.io/",
    },
    description="An easy drop in user-provided Templating system.",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable"
        "Intended Audience :: Developers"
        "License :: Freely Distributable"
        "Natural Language :: English"
        "Operating System :: OS Independent"
        "Programming Language :: Python :: 3.8"
    ],
    keywords=["tagscript"],
    license="Creative Commons Attribution 4.0 International License",
    packages=packages,
    install_requires=requirements,
)
