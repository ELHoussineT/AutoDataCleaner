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
    description="Simple and automatic data cleaning in one line of code! It performs One Hot Encoding, Cleans Dirty/Empty Values, Normalizes values and Removes unwanted columns all in one line of code. Get your data ready for model training and fitting quickly.",
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