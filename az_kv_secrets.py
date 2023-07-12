#!/usr/bin/python
""" az_kv_secrets.py: Retrieves secrets from a defined Azure Key Vault"""
""" Reference Documentation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli """
""" Azure Identity / DefaultAzureCredential Documentation: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview"""
""" Currently must use Azure CLI for credentials to pass correctly """
""" Don't forget to set az contect using AZ_SUBSCRIPTION variable """

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

os.environ['KEY_VAULT_NAME'] = 'name-of-azure-keyvault'
os.environ['AZ_RG_NAME'] = 'name-of-azure-resource-group'

keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

accessKeyName = 'name-of-secret'
secretKeyName = 'name-of-secret'

print(f"Retrieving your secrets from {keyVaultName}.")

accessKey = client.get_secret(accessKeyName)
secretKey = client.get_secret(secretKeyName)

print(f"Your access key is '{accessKey.value}'.")
print(f"Your access key is '{secretKey.value}'.")

print(" done.")