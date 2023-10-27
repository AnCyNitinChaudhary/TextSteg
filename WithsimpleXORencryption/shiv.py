import cv2
import numpy as np

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
text = input("Enter text to hide : ")
# print(type(text))
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
        # print(type(decrypt))
        print("Encrypted text was : ", decrypt)
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