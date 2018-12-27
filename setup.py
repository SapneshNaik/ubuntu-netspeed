from setuptools import setup


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='ubuntu-netspeed',
   version='0.1',
   description='A simple Network speed indicator for Ubuntu',
   long_description=long_description, 
   license="GPL-3.0",
   author='Sapnesh Naik',
   url="http://www.kerneldev.com/",
   author_email='sapnesh@kerneldev.com',
   packages=['src'],
   # install_requires=['bar', 'greek'], #external packages as dependencies
   # scripts=[
   #          'scripts/cool',
   #          'scripts/skype',
   #         ]
)