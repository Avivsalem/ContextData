from setuptools import setup, find_packages

pkg_name = 'contextdata'

setup(name=pkg_name,
      version='0.1',
      description="a package to manage contextual data across your program, and output it to logs",
      author='Aviv Salem',
      author_email='avivsalem@gmail.com',
      url='https://github.com/Avivsalem/ContextData',
      packages=find_packages(include=[pkg_name, f'{pkg_name}.*']),
      python_requires='>=3.7',
      classifiers=[
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
      ],
      install_requires=[],
      )
