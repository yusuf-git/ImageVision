import cv2
import numpy as np
import pyautogui as pygui

# read image
img = cv2.imread('sdv-logm-1.png')
ht, wd, cc= img.shape
print("img size: h-",ht," w-",wd)

# create new image of desired size and color (blue) for padding
ww = 1920
hh = 1080
(ww,hh) = pygui.size()

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