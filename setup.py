import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimaprotect",
    version="1.0.1",
    author="pcourbin",
    author_email="pierre.courbin@gmail.com",
    description="Get alarm status and informations from the IMA Protect API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcourbin/pyimaprotect",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)