import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mementoweb",
    version="1.0.0",
    author="Bhnauka Mahanama",
    author_email="bhanuka@lanl.gov",
    description="Memento validation toolset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mahanama94/memento-validator",
    packages=setuptools.find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "python-dateutil==2.8.1",
        "typing-extensions==3.10.0.0",
        "urllib3==1.26.5",
        "python-dotenv~=0.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)