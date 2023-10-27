import cv2
import numpy as np
from cryptography.fernet import Fernet
import base64

def generate_key():
    return Fernet.generate_key()

def encrypt_text(key, text):
    cipher_suite = Fernet(key)
    return cipher_suite.encrypt(text.encode())

def decrypt_text(key, encrypted_text):
    cipher_suite = Fernet(key)
    return cipher_suite.decrypt(encrypted_text).decode()

def get_ascii_values(text):
    return [ord(char) for char in text]

def get_chars(ascii_values):
    return ''.join(chr(code) for code in ascii_values)

key = generate_key()
image = cv2.imread('1.png')

rows, cols, _ = image.shape

text = input("Enter text to hide : ")
encrypted_text = encrypt_text(key, text)

# Convert encrypted text from bytes to list of ASCII values
encrypted_text_values = get_ascii_values(encrypted_text.decode())

kl = 0
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

l = len(encrypted_text_values)

for i in range(l):
    image[n, m, z] = encrypted_text_values[i] ^ ord(key[kl])
    n = (n + 1) % rows
    m = (m + 1) % cols
    z = (z + 1) % 3
    kl = (kl + 1) % len(key)

cv2.imwrite("encrypted_img.png", image)
print("Data Hiding in Image completed successfully.")

ch = int(input("\nEnter 1 to extract data from Image : "))

if ch == 1:
    key1 = input("\n\nRe enter key to extract text : ")
    decrypt = []

    kl = 0

    if key == bytes(key1, 'utf-8'):
        for i in range(l):
            ascii_val = image[n, m , z] ^ ord(key[kl])
            decrypt.append(ascii_val)
            n = (n + 1) % rows
            m = (m + 1) % cols
            z = (z + 1) % 3
            kl = (kl + 1) % len(key)
        decrypted_text = get_chars(decrypt)
        decrypted_text = decrypt_text(key, decrypted_text.encode())
        print("Decrypted text was : ", decrypted_text)
    else:
        print("Key doesn't match.")
else:
    print("Thank you. EXITING.")
