from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

VERSION='1.0.0'

setup(
        name="tinypistats",
        version=VERSION,
        author="Andrew Vojak",
        author_email="andrew.vojak@gmail.com",
        description="View Raspberry Pi stats on a tiny OLED display",
        long_description=long_description,
        license="Apache License, Version 2.0",
        packages=find_packages(),
        install_requires=[
            'adafruit-circuitpython-ssd1306>=2.11.2',
            'gpiozero>=1.6.2',
            'Pillow>=5.4.1',
            'psutil>=5.8.0'
        ],
        keywords=['python', 'pi', 'raspberry', 'oled', 'stats'],
        classifiers=[
            'Programming Language :: Python :: 3'
            'Programming Language :: Python :: 3.6'
            'Programming Language :: Python :: 3.7'
            'Programming Language :: Python :: 3.8'
            'Programming Language :: Python :: 3.9'
            'Programming Language :: Python :: 3 :: Only'
        ],
        python_requires='>=3.6, <4',
        project_urls={
            'Bug Reports': 'https://github.com/avojak/tinypistats/issues',
            'Source': 'https://github.com/avojak/tinypistats'
        }
)
