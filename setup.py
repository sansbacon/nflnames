"""
setup.py

installation script

"""

from setuptools import setup, find_packages

PACKAGE_NAME = "nflnames"


def run():
    setup(
        name=PACKAGE_NAME,
        version="0.1",
        description="python library for standardizing NFL team and player names",
        author="Eric Truett",
        author_email="eric@erictruett.com",
        license="Apache 2.0",
        packages=find_packages(),
        package_data={PACKAGE_NAME: ['data/*.*']},
        zip_safe=False,
    )


if __name__ == "__main__":
    run()
