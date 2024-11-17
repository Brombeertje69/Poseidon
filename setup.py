# setup.py
from setuptools import setup, find_packages

setup(
    name="poseidon",
    version="0.0.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'poseidon = src.poseidon:main',  # This tells setuptools to link the CLI command to your main function
        ],
    },
)