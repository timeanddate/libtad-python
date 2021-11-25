from setuptools import setup, find_packages

PACKAGES = find_packages()

setup(name='libtad',
      version='1.0',
      description='Python library for accessing Time and Date APIs',
      author='Time and Date',
      url='https://github.com/timeanddate/libtad-python/',
      packages=PACKAGES,
      )
