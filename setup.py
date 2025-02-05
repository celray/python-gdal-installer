from setuptools import setup, find_packages
from pathlib import Path

# Read README content
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gdal-installer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'tqdm>=4.65.0',
    ],
    scripts=['scripts/install-gdal'],
    author="Celray James CHAWANDA",
    author_email="celray.chawanda@outlook.com",
    description="A tool to install GDAL wheels on Windows and wrapper for pip on Unix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="gdal, gis, installer",
    url="https://github.com/celray/python-gdal-installer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    license="MIT",
)