from setuptools import setup


setup(
    name='race-pi',
    version='0.1',
    description='Raspberry Pi Motorsport Telemetry',
    author='Robert Wallhead',
    author_email='robert@thisismyrobot.com',
    url='http://thisismyrobot.com/',
    packages=[
        'race',
        'race/pi',
    ],
    install_requires=[
        'pyserial',
        'spidev',
    ],
)
