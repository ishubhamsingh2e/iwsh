import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# with open('requirements.txt', encoding="utf-16") as rq:
#     required = rq.read().splitlines()

setuptools.setup(
    name="iwsh",
    version="0.0.1",
    author="Shubham singh, Ayan Ambesh",
    author_email="ishubhamsingh@gmail.com",
    description="package for intracting with hardware and software",
    # install_requires=required,
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
)
