from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="diffeq-lib",
    version="0.1.0",
    author="KBTU Python II Team",
    author_email="team@example.com",
    description="Python library for differential equations solving and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Squmon/KBTU-python-2-final",
    
    # CRITICAL: List packages explicitly for your structure
    packages=["diffeq", "diffeq.utils", "diffeq.plotting"],
    
    # Tell setuptools these are Python packages
    package_dir={
        "diffeq": "diffeq",
        "diffeq.utils": "diffeq/utils",
        "diffeq.plotting": "diffeq/plotting"
    },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
)