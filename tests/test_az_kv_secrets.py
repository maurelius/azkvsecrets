import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root directory to the Python path to allow importing az_kv_secrets
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from az_kv_secrets import AzureKeyVaultClient

class TestAzureKeyVaultClient(unittest.TestCase):

    @patch('az_kv_secrets.DefaultAzureCredential')
    @patch('az_kv_secrets.SecretClient')
    def test_init_success(self, mock_secret_client, mock_credential):
        """Test successful initialization of the AzureKeyVaultClient."""
        key_vault_name = "test-vault"
        client = AzureKeyVaultClient(key_vault_name)

        self.assertEqual(client.key_vault_name, key_vault_name)
        mock_credential.assert_called_once()
        mock_secret_client.assert_called_once_with(
            vault_url=f"https://{key_vault_name}.vault.azure.net",
            credential=mock_credential.return_value
        )

    def test_init_empty_vault_name_raises_error(self):
        """Test that initializing with an empty key_vault_name raises a ValueError."""
        with self.assertRaises(ValueError):
            AzureKeyVaultClient("")

    @patch('az_kv_secrets.DefaultAzureCredential')
    @patch('az_kv_secrets.SecretClient')
    def test_get_secret_success(self, mock_secret_client, mock_credential):
        """Test retrieving a single secret successfully."""
        key_vault_name = "test-vault"
        secret_name = "my-secret"
        secret_value = "my-secret-value"

        # Configure the mock SecretClient
        mock_client_instance = mock_secret_client.return_value
        mock_secret = MagicMock()
        mock_secret.value = secret_value
        mock_client_instance.get_secret.return_value = mock_secret

        client = AzureKeyVaultClient(key_vault_name)
        result = client.get_secret(secret_name)

        self.assertEqual(result, secret_value)
        mock_client_instance.get_secret.assert_called_once_with(secret_name)

    @patch('az_kv_secrets.DefaultAzureCredential')
    @patch('az_kv_secrets.SecretClient')
    def test_get_secret_empty_name_raises_error(self, mock_secret_client, mock_credential):
        """Test that get_secret with an empty secret_name raises a ValueError."""
        client = AzureKeyVaultClient("test-vault")
        with self.assertRaises(ValueError):
            client.get_secret("")

    @patch('az_kv_secrets.DefaultAzureCredential')
    @patch('az_kv_secrets.SecretClient')
    def test_get_secrets_success(self, mock_secret_client, mock_credential):
        """Test retrieving multiple secrets successfully."""
        key_vault_name = "test-vault"
        secrets = {
            "secret1": "value1",
            "secret2": "value2"
        }

        # Configure the mock to return different values for different calls
        def get_secret_side_effect(name):
            mock_secret = MagicMock()
            mock_secret.value = secrets[name]
            return mock_secret

        mock_client_instance = mock_secret_client.return_value
        mock_client_instance.get_secret.side_effect = get_secret_side_effect

        client = AzureKeyVaultClient(key_vault_name)
        result = client.get_secrets("secret1", "secret2")

        self.assertEqual(result, ("value1", "value2"))
        self.assertEqual(mock_client_instance.get_secret.call_count, 2)

    @patch('az_kv_secrets.DefaultAzureCredential')
    @patch('az_kv_secrets.SecretClient')
    def test_get_secrets_empty_name_raises_error(self, mock_secret_client, mock_credential):
        """Test that get_secrets with no arguments raises a ValueError."""
        client = AzureKeyVaultClient("test-vault")
        with self.assertRaises(ValueError):
            client.get_secrets()

if __name__ == '__main__':
    unittest.main()