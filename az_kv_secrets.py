""" az_kv_secrets.py: Retrieves secrets from a defined Azure Key Vault """
""" Reference Documentation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli """
""" Azure Identity / DefaultAzureCredential Documentation: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview """
""" Currently must use Azure CLI for credentials to pass correctly """

__name__ = "az_kv_secrets.py"

import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

os.environ['KEY_VAULT_NAME'] = 'name-of-azure-keyvault'
accessKeyName = 'name-of-secret'
secretKeyName = 'name-of-secret'
credential = DefaultAzureCredential()
keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"
client = SecretClient(vault_url=KVUri, credential=credential)

def get_accessKey():
    return client.get_secret(accessKeyName).value
        
def get_secretKey():
    return client.get_secret(secretKeyName).value

def get_keys(): 
    accessKey = get_accessKey() 
    secretKey = get_secretKey() 
    return accessKey, secretKey