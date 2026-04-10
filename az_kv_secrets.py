""" az_kv_secrets.py: Retrieves secrets from a defined Azure Key Vault"""
""" Reference Documentation: https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli """
""" Azure Identity / DefaultAzureCredential Documentation: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview"""
""" Currently must use Azure CLI for credentials to pass correctly """
""" Don't forget to set az context using AZ_SUBSCRIPTION variable """

import os
from typing import Optional, Tuple

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.subscription import SubscriptionClient

# default names can be overridden via environment variables
DEFAULT_KEY_VAULT_NAME = os.getenv("KEY_VAULT_NAME", "your-key-vault-name")     # Replace with your default Key Vault name or set via env var
DEFAULT_AZ_RG_NAME = os.getenv("AZ_RG_NAME", "your-resource-group-name")        # Replace with your default resource group name or set via env var
ACCESS_KEY_NAME = os.getenv("TIO_ACCESS_KEY_NAME", "your-access-key-name")      # Replace with your default access key secret name or set via env var
SECRET_KEY_NAME = os.getenv("TIO_SECRET_KEY_NAME", "your-secret-key-name")      # Replace with your default secret key secret name or set via env var
LINKING_KEY_NAME = os.getenv("TIO_LINKING_KEY_NAME", "your-linking-key-name")   # Replace with your default linking key secret name or set via env var

_client: Optional[SecretClient] = None


def _validate_az_subscription(subscription_id: str):
    subscription_client = SubscriptionClient(credential=DefaultAzureCredential())
    current = next(iter(subscription_client.subscriptions.list()), None)
    if current is None:
        raise RuntimeError("Unable to read Azure subscription from current credentials.")
    if current.subscription_id.lower() != subscription_id.lower():
        raise ValueError(
            f"Current Azure CLI context subscription ID ({current.subscription_id}) does not match AZ_SUBSCRIPTION ({subscription_id}). "
            "Please set the correct context using 'az account set --subscription <subscription_id>'."
        )


def get_secret_client(
    subscription_id: Optional[str] = None,
    key_vault_name: Optional[str] = None,
    disable_subscription_validation: bool = False,
) -> SecretClient:
    """Get (and cache) a SecretClient instance for Key Vault operations."""
    global _client
    if _client is not None:
        return _client

    subscription_id = subscription_id or os.getenv("AZ_SUBSCRIPTION")
    if not subscription_id and not disable_subscription_validation:
        raise EnvironmentError("AZ_SUBSCRIPTION environment variable not set.")

    if not disable_subscription_validation:
        assert subscription_id is not None
        _validate_az_subscription(subscription_id)

    key_vault_name = key_vault_name or DEFAULT_KEY_VAULT_NAME
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    _client = SecretClient(vault_url=key_vault_uri, credential=credential)

    return _client


def get_access_key(client: Optional[SecretClient] = None) -> str:
    """Get access key value from Key Vault."""
    client = client if client is not None else get_secret_client()
    assert client is not None
    return client.get_secret(ACCESS_KEY_NAME).value


def get_secret_key(client: Optional[SecretClient] = None) -> str:
    """Get secret key value from Key Vault."""
    client = client if client is not None else get_secret_client()
    assert client is not None
    return client.get_secret(SECRET_KEY_NAME).value


def get_linking_key(client: Optional[SecretClient] = None) -> str:
    """Get linking key value from Key Vault."""
    client = client if client is not None else get_secret_client()
    assert client is not None
    return client.get_secret(LINKING_KEY_NAME).value


def get_keys(client: Optional[SecretClient] = None) -> Tuple[str, str]:
    """Get the access and secret key pair."""
    return get_access_key(client), get_secret_key(client)


def get_all_keys(client: Optional[SecretClient] = None) -> Tuple[str, str, str]:
    """Get access, secret, and linking keys."""
    return get_access_key(client), get_secret_key(client), get_linking_key(client)
