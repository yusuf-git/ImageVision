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
