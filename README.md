# Azure Key Vault Secrets Helper

A Python module for retrieving secrets from Azure Key Vault, specifically designed for managing API credentials (e.g., Tenable.io access/secret keys) in a secure, centralized manner.

## What It Does

This module provides a simple, cached interface to fetch secrets from an Azure Key Vault instance without exposing credentials in code or environment variables. It handles:

- Azure authentication via `DefaultAzureCredential` (supports MSI, local Azure CLI, and managed identities)
- Subscription validation to ensure you're accessing the correct vault
- Lazy loading and caching of the SecretClient to minimize authentication overhead
- Convenience functions for retrieving specific API keys (access key, secret key, linking key)

## Installation

### Prerequisites

- Python 3.8+
- Azure CLI installed and authenticated
- Access to the Azure subscription and Key Vault

### Setup

1. **Install Azure SDK dependencies:**

   Using `requirements.txt`:

   ```bash
   cd /path/to/azkvsecrets
   pip install -r requirements.txt
   ```

   Or manually:

   ```bash
   pip install azure-identity azure-keyvault-secrets azure-mgmt-subscription
   ```

2. **Set Azure context:**

   ```bash
   az login
   az account set --subscription <your-subscription-id>
   ```

3. **Add to your project:**

   For local Python projects, you can either:
   - Copy the `azkvsecrets` folder to your project directory
   - Add the parent directory to `sys.path`
   - Install as an editable package:

     ```bash
     cd /path/to/azkvsecrets
     pip install -e .
     ```

### Environment Variables

Configure these optional environment variables (defaults provided):

```bash
export AZ_SUBSCRIPTION=<your-subscription-id>                        # Required: Azure subscription ID
export KEY_VAULT_NAME=<your-key-vault-name>                          # Default Key Vault name
export AZ_RG_NAME=<your-resource-group-name>                         # Default resource group
export TIO_ACCESS_KEY_NAME=<your-access-key-name>                    # Secret name for access key
export TIO_SECRET_KEY_NAME=<your-secret-key-name>                    # Secret name for secret key
export TIO_LINKING_KEY_NAME=<your-linking-key-name>                  # Secret name for linking key
```

## Usage

### Basic Example: Retrieve Tenable.io Keys

```python
import os
import logging
import az_kv_secrets as azkv
from tenable.io import TenableIO

# Set subscription ID
# Despite being set above, we can also set it here to ensure it's available for the module
os.environ['AZ_SUBSCRIPTION'] = '<your-subscription-id>'

# Retrieve keys from Azure Key Vault
tenable_keys = azkv.get_keys()
if tenable_keys and all(t is not None for t in tenable_keys):
    os.environ['TIO_ACCESS_KEY'] = tenable_keys[0] if tenable_keys[0] is not None else ""
    os.environ['TIO_SECRET_KEY'] = tenable_keys[1] if tenable_keys[1] is not None else ""
else:
    logging.error("Tenable keys could not be retrieved from Azure Key Vault.")
    exit(1)

# Initialize Tenable.io client
io = TenableIO()
```

### Retrieve Individual Keys

```python
import az_kv_secrets as azkv

# Get individual keys
access_key = azkv.get_access_key()
secret_key = azkv.get_secret_key()
linking_key = azkv.get_linking_key()
```

### Get All Keys at Once

```python
import az_kv_secrets as azkv

access_key, secret_key, linking_key = azkv.get_all_keys()
```

### Manual Client Management

```python
import az_kv_secrets as azkv

# Create client once and reuse
client = azkv.get_secret_client()
key1 = azkv.get_access_key(client)
key2 = azkv.get_secret_key(client)  # Reuses same client, no re-auth
```

## Common Use Cases

### Setting Environment Variables from Vault

```python
import os
import logging
import az_kv_secrets as azkv

# Set subscription ID
# Despite being set above, we can also set it here to ensure it's available for the module
os.environ['AZ_SUBSCRIPTION'] = '<your-subscription-id>'

# Retrieve keys from Azure Key Vault and set as env vars
tenable_keys = azkv.get_keys()
if tenable_keys and all(t is not None for t in tenable_keys):
    os.environ['TIO_ACCESS_KEY'] = tenable_keys[0] if tenable_keys[0] is not None else ""
    os.environ['TIO_SECRET_KEY'] = tenable_keys[1] if tenable_keys[1] is not None else ""
else:
    logging.error("Tenable keys could not be retrieved from Azure Key Vault.")
    exit(1)

# Now use the environment variables with any API client
print(f"Access key loaded: {os.environ.get('TIO_ACCESS_KEY', '')[:8]}...")
print(f"Secret key loaded: {os.environ.get('TIO_SECRET_KEY', '')[:8]}...")
```

### Complete Script Example

```python
#!/usr/bin/env python3
import os
import sys
import logging
import az_kv_secrets as azkv
from tenable.io import TenableIO

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set subscription ID
# Despite being set above, we can also set it here to ensure it's available for the module
os.environ['AZ_SUBSCRIPTION'] = '<your-subscription-id>'

try:
    # Retrieve keys from Azure Key Vault
    tenable_keys = azkv.get_keys()
    if tenable_keys and all(t is not None for t in tenable_keys):
        os.environ['TIO_ACCESS_KEY'] = tenable_keys[0] if tenable_keys[0] is not None else ""
        os.environ['TIO_SECRET_KEY'] = tenable_keys[1] if tenable_keys[1] is not None else ""
    else:
        logging.error("Tenable keys could not be retrieved from Azure Key Vault.")
        sys.exit(1)
    
    # Initialize Tenable.io client
    io = TenableIO()
    
    # Fetch and display scans
    scans = io.scans.list()
    print(f"Found {len(scans)} scans:")
    for scan in scans:
        print(f"  - {scan['name']} (Status: {scan['status']})")

except Exception as e:
    logging.error(f"Error: {e}", exc_info=True)
    sys.exit(1)
```

## Troubleshooting

### `AZ_SUBSCRIPTION environment variable not set`

Set the subscription environment variable:

```bash
export AZ_SUBSCRIPTION=<your-subscription-id>
```

### `Current Azure CLI context subscription ID does not match`

Ensure you're in the correct Azure subscription:

```bash
az account set --subscription <your-subscription-id>
```

### `Unable to authenticate`

Ensure Azure CLI is installed and authenticated:

```bash
az login
az account show
```

### `Secret not found in Key Vault`

Verify the secret names exist in your Key Vault and match the environment variable names:

```bash
az keyvault secret list --vault-name <your-key-vault-name>
```

## API Reference

### Functions

- **`get_secret_client(subscription_id=None, key_vault_name=None, disable_subscription_validation=False)`**
  
  Returns a cached Azure KeyVault SecretClient instance.

- **`get_access_key(client=None)`**
  
  Returns the Tenable.io access key from Key Vault.

- **`get_secret_key(client=None)`**
  
  Returns the Tenable.io secret key from Key Vault.

- **`get_linking_key(client=None)`**
  
  Returns the Tenable.io linking key from Key Vault.

- **`get_keys(client=None)`**
  
  Returns a tuple of (access_key, secret_key).

- **`get_all_keys(client=None)`**
  
  Returns a tuple of (access_key, secret_key, linking_key).

## References

- [Azure Key Vault Python SDK](https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python?tabs=azure-cli)
- [Azure Identity Authentication](https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview)
- [pyTenable Documentation](https://pytenable.readthedocs.io/)
