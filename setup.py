from setuptools import setup, find_packages

pkg_name = 'contextdata'

setup(name=pkg_name,
      version='0.1a',
      author='Aviv Salem',
      author_email='avivsalem@gmail.com',
      url='https://github.com/Avivsalem/ContextData',
      packages=find_packages(include=[pkg_name, f'{pkg_name}.*']),
      install_requires=[],
      )
