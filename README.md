# azkvsecrets

Script for retrieving secrets from Azure Key Vault

## Usage

I typically use this to retrieve API access keys from a specific KV. Add the script to your $PATH or keep it in the local working directory.

```python
import azkvsecrets
from tenable.io import TenableIO
# Define keys to auth to API
accessKey, secretKey = azkvsecrets.get_keys()
# Bootstrap API connection
io = TenableIO(access_key=accessKey, secret_key=secretKey)
```
