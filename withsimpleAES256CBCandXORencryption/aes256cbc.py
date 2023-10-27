from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
import os


def encrypt_aes_cbc(shivkey, plaintext):
    shivkey = shivkey.ljust(32, b'\0')  # Ensure the shivkey is 32 bytes (256 bits)
    iv = os.urandom(16)  # Generate a random 16-byte IV
    cipher = Cipher(algorithms.AES(shivkey), modes.CBC(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_str = base64.b64encode(iv + ciphertext).decode('utf-8')
    return encrypted_str


def decrypt_aes_cbc(shivkey, ciphertext):
    shivkey = shivkey.ljust(32, b'\0')  # Ensure the shivkey is 32 bytes (256 bits)

    # Decode the base64-encoded ciphertext
    ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
    iv = ciphertext[:16]  # Extract the IV from the ciphertext
    ciphertext = ciphertext[16:]  # Extract the actual ciphertext

    cipher = Cipher(algorithms.AES(shivkey), modes.CBC(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    decrypted_str = unpadded_data.decode('utf-8')
    return decrypted_str


# Example usage
shivkey = b'Thirty-two byte key for AES-256'  # 256-bit shivkey
plaintext = b'This is a secret message for AES-256 encryption in CBC mode.'

# Encrypt the plaintext
encrypted_text = encrypt_aes_cbc(shivkey, plaintext)
print("Encrypted Text:", encrypted_text)
print(type(encrypted_text))
# Decrypt the ciphertext
decrypted_text = decrypt_aes_cbc(shivkey, encrypted_text)
print("Decrypted Text:", decrypted_text)
