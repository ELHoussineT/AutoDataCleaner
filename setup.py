from setuptools import setup, find_packages

from AutoDataCleaner.AutoDataCleaner import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='AutoDataCleaner',
    version=__version__,

    url='https://github.com/sinkingtitanic/AutoDataCleaner',
    author='Elhoussine Talab',
    author_email='ofcourse7878@gmail.com',
    description="Python library to simply perform dataset cleaning on structured data stored in a Panda's DataFrame automatically with one line of code; to be used prior to training, e.g.: in data pre-processing phase in a machine learning project.",
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=[
    'pandas',
    ],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Database"
    ]
)