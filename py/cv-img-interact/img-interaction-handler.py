#/############################################################
# Author : Yusuf
# Date & Time : 19-Apr-2020 12:00 AM To 06:30 AM, 21-Apr-2020 03:10 AM, 01-May-2020 05:00 AM to 8:00 AM
###############################################################
# create a thumbnail of an image
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils
import imagehash


def enhanceSharpness(img):
    #im = Image.open(img)
    enhancer = ImageEnhance.Sharpness(img)
    enhanced_im = enhancer.enhance(10.0)
    #enhanced_im.save("enhanced_B.png")
    #enhanced_im.save("enhanced_A.png")
    return enhanced_im


def enhanceContrast(img):
    #im = Image.open(img)
    enhancer = ImageEnhance.Contrast(img)
    enhanced_im = enhancer.enhance(4.0)
    return enhanced_im

def enhanceBrightness(img):
    #im = Image.open(img)
    enhancer = ImageEnhance.Brightness(img)
    enhanced_im = enhancer.enhance(1.8)
    return enhanced_im


def compare_images_colored(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	#m = mse(imageA, imageB)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
        
    #(score, diff) = ssim(imageA, imageB, multiChannel=True, full=True)/commented for experimental purpose - 23-Apr-2020 03:20 AM
    (score, diff) = ssim(grayA, grayB,  full=True)
    diff = (diff * 250).astype("uint8")
    print("SSIM: {}".format(score))
    #print("l: {}".format(l))
    #print("c: {}".format(c))
    #print("s: {}".format(s))
 
	 # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    
    thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
	    # compute the bounding box of the contour and then draw the
	    # bounding box on both input images to represent where the two
	    # images differ
	    (x, y, w, h) = cv2.boundingRect(c)
	    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 155), 2)
	    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 155), 2)
    #cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 155), 2)
    cv2.imwrite("diff_img_colored.png",diff)
    print("Match similarity:",score)
	# show the output images
    cv2.imshow("Original-Colored", imageA)
    cv2.imshow("Modified-Colored", imageB)
    cv2.imshow("Diff-Colored", diff)
    #cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)

def compare_images_grey(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	#m = mse(imageA, imageB)
        
    #(score, diff) = ssim(imageA, imageB,full=True)
    (score, diff) = ssim(imageA, imageB, full=True)
    diff = (diff * 250).astype("uint8")
    print("SSIM: {}".format(score))
    #print("l: {}".format(l))
    #print("c: {}".format(c))
    #print("s: {}".format(s))
 
	 # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    
    thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
	    # compute the bounding box of the contour and then draw the
	    # bounding box on both input images to represent where the two
	    # images differ
	    (x, y, w, h) = cv2.boundingRect(c)
	    cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 155), 2)
	    cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 155), 2)
    #cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 155), 2)
    cv2.imwrite("diff_img.png",diff)
    print("Match similarity:",score)
	# show the output images
    cv2.imshow("Original-Grey", imageA)
    cv2.imshow("Modified-Grey", imageB)
    cv2.imshow("Diff-Grey", diff)
    #cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)



def doPILPerceptualHash(imageAStr, imageBStr):
    # example_phash.py

# Import dependencies

    # Create the Hash Object of the first image
    baselineHash = imagehash.phash(Image.open(imageAStr))
    print('Original Picture: ' + str(baselineHash))

    # Create the Hash Object of the second image
    actualHash = imagehash.phash(Image.open(imageBStr))
    print('Actual Picture: ' + str(actualHash))

    # Compare hashes to determine whether the pictures are the same or not
    if(baselineHash == actualHash):
        print("Perceptual Hashing :: The pictures are perceptually the same !")
    else:
        distance = baselineHash - actualHash
        print("Perceptual Hashing :: The pictures are different, distance: " + str(distance))


def dodifferencehashing(imageAStr, imageBStr):
    baselineHash = imagehash.dhash(Image.open(imageAStr))
    print('Original Picture: ' + str(baselineHash))

    actualHash = imagehash.dhash(Image.open(imageBStr))
    print('Actual Picture: ' + str(actualHash))

    if(baselineHash == actualHash):
        print("Difference Hashing :: The pictures are perceptually the same !")
    else:
        distance = baselineHash - actualHash
        print("Difference Hashing :: The pictures are different, distance: " + str(distance))


def dhash(image, hashSize=10):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def doOpenCVPerceptualHash(imageAStr, imageBStr):
    imageA = cv2.imread(imageAStr)
    imageB = cv2.imread(imageBStr)
    imageA_grey = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    baselineHash = dhash(imageA_grey)
    imageB_grey = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    actualHash = dhash(imageB_grey)
    if(baselineHash == actualHash):
        print("openCV :: The pictures are perceptually the same !")
    else:
        distance = baselineHash - actualHash
        print("openCV :: The pictures are different, distance: " + str(distance))

# load the image
image1 = Image.open("images/104244_disableMarkerLine_enableMarkerName_B.png")
image2 = Image.open("images/104244_disableMarkerLine_enableMarkerName.png")
# report the size of the image
print("Image1:",image1.size)
print("Image2:",image2.size)
# create a thumbnail and preserve aspect ratio
image1.thumbnail((500,500))
image2.thumbnail((500,500))
# report the size of the thumbnail
print("Thumbnail-img1",image1.size)
print("Thumbnail-img2",image2.size)
image2 = image2.resize((480,500))
print("#################################")
print("Thumbnail-img1",image1.size)
print("Thumbnail-img2",image2.size)

image1.save("image1_thumb.png")
image2.save("image2_thumb.png")
img1 = Image.open("image1_thumb.png")
img2 = Image.open("image2_thumb.png")

img1 = enhanceSharpness(img1)
img2 = enhanceSharpness(img2)
#img1 = enhanceContrast(img1)
#img2 = enhanceContrast(img2)
#img1 = enhanceBrightness(img1)
#img2 = enhanceBrightness(img2)

img1.save("image1_thumb_.png")
img2.save("image2_thumb_.png")

img1 = cv2.imread("image1_thumb_.png")
img2 = cv2.imread("image2_thumb_.png")
img1_g = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_g = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#compare_images_colored(img1,img2,"Img Comp")
#compare_images_grey(img1_g,img2_g,"Img Comp")
#doPILPerceptualHash("image1_thumb__.png","image1_thumb__.png")
#doPILPerceptualHash("histplot_invalid_1.png","histplot_valid_1.png") #fail score
doPILPerceptualHash("sdv_bug2.png","sdv_bug2A.png") #fail score
#doPILPerceptualHash("threshbininv_curve_4.png","threshbininv_curve_5.png") #fail score
doPILPerceptualHash("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName.png") #fail score
doPILPerceptualHash("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName___.png") #fail score

#dodifferencehashing("image1_thumb__.png","image1_thumb__.png")
#dodifferencehashing("histplot_invalid_1.png","histplot_valid_1.png") #fail score
dodifferencehashing("sdv_bug2.png","sdv_bug2A.png") #fail score
#dodifferencehashing("threshbininv_curve_4.png","threshbininv_curve_5.png") #fail score
dodifferencehashing("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName.png") #fail score
dodifferencehashing("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName___.png") #fail score

#doOpenCVPerceptualHash("image1_thumb__.png","image2_thumb__.png")
#doOpenCVPerceptualHash("histplot_invalid_1.png","histplot_valid_1.png") #fail score
doOpenCVPerceptualHash("sdv_bug2.png","sdv_bug2A.png") #fail score
#doOpenCVPerceptualHash("threshbininv_curve_4.png","threshbininv_curve_5.png") #fail score
doOpenCVPerceptualHash("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName.png") #fail score
doOpenCVPerceptualHash("104244_disableMarkerLine_enableMarkerName_B.png","104244_disableMarkerLine_enableMarkerName___.png") #fail score
