from setuptools import find_packages, setup

setup(
    name='ucmdb_rest',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'requests~=2.31.0'
    ],
    author='Keith Paschal',
    author_email='kw.paschal@gmail.com',
    description='A collection of utilities to interact with the Universal Configuration Management Database (UCMDB) REST API',  # noqa: E501
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