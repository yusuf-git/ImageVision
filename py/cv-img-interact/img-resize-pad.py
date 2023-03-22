import cv2
import numpy as np
import pyautogui as pygui
from PIL import Image  


def resize(imFile,width,height):
    img = Image.open(imFile)
    out = img.resize((width,height))
    print("out------------------:",out.size)
    return out

def resize_width_per_aspect_ratio(img, target_width, target_height):
    width_ratio = img.shape[1]/target_height
    print("width ratio:",width_ratio)
    new_height = int(width_ratio * target_width)
    print("new_height",new_height)
    dim = (new_height, img.shape[1])
    print("dim:",dim)
    img = img.resize(dim)
    return img


def resize_height_per_aspect_ratio(img, target_width, target_height):
    height_ratio = img.size[0]/target_width
    print("height ratio:",height_ratio)
    new_width = int(height_ratio * target_height)
    print("new_width",new_width)
    dim = (new_width, img.size[1])
    print("dim:",dim)
    img = img.resize(dim)
    return img

# read image
#img = cv2.imread('sdv-logm-1.png')
img_filename = 'CPOTooltip_end.png'
img = cv2.imread(img_filename)
print("img size - check:",img.shape[0],"x",img.shape[1])
ht, wd, cc= img.shape
print("img size: h-",ht," w-",wd)

# create new image of desired size and color (blue) for padding
ww = 1920
hh = 1080
(ww,hh) = pygui.size()
print("screen size:",ww,"x",hh)
if(ht > hh and wd <= ww):
    img = resize_height_per_aspect_ratio(img,img.shape[1],hh)

if(wd > ww and ht <= hh):
    img = resize_width_per_aspect_ratio(img, ww, img.shape[0])


color = (255,0,0)
result = np.full((hh,ww,cc), color, dtype=np.uint8)

# compute center offset
xx = (ww - wd) // 2
yy = (hh - ht) // 2
print("width:::::",ww)
print("height::",hh)
# copy img image into center of result image
result[yy:yy+ht, xx:xx+wd] = img

# view result
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# save result
cv2.imwrite("sdv-logm-resized-1.png", result)


