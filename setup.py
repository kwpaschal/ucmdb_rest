# my_package/setup.py

from setuptools import setup, find_packages

setup(
    name='ucmdb_rest',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0'
    ],
    author='Keith Paschal',
    author_email='kpaschal@opentext.com',
    description='This is a collection of utilities to interact with the Universal Configuration Management Database (UCMDB) REST API',
    long_description=open('README.md').read(), # Optional: Add a README for long descriptions
    long_description_content_type='text/markdown', # If using markdown in README
    url='https://github.com/yourusername/my_package', # Optional: Link to your repository
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Example license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', # Specify minimum Python version
)