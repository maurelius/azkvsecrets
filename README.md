# azkvsecrets

Script for retrieving secrets from Azure Key Vault. I use this so I don't have to store secrets in plaintext for automating [Tenable.io](https://github.com/maurelius/tenable) things

## Usage

I typically use this to retrieve API access keys from a specific KV. Add the script to your `$PATH` or keep it in the local working directory.  
**Azure CLI is required**. You need to be signed into the correct user context that has access to the KeyVault in Azure.
    - Run `az login`

```python
import az_kv_secrets
from tenable.io import TenableIO
# Define keys to auth to API
accessKey, secretKey = azkvsecrets.get_keys()
# Bootstrap API connection
io = TenableIO(access_key=accessKey, secret_key=secretKey)
```
