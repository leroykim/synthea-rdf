from setuptools import setup

setup(
    name="synthea_rdf",
    version="0.1.1",
    description="Semantic web representation for the Synthea.",
    author="Dae-young Kim",
    author_email="leroy.kim@umbc.edu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={"Source Code": "https://github.com/leroykim/synthea_rdf"},
    license="GNU General Public License v3.0",
    packages=["synthea_rdf"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3",
        "Operating System :: OS Independent",
    ],  # Optional
    install_requires=[
        "rdflib",
        "pandas",
        "alive_progress",
    ],
)
