import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error
import numpy as np
import random
import math
def get_position(n,y):
    num_list = list(range(0, n))
    random.shuffle(num_list)
    # print(num_list)
    position_list = []
    for i in range(n):
        var = num_list[i]
        i = math.floor(var/(y+1))
        j = var % (y+1)
        position_list.append((i, j))
    return position_list

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
original_image=x.copy()
# print(type(original_image))
# print(type(x))
# print("Printing the image matrix",x)
i = x.shape[0] #prints the dimension of the image
j = x.shape[1]
print(i, j)
print(x)
# key = input("Enter key to edit(Security Key) : ")#will be used to authenticate the user
text = input(f"Enter text to hide containing maximum of {i*j} characters: ")
temp=len(text)
while(temp>i*j):
    print(f"The text size if more than {i*j} characters, please enter the text again:")
    text = input(f"Enter text to hide containing maximum of {i*j} characters: ")
    temp=len(text)
ls=get_position(len(text),j-1)
print("positional list is:",ls)
# print(type(text))
# kl = 0
z = 0  # decides plane
l = len(text)

for i in range(l):
    x[ls[i][0], ls[i][1], z] = d[text[i]] ^ x[ls[i][0],ls[i][1],z]
    z = (z + 1) % 3
    # kl = (kl + 1) % len(key)
print(x)
cv2.imwrite("encrypted_img.png", x)
print("Data Hiding in Image completed successfully.")
#Note in the above encryption process, the x is updated
z = 0  # decides plane

ch = int(input("\nEnter 1 to extract data from Image or Enter anything else to exit: "))

if ch == 1:
    decrypt = ""

    for i in range(l):
        decrypt += c[x[ls[i][0], ls[i][1], z] ^ original_image[ls[i][0],ls[i][1],z]]
        z = (z + 1) % 3
        # kl = (kl + 1) % len(key)
    # print(type(decrypt))
    print("Encrypted text was : ", decrypt)
else:
    print("Thank you. EXITING.")

# Calculate PSNR
# original_image = cv2.imread('veryverysmall.png')
x = cv2.imread("encrypted_img.png")
x = x.astype(original_image.dtype)
psnr_value = calculate_psnr(original_image, x)
print(f"PSNR value is {psnr_value} dB")



gray_image1 = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)


ssim_index = ssim(gray_image1, gray_image2)


mse_value = mean_squared_error(gray_image1, gray_image2)


print(f'SSIM: {ssim_index:.2f}')
print(f'MSE: {mse_value:.2f}')