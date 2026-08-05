import binascii
import hashlib
import os
import secrets

print("==================================================")
print("🔒 Cryptographic Password Hasher & Salt Utility 🔒")
print("==================================================")
print("1. 🔑 Hash a new password")
print("2. 🔍 Verify password against stored hash")
print("3. ❌ Exit")

choice = input("Select an option (1/2/3): ").strip()

if choice == "1":
    password = input("Enter password to hash 🔑: ").strip()
    if not password:
        print("⚠️ Password cannot be empty!")
    else:
        # Generate 16-byte random salt
        salt = os.urandom(16)
        salt_hex = binascii.hexlify(salt).decode("utf-8")

        # Derive 32-byte key using PBKDF2-HMAC-SHA256 with 600,000 iterations
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations=600000,
            dklen=32
        )
        hash_hex = binascii.hexlify(key).decode("utf-8")
        stored_value = f"{salt_hex}${hash_hex}"

        print("\n✅ Password hashed successfully!")
        print(f"🧂 Salt (hex): {salt_hex}")
        print(f"🔑 Hash (hex): {hash_hex}")
        print(f"📦 Stored String: {stored_value}")

elif choice == "2":
    password_input = input("Enter password to verify 🔑: ").strip()
    stored_hash_str = input("Enter stored hash string (salt$hash) 📦: ").strip()

    if not password_input or not stored_hash_str:
        print("⚠️ Password and stored hash string cannot be empty!")
    elif "$" not in stored_hash_str:
        print("❌ Invalid stored hash format! Must be salt_hex$hash_hex")
    else:
        parts = stored_hash_str.split("$")
        salt_hex = parts[0]
        hash_hex = parts[1]

        try:
            salt = binascii.unhexlify(salt_hex.encode("utf-8"))
            derived_key = hashlib.pbkdf2_hmac(
                "sha256",
                password_input.encode("utf-8"),
                salt,
                iterations=600000,
                dklen=32
            )
            computed_hash_hex = binascii.hexlify(derived_key).decode("utf-8")

            # Constant-time comparison to prevent timing side-channel attacks
            if secrets.compare_digest(computed_hash_hex, hash_hex):
                print("\n🎉 Password verification SUCCESSFUL! Match found.")
            else:
                print("\n❌ Password verification FAILED! Incorrect password.")
        except Exception as e:
            print(f"⚠️ Error verifying password: {e}")

elif choice == "3":
    print("👋 Goodbye!")

else:
    print("⚠️ Invalid choice selected.")
