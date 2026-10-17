#These files treat your project as a standalone Python package. This allows you to import custom modules
#  (e.g., from src.components import data_ingestion) across different files without encountering path errors.
from setuptools import setup
from setuptools import find_packages

setup(
    name='src',
    version='0.0.1',
    author='Uttam',
    author_email="kputtam7@gmail.com",
    packages=find_packages()
)