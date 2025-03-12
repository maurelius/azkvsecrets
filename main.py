import sys
import os

# Assuming your module is in the 'Azure' directory
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Azure'))
sys.path.append(module_path)

from Azure import get_keys  # Correct import

accessKey, secretKey, linkingKey = get_keys() # Correct function call

print(f"Access Key: {accessKey}")
print(f"Secret Key: {secretKey}")
print(f"Linking Key: {linkingKey}")