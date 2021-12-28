from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in robothink/__init__.py
from robothink import __version__ as version

setup(
	name="robothink",
	version=version,
	description="Robothink booking software",
	author="tarunsairam2142",
	author_email="tarunsairam2142@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
