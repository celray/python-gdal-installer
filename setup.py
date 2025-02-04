from setuptools import setup, find_packages

setup(
    name="gdal-installer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    scripts=['scripts/install_gdal'],
    author="Celray James CHAWANDA",
    author_email="celray.chawanda@outlook.com",
    description="A tool to install GDAL wheels on Windows and wrapper for pip on Unix",
    long_description=open('README').read(),
    keywords="gdal, gis, installer",
    url="https://github.com/celray/python-gdal-installer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
