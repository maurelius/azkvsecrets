import os
from az_kv_secrets import AzureKeyVaultClient

def main():
    """
    Example script to demonstrate the usage of the AzureKeyVaultClient.

    This script shows how to initialize the client and retrieve secrets from
    Azure Key Vault. Before running, ensure you have:
    1. Logged in to Azure via the Azure CLI (`az login`).
    2. Set the `KEY_VAULT_NAME` environment variable to the name of your
       Azure Key Vault.
    """
    try:
        # Fetch Key Vault name from environment variable
        key_vault_name = os.environ.get("KEY_VAULT_NAME")

        if not key_vault_name:
            print("Error: The KEY_VAULT_NAME environment variable is not set.")
            print("Please set it to the name of your Azure Key Vault.")
            return

        # Define the names of the secrets you want to retrieve
        # IMPORTANT: Replace these with the actual names of your secrets
        secret_names_to_fetch = ("accessKey", "secretKey", "linkingKey")

        # Initialize the client
        print(f"Connecting to Azure Key Vault: {key_vault_name}...")
        client = AzureKeyVaultClient(key_vault_name)

        # Retrieve the secrets
        print(f"Retrieving secrets: {', '.join(secret_names_to_fetch)}...")
        accessKey, secretKey, linkingKey = client.get_secrets(*secret_names_to_fetch)
        print("Secrets retrieved successfully.")

        # Now you can use the secrets in your application
        # For example, connecting to the Tenable.io API
        # from tenable.io import TenableIO
        # print("Initializing Tenable.io client...")
        # io = TenableIO(access_key=accessKey, secret_key=secretKey)
        # print("Tenable.io client initialized successfully.")

        # For demonstration purposes, we'll just print the keys
        print("\n--- Retrieved Secrets ---")
        print(f"Access Key: {accessKey}")
        print(f"Secret Key: {secretKey}")
        print(f"Linking Key: {linkingKey}")
        print("-------------------------")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please ensure you are authenticated with Azure CLI ('az login') and have access to the Key Vault.")

if __name__ == "__main__":
    main()