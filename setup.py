from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="solring",
        version="0.0.1",
        author="Hakan Ozler",
        author_email="ozler.hakan@gmail.com",
        description="a solr import tool to save data from solr to local storage",
        long_description=long_description,
        long_description_content_type="text/plain; charset=UTF-8",
        url="https://github.com/ozlerhakan/solring",
        project_urls={
            "Bug Tracker": "https://github.com/ozlerhakan/solring/issues",
        },
        license="MIT",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        python_requires=">=3.7",
        keywords=["python", 'solr', 'pandas', 'import'],
        install_requires=[
            'solrpy==1.0.0',
            'pandas>=1.3.4'
        ],
        platforms=["linux", "unix"],
        entry_points={
            "console_scripts": [
                "solring=solring.Solring:main"
            ],
        }
    )
