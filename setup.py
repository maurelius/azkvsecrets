from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="azkvsecrets",
    version="2.0.0",
    author="maurelius",
    description="A simple module for retrieving secrets from Azure Key Vault",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maurelius/azkvsecrets",  # Replace with your repo URL
    py_modules=["az_kv_secrets"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Assuming MIT License
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
    ],
    python_requires='>=3.7',
    install_requires=[
        "azure-identity>=1.12.0",
        "azure-keyvault-secrets>=4.7.0",
    ],
)