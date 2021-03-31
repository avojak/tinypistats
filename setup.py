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
        install_requires=[
            'adafruit-circuitpython-ssd1306>=2.11.2',
            'gpiozero>=1.6.2',
            'Pillow>=5.4.1'
            'psutil>=5.8.0'
        ],
        keywords=['python', 'pi', 'raspberry', 'oled', 'stats'],
        classifiers=[
        ]
)
