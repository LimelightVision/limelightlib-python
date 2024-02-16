from setuptools import setup, find_packages

setup(
name='limelightlib-python',
version='0.9.1',
url='https://limelightvision.io',
author='Brandon Hjelstrom',
author_email='brandon@limelightvision.io',
description='Built to interface with any Limelight Smart Camera',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
install_requires=[
    'websocket-client>=1.5',
],
python_requires='>=3.6',
)