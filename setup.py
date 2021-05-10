import os 
import sys
from setuptools import setup, find_packages

version = '0.0.1'
binary_names = ['pypdf']
pkg_name = 'pypdf'
repo_name = 'pypdf-lib'

root = os.path.abspath(os.path.dirname(__file__))
packages = find_packages(include=[pkg_name, "{}.*".format(pkg_name)])


deps = {
    'main': [
        'file-io',
    ],
}

with open(os.path.join(root, 'README.md'), 'rb') as readme:
    long_description = readme.read().decode('utf-8')


root = os.path.abspath(os.path.dirname(__file__))

setup(
    name=repo_name,
    version=version,
    description=pkg_name,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tri Songz',
    author_email='ts@growthengineai.com',
    url=f'http://github.com/trisongz/{repo_name}',
    python_requires='>3.6',
    install_requires=deps['main'],
    packages=packages,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
    ],
)