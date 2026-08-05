import binascii
import hashlib
import os
import secrets
import unittest

class TestPasswordHasher(unittest.TestCase):
    def test_pbkdf2_hashing_and_verification(self):
        password = "SecurePassword123!"
        salt = os.urandom(16)
        salt_hex = binascii.hexlify(salt).decode("utf-8")

        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600000, 32)
        hash_hex = binascii.hexlify(key).decode("utf-8")
        stored = f"{salt_hex}${hash_hex}"

        # Re-derive and verify
        parts = stored.split("$")
        parsed_salt = binascii.unhexlify(parts[0].encode("utf-8"))
        derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), parsed_salt, 600000, 32)
        computed_hex = binascii.hexlify(derived).decode("utf-8")

        self.assertTrue(secrets.compare_digest(computed_hex, parts[1]))

    def test_invalid_password_fails(self):
        password = "CorrectPassword"
        wrong_password = "WrongPassword"
        salt = os.urandom(16)

        key1 = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600000, 32)
        key2 = hashlib.pbkdf2_hmac("sha256", wrong_password.encode("utf-8"), salt, 600000, 32)

        hash1 = binascii.hexlify(key1).decode("utf-8")
        hash2 = binascii.hexlify(key2).decode("utf-8")

        self.assertFalse(secrets.compare_digest(hash1, hash2))

if __name__ == "__main__":
    unittest.main()
