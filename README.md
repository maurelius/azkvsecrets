# azkvsecrets

Script for retrieving secrets from Azure Key Vault. I use this so I don't have to store secrets in plaintext for automating [Tenable.io](https://github.com/maurelius/tenable) things

## Usage

I typically use this to retrieve API access keys from a specific KV. Create a subdirectory named **Azure** and drop the files in there.
I'll figure out how to make it work right from `git clone` soon.
  
**Azure CLI is required**. You need to be signed into the correct user context that has access to the KeyVault in Azure.
    - Run `az login`

```python
from Azure import az_kv_secrets
from tenable.io import TenableIO
# Grab the three keys that are retrieved via get_keys()
# linkingKey is used for new scanner installation
accessKey, secretKey, linkingKey = azkvsecrets.get_keys()
# Bootstrap API connection
io = TenableIO(access_key=accessKey, secret_key=secretKey)
```
