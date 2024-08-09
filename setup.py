from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name='MLOps-project',
    version='0.1',
    packages=find_packages(),
    author='Christian',
    author_email='christianichebi@gmail.com',
    install_requires=required
)