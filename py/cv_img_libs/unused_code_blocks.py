'''
# create a thumbnail of an image
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils
import imagehash
'''

'''

while(k < res_length):
        ob = imageops(res_obj[k]["image"], res_obj[k]["base_img_path"], res_obj[k]["runtime_img_path"], res_obj[k]["algo"],res_obj[k]["expscore"],res_obj[k]["original_score"],res_obj[k]["result"],res_obj[k]["msg"])
        #print(ob)
        #print("##############################")
        #if(ob.result is False and str(ob.msg).lower().startswith("missing") is False):
        print("ob.result = ",ob.result)
        if(ob.result == True):
            print("##############################")
            print("deleting item:",ob)
            comp_result_data.pop(k)
            print("##############################")
        k = k + 1


for r in comp_result_data:
    print([r])
    print("#######JSON string#######################")
    json_rec = jsonpickle.encode(r)
    print(json_rec)
    print("#######END - JSON string#######################")
    

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#res_obj = jsonpickle.decode(json_file_data)
'''










'''
#############################################################################################################################
###################################### UNUSED FUNCTIONS #####################################################################
#############################################################################################################################
# created on 12-Feb-2021 12:30 PM #
def eval_OR_operator_resultsets(results_collection_dict, eval_group_result_coll_start_idx, eval_group_result_coll_end_idx ):
    if(len(results_collection_dict) <= 0):
        print("No records in resultset")
        return False, False, {}
    result_dict = results_collection_dict[eval_group_result_coll_end_idx][algo_name_list[eval_group_result_coll_end_idx]]
    if len(result_dict) > 0:
        return True, False, result_dict
    else:
        return True, True, result_dict



 # created on 17-Oct-2020 05:30 PM #
 # updates on 18-Oct-2020 12:25 AM, 03:15 AM #
def analyze_net_result(dt, comp_result_data, op_net_result):
    #if(op_net_result == True):
    #    return True, "", passed_imgs_with_or_operator_algo
    curr_algo=""
    match_operator = config_utils_lib.get_algo_match_operator(dt)
    operations_res = True
    comp_res_obj  = iter(comp_result_data)
    n = 0
    passed_imgs_with_or_operator_algo = {}
    #passed_imgs_with_or_operator = []
    tmp_failures_with_algos = ""
    failures_with_algos = ""
    while(len(comp_result_data) > 0 and n < len(comp_result_data)):
        if(comp_result_data[n]["algo"] == "BF"):
            comp_result_data[n]["algo"] = "BRISK-FLANN"
        if(comp_result_data[n]["algo"] == "p-hash"):
            comp_result_data[n]["algo"] = "perceptual_hashing"
        operator = match_operator[comp_result_data[n]["algo"]]
        curr_algo = comp_result_data[n]["algo"]
        print("operator:",operator)
        print("curr_algo:",curr_algo)
        #curr_algo = next(comp_res_obj)
        while(comp_result_data[n]["algo"] == curr_algo and n < len(comp_result_data)):
            if(comp_result_data[n]["result"] == False and operator.lower() == "and"):
                operations_res = False
                tmp_failures_with_algos = curr_algo
            passed_imgs_with_or_operator_algo =  find_passed_imgs_with_or_operator(n, curr_algo, operator, comp_result_data)
            n = n + 1
            if(n >= len(comp_result_data)):
                break
        # concatenate algos with comma until before the last algo
        if(n < len(comp_result_data)):
            failures_with_algos = failures_with_algos + tmp_failures_with_algos + ", "
        elif(n > len(comp_result_data)):
            failures_with_algos = failures_with_algos + tmp_failures_with_algos  # concatenate algo without comma for the last algo
        tmp_failures_with_algos = ""
    # in case the algos that have failed ends with comma, remove it
    if(failures_with_algos.strip().endswith(",") == True):
        failures_with_algos = failures_with_algos.strip()[:-1]
    
    if(op_net_result == False):
        return operations_res, failures_with_algos, passed_imgs_with_or_operator_algo
    else:
        return True, failures_with_algos, passed_imgs_with_or_operator_algo # in case the net result is already True(i.e.Pass), return the passed images list with "OR" operator algo with net result being True

  


def find_passed_imgs_with_or_operator(n, curr_algo, operator, comp_result_data):
    passed_algos_imgs_with_or_operator = {}
    passed_imgs_with_or_operator = []
    if(comp_result_data[n]["result"] == True and operator.lower() == "or"):
        passed_imgs_with_or_operator.append(comp_result_data[n]["image"])
        passed_algos_imgs_with_or_operator[curr_algo] = passed_imgs_with_or_operator
    return passed_algos_imgs_with_or_operator



# created on 21-Jan-2021 11:50 PM #
def check_for_AND_eval_operator(algo_cnt):
    multi_eval_groups = False
    curr_group_or_operator = False
    curr_group_and_operator = False
    group_level_or_operator = False
    group_level_and_operator = False
    next_group_or_operator = False
    next_group_and_operator = False

    tmp_algo_idx = 0
    _AND_operator = False
    while(tmp_algo_idx < algo_cnt):
        tmp_algo = algo_name_list_runnables[tmp_algo_idx]
        tmp_operator = match_operator_dict[tmp_algo]
        tmp_runnable_state = runnable_state_labels[algo_runnable_state] 

        if tmp_operator == "and" and tmp_runnable_state == "on":
            _AND_operator = True
        tmp_algo_idx = tmp_algo_idx + 1
    return _AND_operator



# created on 23-Jan-2021 11:00 PM #
# updates on 28-Jan-2021 01:25 AM #
def can_delete_passed_results(algo_curr_idx, algo_cnt, dt):
    if algo_curr_idx == 0:
        return False
    eval_groupID = ""
    algo_match_operator = ""
    and_operator_present = False
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)    
    while (algo_curr_idx < algo_cnt):
        algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_curr_idx]]
        if algo_runnable_state == "1":
            and_operator_present = logical_gate_evaluator.check_AND_operator_in_curr_eval_group(algo_curr_idx, algo_cnt, dt)
            next_algo = algo_name_list_runnables[algo_curr_idx+1]
            next_algo_match_operator = match_operator_dict[next_algo]
            break
        algo_curr_idx = algo_curr_idx + 1

    if and_operator_present == True:
        return False
    else:
        return True




# created on 23-Jan-2021 01:15 PM to 05:30 PM #
# updates on 24-Jan-2021 02:10 AM #
def check_multiple_eval_groups_configured(algo_curr_idx, algo_cnt, dt):
    multi_eval_groups = False
    eval_groupID_dict = config_utils_lib.get_algo_eval_groupID(dt)
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    while algo_curr_idx < algo_cnt:
        curr_eval_groupID = eval_groupID_dict[algo_name_list_runnables[algo_curr_idx]]
        next_eval_groupID, _ = logical_gate_evaluator.get_next_eval_groupID_and_match_operator(algo_curr_idx,algo_cnt,dt)
        if curr_eval_groupID != next_eval_groupID and curr_eval_groupID != "" and next_eval_groupID != "":
            multi_eval_groups = True
            break
        algo_curr_idx = algo_curr_idx + 1
    return multi_eval_groups



# created on 19-Jan-2021 05:30 PM #
 # updates on 20-Jan-2021 11:45 PM #
def get_algo_operator(idx, dt, comp_result_data):
    curr_algo=""
    operator = ""
    groupID = ""
    match_operator = config_utils_lib.get_algo_match_operator(dt)
    operations_res = True
    comp_res_obj  = iter(comp_result_data)
    n = 0
    #passed_imgs_with_or_operator = []
    tmp_failures_with_algos = ""
    failures_with_algos = ""
    if(len(comp_result_data) > 0 and idx < len(comp_result_data)):
        operator = match_operator[comp_result_data[n]["algo"]]
        curr_algo = comp_result_data[n]["algo"]
    return curr_algo, operator, groupID






#print("*************************************************************************")
#print("                    ImageVision v6 operation summary -->         ")
#print("net result                              : ",operation_net_result)
#print("failures with algos                     : ",net_img_found_result_dict)
#print("passed matches with 'OR' operator algo  : ",passed_imgs_with_or_operator_algo)
#print("**************************************************************************")

#ob = imageops(res_obj[0]["image"],res_obj[0]["algo"],res_obj[0]["expscore"],res_obj[0]["original_score"],res_obj[0]["result"],res_obj[0]["msg"])

#a = [{"image":"1.png","score":1.0,"outcome":False},{"image":"2.png","score":0.96,"outcome":True}]





#############################################################################################################################
###################################### UNUSED FUNCTIONS #####################################################################
#############################################################################################################################
'''



'''
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
'''