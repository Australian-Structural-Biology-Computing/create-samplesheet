from setuptools import setup, find_packages

setup(
    name="samplesheetutils",
    version="1.0",
    author="Nathan Glades",
    author_email="n.glades@unsw.edu.au",
    packages=find_packages(),
    description="Collection of utilities for creating and transforming samplesheets and samples",
    install_requires=["pyyaml==6.0.2"],
    
    entry_points={
        'console_scripts': [
            'create-samplesheet=samplesheetutils.binaries.create_samplesheet:create_samplesheet',
            'sample-name=samplesheetutils.binaries.sample_name:sample_name'
        ]
    }
)
