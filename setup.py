from setuptools import setup, find_packages
from pathlib import Path

pkg_name = 'contextdata'
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name=pkg_name,
      version='0.1.4',
      description="a package to manage contextual data across your program, and output it to logs",
      long_description=long_description,
      long_description_content_type='text/markdown',
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
      include_package_data=True,
      )
