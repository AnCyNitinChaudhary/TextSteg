import cv2
import numpy as np


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64

# Generate a private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Generate a public key
public_key = private_key.public_key()

# Serialize public key
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')  # Decode to string

# Serialize private key
pem2 = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.BestAvailableEncryption(b'passphrase')
).decode('utf-8')  # Decode to string

# The message to be encrypted
message = b'this'

# Encrypt the message and encode it to base64
ciphertext_bytes = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
ciphertext = base64.b64encode(ciphertext_bytes).decode('utf-8')
# print(type(ciphertext))
# Decrypt the message: decode from base64 and decrypt
  # Decode to string

print("Serialized Public Key:", pem)
print("Serialized Private Key:", pem2)
print("Encrypted Message:", ciphertext)
# print("Decrypted Message:", plaintext)













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

shivkey = input("Enter shivkey to edit(Security shivkey) : ")#will be used to authenticate the user
# text = input("Enter text to hide : ")
text = ciphertext

kl = 0
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

l = len(text)

for i in range(l):
    x[n, m, z] = d[text[i]] ^ d[shivkey[kl]]
    n = n + 1
    m = m + 1
    z = (z + 1) % 3
    kl = (kl + 1) % len(shivkey)

cv2.imwrite("encrypted_img.png", x)
print("Data Hiding in Image completed successfully.")
#Note in the above encryption process, the x is updated
kl = 0
z = 0  # decides plane
n = 0  # number of row
m = 0  # number of column

ch = int(input("\nEnter 1 to extract data from Image : "))







def nitinfunction(decryptstring):
    decoded_ciphertext = base64.b64decode(decryptstring.encode('utf-8'))
    plaintext_bytes = private_key.decrypt(decoded_ciphertext, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    plaintext = plaintext_bytes.decode('utf-8')
    return plaintext
if ch == 1:
    shivkey1 = input("\n\nRe enter shivkey to extract text : ")
    decrypt1 = ""

    if shivkey == shivkey1:
        for i in range(l):
            decrypt1 += c[x[n, m, z] ^ d[shivkey[kl]]]
            n = n + 1
            m = m + 1
            z = (z + 1) % 3
            kl = (kl + 1) % len(shivkey)
        
        print("Encrypted text was : ", nitinfunction(decrypt1))
    else:
        print("shivkey doesn't match.")
else:
    print("Thank you. EXITING.")

# Calculate PSNR
original_image = cv2.imread('5.png')
x = cv2.imread("encrypted_img.png")
x = x.astype(original_image.dtype)
psnr_value = calculate_psnr(original_image, x)
print(f"PSNR value is {psnr_value} dB")