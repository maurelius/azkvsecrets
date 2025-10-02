# Azure Key Vault Secrets (`azkvsecrets`)

A simple and reusable Python module for retrieving secrets from Azure Key Vault. This module is designed to be a secure and efficient way to manage secrets for applications, such as automating tasks with [Tenable.io](https://github.com/maurelius/tenable).

## Features

-   **Simple Interface**: A clean, class-based design that's easy to integrate.
-   **Secure**: Leverages `DefaultAzureCredential` to authenticate using managed identities, environment variables, or the Azure CLI. No more plaintext secrets.
-   **Flexible**: Easily retrieve one or multiple secrets with dedicated methods.
-   **Drop-in Ready**: Installable as a standard Python package.

## Requirements

-   Python 3.7+
-   An Azure subscription with a Key Vault instance.
-   **Azure CLI**: You must be authenticated with the Azure CLI for the script to work in a local development environment. Run the following command to log in:
    ```bash
    az login
    ```

## Installation

You can install the required packages using pip:

```bash
pip install azure-keyvault-secrets azure-identity
```

To use this module in your projects, you can install it directly from the source:

```bash
pip install .
```

## Usage

To use the `azkvsecrets` module, you first need to set an environment variable with the name of your Azure Key Vault.

```bash
export KEY_VAULT_NAME="your-key-vault-name"
```

Then, you can use the `AzureKeyVaultClient` class in your Python scripts to retrieve secrets.

### Example

Here's how to retrieve API keys for the Tenable.io API:

```python
import os
from az_kv_secrets import AzureKeyVaultClient
from tenable.io import TenableIO

def main():
    try:
        # 1. Get the Key Vault name from an environment variable
        key_vault_name = os.environ.get("KEY_VAULT_NAME")
        if not key_vault_name:
            raise ValueError("The KEY_VAULT_NAME environment variable is not set.")

        # 2. Initialize the Azure Key Vault client
        kv_client = AzureKeyVaultClient(key_vault_name)

        # 3. Define the names of the secrets to retrieve
        access_key_name = "tio-access-key"  # Replace with your secret name
        secret_key_name = "tio-secret-key"  # Replace with your secret name

        print("Retrieving secrets from Azure Key Vault...")

        # 4. Retrieve multiple secrets at once
        accessKey, secretKey = kv_client.get_secrets(access_key_name, secret_key_name)

        print("Secrets retrieved successfully.")

        # 5. Use the secrets to initialize the Tenable.io client
        # print("Initializing Tenable.io client...")
        # io = TenableIO(access_key=accessKey, secret_key=secretKey)
        # print("Tenable.io client initialized.")

        # For demonstration, we'll just print the keys
        print("\n--- Retrieved Secrets ---")
        print(f"Access Key: {accessKey}")
        print(f"Secret Key: {secretKey}")
        print("-------------------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

### Retrieving a Single Secret

If you only need one secret, you can use the `get_secret` method:

```python
# ... (inside the try block)
access_key = kv_client.get_secret("tio-access-key")
print(f"Retrieved Access Key: {access_key}")
```