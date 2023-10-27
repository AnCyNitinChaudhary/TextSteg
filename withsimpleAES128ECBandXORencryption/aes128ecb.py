from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64


def encrypt_aes_ecb(shivkey, plaintext):
    shivkey = shivkey.ljust(16, b'\0')  # Ensure the shivkey is 16 bytes (128 bits)
    cipher = Cipher(algorithms.AES(shivkey), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the plaintext to be a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    encrypted_str = base64.b64encode(ciphertext).decode('utf-8')
    return encrypted_str


def decrypt_aes_ecb(shivkey, ciphertext):
    shivkey = shivkey.ljust(16, b'\0')  # Ensure the shivkey is 16 bytes (128 bits)
    cipher = Cipher(algorithms.AES(shivkey), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(
        base64.b64decode(ciphertext)) + decryptor.finalize()

    # Unpad the decrypted data
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    decrypted_str = unpadded_data.decode('utf-8')
    return decrypted_str


# Example usage
shivkey = b'Sixteen byte key'  # 128-bit shivkey
plaintext = b'This is Shivansh'

# Encrypt the plaintext
encrypted_text = encrypt_aes_ecb(shivkey, plaintext)
print("Encrypted Text:", encrypted_text)
print(type(encrypted_text))
# Decrypt the ciphertext
decrypted_text = decrypt_aes_ecb(shivkey, encrypted_text)
print("Decrypted Text:", decrypted_text)
