import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="Serasa",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License",
    description="Serasa api",
    long_description=README,
    author="José Sales",
    author_email="jose.sales@symbit.com.br",
    install_requires=[],
)
