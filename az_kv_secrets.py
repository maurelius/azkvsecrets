"""
az_kv_secrets.py: Retrieves secrets from a defined Azure Key Vault
Reference Documentation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli
Azure Identity / DefaultAzureCredential Documentation: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview
"""

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

class AzureKeyVaultClient:
    """A client for retrieving secrets from Azure Key Vault."""

    def __init__(self, key_vault_name: str):
        """
        Initializes the AzureKeyVaultClient.

        Args:
            key_vault_name: The name of the Azure Key Vault.
        """
        if not key_vault_name:
            raise ValueError("Key Vault name cannot be empty.")

        self.key_vault_name = key_vault_name
        self.kv_uri = f"https://{key_vault_name}.vault.azure.net"
        self._credential = DefaultAzureCredential()
        self._client = SecretClient(vault_url=self.kv_uri, credential=self._credential)

    def get_secret(self, secret_name: str) -> str:
        """
        Retrieves a single secret from the Key Vault.

        Args:
            secret_name: The name of the secret to retrieve.

        Returns:
            The value of the secret.
        """
        if not secret_name:
            raise ValueError("Secret name cannot be empty.")
        return self._client.get_secret(secret_name).value

    def get_secrets(self, *secret_names: str) -> tuple:
        """
        Retrieves multiple secrets from the Key Vault.

        Args:
            *secret_names: A list of secret names to retrieve.

        Returns:
            A tuple containing the values of the requested secrets.
        """
        if not secret_names:
            raise ValueError("Secret names cannot be empty.")
        return tuple(self.get_secret(name) for name in secret_names)