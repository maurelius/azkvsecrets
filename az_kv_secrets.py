""" az_kv_secrets.py: Retrieves secrets from a defined Azure Key Vault """
""" Reference Documentation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli """
""" Azure Identity / DefaultAzureCredential Documentation: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview """
""" Currently must use Azure CLI for credentials to pass correctly """

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Define the Key Vault and store it as an environment variable
os.environ['KEY_VAULT_NAME'] = 'name-of-azure-keyvault'
# Define the names of keys you want to grab secrets from
accessKeyName = 'name-of-secret'
secretKeyName = 'name-of-secret'
linkingKeyName = 'name-of-linking-key'
# Set up creds from using azcli
credential = DefaultAzureCredential()
# Store your KV name
keyVaultName = os.environ["KEY_VAULT_NAME"]
# Define the URI to access the KV
KVUri = f"https://{keyVaultName}.vault.azure.net"
# Set up a client to auth to your Azure Key Vault
client = SecretClient(vault_url=KVUri, credential=credential)

# Function to grab an accessKey based on name and return its value
def get_accessKey():
    return client.get_secret(accessKeyName).value
# Function to grab a secretKey based on name and return its value        
def get_secretKey():
    return client.get_secret(secretKeyName).value
# Function to grab a linkingKey based on name and return its value
def get_linkingKey():
    return client.get_secret(linkingKeyName).value
# Function to grab all the keys, assign to them, and return the stored values
def get_keys(): 
    accessKey = get_accessKey() 
    secretKey = get_secretKey() 
    linkingKey = get_linkingKey()
    return accessKey, secretKey, linkingKey