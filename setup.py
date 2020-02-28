#
# Copyright 2019 David Zerulla
#
# SPDX-License-Identifier: MIT

"""Repoload - a change request download tool."""

import re
import setuptools

version = re.search('^__VERSION__\s*=\s*"(.*)"',
                    open('repoload/repoload.py').read(),
                    re.M
                    ).group(1)

long_description = open('README.md').read()

setuptools.setup(
    name="repoload",
    version=version,
    author="Stefan Lengfeld, David Zerulla",
    author_email="contact@stefanchrist.eu, ddaze@outlook.de",
    license="MIT",
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="repoload repo gerrit",
    url="https://github.com/lengfeld/repoload",
    packages=["repoload"],
    entry_points = {
        "console_scripts": ['repoload = repoload.repoload:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    platforms='any',
)
