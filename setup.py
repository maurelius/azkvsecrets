from setuptools import setup

setup(
    name="az_kv_secrets", 
    version="1.1",  # Update version as needed
    description="A module for accessing secrets from Azure Key Vault",
    author="maurelius",
    packages=["az_kv_secrets"], 
    install_requires=[
        "azure-identity",  # External library dependencies
        "azure-keyvault-secrets"
    ],
)