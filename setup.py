from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='discord.py-lifesaver',
    version='0.0.0',
    keywords='discord discord.py',
    description=('Lifesaver is an extremely opinionated bot foundation that provides a bunch of '
                 'handy utilities to the average Discord.py developer.'),
    long_description=long_description,
    url='https://github.com/slice/discord.py-lifesaver',
    author='Ryan Emmanuel Tongol',
    author_email='ryaneft@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha', 'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    packages=['lifesaver', 'lifesaver.bot', 'lifesaver.utils', 'lifesaver.bot.exts'],
    dependency_links=[
        'git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py',
        'ruamel.yaml'
    ])
