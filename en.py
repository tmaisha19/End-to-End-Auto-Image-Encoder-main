# # Python program implementing Image Steganography

# # PIL module is used to extract
# # pixels of image and modify it
# from PIL import Image

# # Convert encoding data into 8-bit binary
# # form using ASCII value of characters
# def genData(data):

# 		# list of binary codes
# 		# of given data
# 		newd = []

# 		for i in data:
# 			newd.append(format(ord(i), '08b'))
# 		return newd

# # Pixels are modified according to the
# # 8-bit binary data and finally returned
# def modPix(pix, data):

# 	datalist = genData(data)
# 	lendata = len(datalist)
# 	imdata = iter(pix)

# 	for i in range(lendata):

# 		# Extracting 3 pixels at a time
# 		pix = [value for value in imdata.__next__()[:3] +
# 								imdata.__next__()[:3] +
# 								imdata.__next__()[:3]]

# 		# Pixel value should be made
# 		# odd for 1 and even for 0
# 		for j in range(0, 8):
# 			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
# 				pix[j] -= 1

# 			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
# 				if(pix[j] != 0):
# 					pix[j] -= 1
# 				else:
# 					pix[j] += 1
# 				# pix[j] -= 1

# 		# Eighth pixel of every set tells
# 		# whether to stop ot read further.
# 		# 0 means keep reading; 1 means thec
# 		# message is over.
# 		if (i == lendata - 1):
# 			if (pix[-1] % 2 == 0):
# 				if(pix[-1] != 0):
# 					pix[-1] -= 1
# 				else:
# 					pix[-1] += 1

# 		else:
# 			if (pix[-1] % 2 != 0):
# 				pix[-1] -= 1

# 		pix = tuple(pix)
# 		yield pix[0:3]
# 		yield pix[3:6]
# 		yield pix[6:9]

# def encode_enc(newimg, data):
# 	w = newimg.size[0]
# 	(x, y) = (0, 0)

# 	for pixel in modPix(newimg.getdata(), data):

# 		# Putting modified pixels in the new image
# 		newimg.putpixel((x, y), pixel)
# 		if (x == w - 1):
# 			x = 0
# 			y += 1
# 		else:
# 			x += 1

# # Encode data into image
# def encode():
# 	img = input("Enter image name(with extension) : ")
# 	image = Image.open(img, 'r')

# 	data = input("Enter data to be encoded : ")
# 	if (len(data) == 0):
# 		raise ValueError('Data is empty')

# 	newimg = image.copy()
# 	encode_enc(newimg, data)

# 	new_img_name = input("Enter the name of new image(with extension) : ")
# 	newimg.save(new_img_name)

# # Decode the data in the image
# def decode():
# 	img = input("Enter image name(with extension) : ")
# 	image = Image.open(img, 'r')

# 	data = ''
# 	imgdata = iter(image.getdata())

# 	while (True):
# 		pixels = [value for value in imgdata.__next__()[:3] +
# 								imgdata.__next__()[:3] +
# 								imgdata.__next__()[:3]]

# 		# string of binary data
    
# 		binstr = ''

# 		for i in pixels[:8]:
# 			if (i % 2 == 0):
# 				binstr += '0'
# 			else:
# 				binstr += '1'

# 		data += chr(int(binstr, 2))
# 		print(data)
# 		if (pixels[-1] % 2 != 0):
# 			return data

# # Main Function
# def main():
# 	a = int(input(":: Welcome to Steganography ::\n"
# 						"1. Encode\n2. Decode\n"))
# 	if (a == 1):
# 		encode()

# 	elif (a == 2):
# 		print("Decoded Word : " + decode())
# 	else:
# 		raise Exception("Enter correct input")

# # Driver Code
# if __name__ == '__main__' :

# 	# Calling main function
# 	main()


# Python program to demonstrate
# image steganography using OpenCV


import cv2
import numpy as np
import random


# Encryption function
def encrypt():
	
	# img1 and img2 are the
	# two input images
	img1 = cv2.imread('mohot.jpg')
	img2 = cv2.imread('mohot2.jpg')
	
	for i in range(img2.shape[0]):
		for j in range(img2.shape[1]):
			for l in range(3):
				
				# v1 and v2 are 8-bit pixel values
				# of img1 and img2 respectively
				v1 = format(img1[i][j][l], '08b')
				v2 = format(img2[i][j][l], '08b')
				
				# Taking 4 MSBs of each image
				v3 = v1[:4] + v2[:4]
				
				img1[i][j][l]= int(v3, 2)
				
	cv2.imwrite('pic3in2.png', img1)

	
# Decryption function
def decrypt():
	
	# Encrypted image
	img = cv2.imread('pic3in2.png')
	width = img.shape[0]
	height = img.shape[1]
	
	# img1 and img2 are two blank images
	img1 = np.zeros((width, height, 3), np.uint8)
	img2 = np.zeros((width, height, 3), np.uint8)
	
	for i in range(width):
		for j in range(height):
			for l in range(3):
				v1 = format(img[i][j][l], '08b')
				v2 = v1[:4] + chr(random.randint(0, 1)+48) * 4
				v3 = v1[4:] + chr(random.randint(0, 1)+48) * 4
				
				# Appending data to img1 and img2
				img1[i][j][l]= int(v2, 2)
				img2[i][j][l]= int(v3, 2)
	
	# These are two images produced from
	# the encrypted image
	cv2.imwrite('pic2_re.png', img1)
	cv2.imwrite('pic3_re.png', img2)
	
	
# Driver's code
encrypt()
decrypt()
