from setuptools import setup

VERSION='0.0.1'

setup(
        name="tinypistats",
        version=VERSION,
        author="Andrew Vojak",
        author_email="andrew.vojak@gmail.com",
        description="View Raspberry Pi stats on a tiny OLED display",
        license="Apache License, Version 2.0",
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'pi', 'raspberry', 'oled', 'stats'],
        classifiers=[
        ]
)
