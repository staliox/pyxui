from setuptools import setup, find_packages
    
VERSION = "2.0.0"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="pyxui",
    version=VERSION,
    author="Staliox",
    description="An application with python that allows you to modify your xui panel",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/staliox/pyxui",
    keywords=[
        "pyxui",
        "xui",
        "xui python",
        "xui panel"
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["aiohttp>=3.8"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT"
)
