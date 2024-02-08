"""A module that contains the Secure class
"""

from bcrypt import gensalt, hashpw, checkpw
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class Secure:
    """A class that contain security function needed in application."""

    def hash_password(self, password: str, salt: bytes | None = None) -> bytes:
        """Return hash of the password that entered

        Args:
            password (str): Password to hash
            salt (bytes | None, optional): salt to hash. Defaults to None.

        Returns:
            bytes: Hash of the password
        """
        if salt is None:
            hardness = 15
            salt = gensalt(hardness)
        password_hash = hashpw(password.encode(), salt)
        return password_hash

    def check_password(self, password: str, hash_password: bytes) -> bool:
        """Check if the password match with the hash.

        Args:
            password (str): The password to check
            hash_password (bytes): The hash to check

        Returns:
            bool: True if matched and false if not matched
        """
        return checkpw(password.encode(), hash_password)

    def generate_encryption_key(
        self,
        password: str,
        salt: bytes | None = None,
    ) -> bytes:
        """A method that generate encryption key base on a password.

        Args:
            password (str): The base password to generate key.
            salt (bytes | None, optional): The salt to generate key. Defaults to None.

        Returns:
            Tuple: A tuple that contain the encryption key and the salt.
        """
        if salt is None:
            salt = get_random_bytes(32)
        key = PBKDF2(password, salt, dkLen=32)
        return key, salt

    def encrypt_data(self, data: str, key: bytes) -> (bytes, bytes):
        """A method that encrypt data with a specific encryption key.

        Args:
            data (str): The data to encrypt.
            key (bytes): The key of encryption.

        Returns:
            Tuple: A tuple that contain The encrypted data and initialization vector.
        """
        cipher = AES.new(key, AES.MODE_CBC)
        cipher_data = cipher.encrypt(pad(data.encode(), AES.block_size))
        initialization_vector = cipher.iv
        return cipher_data, initialization_vector

    def decrypt_data(
        self,
        cipher_data: bytes,
        key: bytes,
        initialization_vector: bytes,
    ) -> str:
        """A method that decrypt the data with a specific encryption key.

        Args:
            cipher_data (bytes): The data to decrypt.
            key (bytes): The key of decryption.
            initialization_vector (bytes): initialization vector to make cipher.

        Returns:
            str: The original data that decrypted.
        """
        cipher = AES.new(key, AES.MODE_CBC, iv=initialization_vector)
        decrypted_data = cipher.decrypt(cipher_data)
        original_data = unpad(decrypted_data, AES.block_size)
        return original_data.decode()
