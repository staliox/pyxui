from setuptools import setup, find_packages
    
VERSION = "1.0.1"

with open("README.md", "r") as f:
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
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT"
)
