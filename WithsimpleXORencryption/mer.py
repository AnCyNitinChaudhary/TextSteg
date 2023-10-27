import cv2
import numpy as np
from cryptography.fernet import Fernet
import base64
import os

def generate_key():
    return Fernet.generate_key()

def encrypt_text(key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode())

def decrypt_text(key, encrypted_text):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_text).decode()

key = generate_key()

image = cv2.imread('1.png')

rows, cols, _ = image.shape

plaintext = "My secret message"
encrypted_text = encrypt_text(key, plaintext)

# Assert the plaintext can fit into the image
assert len(encrypted_text)*8 <= rows*cols*3, "The plaintext is too long to fit into the image"

bit_msg = list(map(int, ''.join([bin(byte)[2:].zfill(8) for byte in encrypted_text])))

for idx, bit in enumerate(bit_msg):
    i = idx // (cols*3)        # Row index
    j = (idx // 3) % cols       # Column index
    k = idx % 3                # Colour index

    # Change pixel's least significant bit to bit
    image[i][j][k] = (image[i][j][k] & 0xFE) | bit

cv2.imwrite("encrypted_img.png", image)
print("Data hiding in image completed successfully.")

# Decrypting
encrypted_text_bits = []

for idx in range(len(encrypted_text)*8):
    i = idx // (cols*3)
    j = (idx // 3) % cols
    k = idx % 3

    encrypted_text_bits.append(image[i][j][k] & 1)

encrypted_text_bytes = [int(''.join(map(str,encrypted_text_bits[i:i+8])), 2) for i in range(0, len(encrypted_text_bits), 8)]

# Convert list of bytes into bytes-like object
encrypted_text = bytes(encrypted_text_bytes)

decrypted_text = decrypt_text(key, encrypted_text)
print("Decrypted text is: ", decrypted_text)
