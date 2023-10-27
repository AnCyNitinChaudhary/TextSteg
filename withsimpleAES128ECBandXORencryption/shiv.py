import cv2
import numpy as np

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
# print("Encrypted Text:", encrypted_text)
# print(type(encrypted_text))
# Decrypt the ciphertext
# print("Decrypted Text:", decrypted_text)


















#Below is my code
def calculate_psnr(original_image, encrypted_image):
    mse = np.mean((original_image - encrypted_image) ** 2)
    if mse == 0:
        return float('inf')  # PSNR is infinite if images are identical
    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr


d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)
# print('The dictionary d is:')
# print(d)
# print('the dictionary c is:')
# print(c)
x = cv2.imread("5.png")
# print(type(x))
# print("Printing the image matrix",x)
i = x.shape[0] #prints the dimension of the image
j = x.shape[1]
print(i, j)

key = input("Enter key to edit(Security Key) : ")#will be used to authenticate the user
# text = input("Enter text to hide : ")
text = encrypted_text

kl = 0
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

l = len(text)

for i in range(l):
    x[n, m, z] = d[text[i]] ^ d[key[kl]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3
    kl = (kl + 1) % len(key)

cv2.imwrite("encrypted_img.png", x)
print("Data Hiding in Image completed successfully.")
#Note in the above encryption process, the x is updated
kl = 0
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

ch = int(input("\nEnter 1 to extract data from Image : "))

if ch == 1:
    key1 = input("\n\nRe enter key to extract text : ")
    decrypt = ""

    if key == key1:
        for i in range(l):
            decrypt += c[x[n, m, z] ^ d[key[kl]]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
            kl = (kl + 1) % len(key)
        decrypted_text = decrypt_aes_ecb(shivkey,decrypt)
        print("Encrypted text was : ", decrypted_text)
    else:
        print("Key doesn't match.")
else:
    print("Thank you. EXITING.")

# Calculate PSNR
original_image = cv2.imread('5.png')
x = cv2.imread("encrypted_img.png")
x = x.astype(original_image.dtype)
psnr_value = calculate_psnr(original_image, x)
print(f"PSNR value is {psnr_value} dB")