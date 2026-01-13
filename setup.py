from setuptools import find_packages, setup

setup(
    name='ucmdb_rest',
    version='2.0.1',  # Bumped for the new OO architecture and Enums
    packages=find_packages(),
    install_requires=[
        'requests~=2.31.0'  # Compatible release pinning
    ],
    author='Keith Paschal',
    author_email='kw.paschal@gmail.com',
    description='A collection of utilities to interact with the Universal Configuration Management Database (UCMDB) REST API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kwpaschal/ucmdb_rest',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)