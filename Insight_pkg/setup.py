import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Insight_pkg",
    version="0.0.1",
    author="Dr. Dirk Colbry",
    author_email="colbrydi@msu.edu",
    description="Package of image analysis projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/buckl113/Insight",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)