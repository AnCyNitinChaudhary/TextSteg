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
print(type(ciphertext))
# Decrypt the message: decode from base64 and decrypt
decoded_ciphertext = base64.b64decode(ciphertext.encode('utf-8'))
plaintext_bytes = private_key.decrypt(
    decoded_ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
plaintext = plaintext_bytes.decode('utf-8')  # Decode to string

print("Serialized Public Key:", pem)
print("Serialized Private Key:", pem2)
print("Encrypted Message:", ciphertext)
print("Decrypted Message:", plaintext)