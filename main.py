import sys
import os

# Assuming your module is in the 'Azure' directory
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Azure'))
sys.path.append(module_path) 

from az_kv_secrets import get_keys

api_key = get_keys("KeyVaultName", "api_key")
print(api_key) 