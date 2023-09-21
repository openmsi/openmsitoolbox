" Setup for pip install of the package "

# imports
import pathlib
import setuptools

VERSION = None
VERSION_PATH = pathlib.Path(__file__).parent/"openmsitoolbox"/"version.py"
with open(VERSION_PATH,"r") as version_file:
    for line in version_file.readlines():
        if line.startswith("__version__"):
            VERSION = line.strip().split("=")[-1].strip().strip('"')
if not VERSION:
    raise RuntimeError("ERROR: Failed to find version tag!")

LONG_DESCRIPTION = ""
with open("README.md", "r") as readme:
    for il, line in enumerate(readme.readlines(), start=1):
        LONG_DESCRIPTION += line

setupkwargs = {
    "name":"openmsitoolbox",
    "packages":setuptools.find_packages(include=["openmsitoolbox*"]),
    "include_package_data":True,
    "version":VERSION,
    "description":(
        "Python utilities for OpenMSI projects "
        "Developed for Open MSI (NSF DMREF award #1921959)"
    ),
    "long_description":LONG_DESCRIPTION,
    "long_description_content_type":"text/markdown",
    "author":"OpenMSI Dev Team",
    "author_email":"openmsistream@gmail.com",
    "url":"https://github.com/openmsi/openmsitoolbox",
    "download_url":f"https://github.com/openmsi/openmsitoolbox/archive/refs/tags/v{VERSION}.tar.gz",
    "license":"GNU GPLv3",
    "python_requires":">=3.7",
    "install_requires":[],
    "extras_require":{
        "test": [
            "black",
            "packaging",
            "pyflakes",
            "pylint",
            "requests",
        ],
        "dev": [
            "twine",
        ],
    },
    "keywords":[
        "materials",
        "data_science",
    ],
    "classifiers":[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
}

setupkwargs["extras_require"]["all"] = sum(setupkwargs["extras_require"].values(), [])

setuptools.setup(**setupkwargs)
