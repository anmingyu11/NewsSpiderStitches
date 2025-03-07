# -*- coding: utf-8 -*-

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

required = [
    "lxml",
    "pandas"
]

setup(
    name="NewsStiches",
    version="1.0.0",
    description="get news in data frame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AnMingYu",
    author_email="349047303@qq.com",
    url="https://github.com/anmingyu11/NewsSpiderStitches",
    packages=find_packages(exclude=["tests", "tests.*","cache","*/cache/*"]),
    python_requires=">=3.4",
    setup_requires=None,
    install_requires=required,
    extras_require={},
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
