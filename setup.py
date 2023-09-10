import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threadscrape",
    version="1.0.0",
    author="aditya76-git",
    author_email="cdr.aditya.76@gmail.com",
    description="ThreadScrape - Threads.net WEB API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aditya76-git/threadscrape-threads-net-web-api",
    project_urls={
        "Tracker": "https://github.com/aditya76-git/threadscrape-threads-net-web-api/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)