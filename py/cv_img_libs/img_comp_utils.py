##Created on 08-Aug-2020 10:30 AM
##Updates on 08-Aug-2020 01:30 AM, 09-Aug-2020 01:00 AM, 10-Aug-2020 03:10 AM, 11-Aug-2020 10:30 PM, 12-Aug-2020 01:30 AM, 13-Aug-2020 02:30 AM, 14-Aug-2020 02:15 AM, 15-Aug-2020 02:45 AM, 28-Sep-2020 02:20 AM, 29-Sep-2020 01:15 AM, 02-Oct-2020 01:00 AM, 03-Oct-2020 01:15 AM, 04-Oct-2020 12:45 AM, 05-Oct-2020 02:25 AM, 06-Aug-2020 02:45 AM, 07-Aug-2020 03:20 AM, 13-Oct-2020 04:00 AM, 18-Oct-2020 03:45 AM, 24-Nov-2020 11:50 PM, 24-Oct-2021 02:50 AM, 21-Nov-2011 01:00 PM to 09:45 PM

import argparse
import os.path
import time
import json
import logging
import numpy as np
from PIL import Image  
import cv2
import pyautogui as pygui
from skimage.measure import compare_ssim
import imutils
import os
from pathlib import Path
from shutil import copyfile
import multiprocessing as mp
from multiprocessing import Process, Lock
from cv_img_matcher.algos_namelist import comp_algos
from data_models.imageops_data_model import CustomEncoder
from cv_img_libs import gen_utils
#from di_container import di_container

def readJson(jsonFile_, mainkey):
    f_ = open(jsonFile_) 
    data_ = json.load(f_) 
    #print(data_)
    for i in data_[mainkey]: 
        pass
        #print(i) 
    f_.close()
    return data_

def readJson_plain(jsonFile_):
    f_ = open(jsonFile_) 
    data_ = json.load(f_) 
    #print(data_) #uncomment later 07-Oct-2020 09:37 PM
    #for i in data_: 
    #    print(i) 
    f_.close()
    return data_

# created on 04-Oct-2020 09:05 PM #
#def writeJson(jsonFile_, data):
 #   with open(jsonFile_, 'w') as fp:
  #      json.dump(data, fp)


def writeResult(result,msg, resPath):
    resFile = os.path.join(resPath, "result.json")
    if(os.path.exists(resFile)):
        os.remove(resFile)
    resultStr = {"result":result,"message":msg}
    resJson = json.dumps(resultStr, indent=4)
    with open(resFile,"w") as json_out:
        json_out.write(resJson)


# created on 06-Aug-2020 02:45 AM #
# updates on 07-Aug-2020 03:20 AM, 03:15 PM, 17-Oct-2020 03:05 AM, 01-Nov-2020 01:35 AM #
def writeJson(resFile, data, stringFormat=False, filemode="w", del_current_file=True):
    #resFile = os.path.join(resPath, "result.json")
    if(os.path.exists(resFile) and del_current_file == True):
        os.remove(resFile)
    
    #resultStr = {"result":result,"message":msg}
    #print(data)
    #resJson = json.dump(data.__dict__, lambda o: o.__dict__, indent=4)
    #resJson = json.dumps(data, cls = CustomEncoder)
    if(stringFormat==False):
        resJson = json.dumps([o.dump() for o in sorted(data)])
    else:
        data = json.dumps(data)
        resJson = str(data)
    #print("resjson:",resJson) #uncomment later 01-Oct-2020 09:35 PM
    with open(resFile,filemode) as json_out:
        json_out.write(resJson)


# created on 06-Aug-2020 02:45 AM #
# updates on 07-Aug-2020 03:20 AM, 03:15 PM #
#def write_dict_Json(resFile, data):
    #resFile = os.path.join(resPath, "result.json")
 #   if(os.path.exists(resFile)):
 #       os.remove(resFile)
    #resultStr = {"result":result,"message":msg}
    #print(data)
    #resJson = json.dump(data.__dict__, lambda o: o.__dict__, indent=4)
    #resJson = json.dumps(data, cls = CustomEncoder)
    #resJson = json.dumps([o.dump() for o in data])
    #print("resjson:",resJson) #uncomment later 01-Oct-2020 09:35 PM
 #   with open(resFile,"w") as json_out:
 #       json_out.write(str(data))


 # created on 06-Aug-2020 02:45 AM #
 # updates on 07-Aug-2020 01:30 AM, 28-Oct-2020 12:10 AM, 23-Nov-2020 03:10 PM #
def writelist_toJson(resFile, datalist):
    #resFile = os.path.join(resPath, "result.json")
    if(os.path.exists(resFile)):
        os.remove(resFile)
    #resultStr = {"result":result,"message":msg}
    #print(data)
    #resJson = json.dump(data.__dict__, lambda o: o.__dict__, indent=4)
    resJson = json.dumps([ob.__dict__ for ob in datalist], indent=4)
    ##print("resjson:",resJson)
    with open(resFile,"w") as json_out:
        json_out.write(resJson)

# added on 23-Nov-2020 03:10 PM #
def writeToFile(file, contents):
    f = open(file, "a")
    f.write(contents)
    f.close()


def readMaskArea(maskRegion_):
    c_x1 = ""
    c_y1 = ""
    c_x2 = ""
    c_y2 = ""
    if(maskRegion_ != ""):
        c_x1 = str(maskRegion_).split(',')[0]
        c_y1 = str(maskRegion_).split(',')[1]
        c_x2 = str(maskRegion_).split(',')[2]
        c_y2 = str(maskRegion_).split(',')[3]
    return c_x1,c_y1,c_x2,c_y2


# created on 05-Oct-2020 02:10 AM #
# updates on 05-Oct-2020 02:20 AM, 23-Nov-2020 03:30 PM to 11:20 PM #
def baseline_apply_mask_excluding_region(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set):
    print("img category : baseline, action : apply mask, mask action on : excluding the specified region")
    logging.info("img category : baseline, action : apply mask, mask action on : excluding the specified region")
    c_x1_, c_y1_, c_x2_, c_y2_ = readMaskArea(mask_area)
    img1_path = os.path.dirname(tmp_img1)
    img2_path = os.path.dirname(tmp_img2)
    #if(img_files_[key] is False):
    img1_fname = os.path.join(img1_path, os.path.basename(tmp_img1))
    tmp_ref_file1 = os.path.basename(tmp_img1).split('_')
    idx = int(tmp_ref_file1[1].split('.')[0])
    print("runtime image --> temp image path : ", img1_path)
    base_img_cnt, runtime_img_cnt = get_img_count(img1_path,img2_path)
    print("base_img_cnt,run img cnt:",base_img_cnt," ",runtime_img_cnt)
    print("mask region :",(int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)))
    logging.info("mask region :("+ str(c_x1_) + ","+ str(c_y1_) + "), (" + str(c_x2_) + "," + str(c_y2_) + ")")

    for x in range(1, base_img_cnt+1, 1):
        image = cv2.imread(img1_fname)
        mask_ = np.zeros(image.shape[:2], dtype = "uint8")
        h,w,c = image.shape
        #print("image : ",img1_fname," --> width, height, channel:", w, h, c)
        cv2.rectangle(mask_, (int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)), (255,0,0), -1)
        masked_ = cv2.bitwise_and(image, image, mask = mask_)
        cv2.imwrite(img1_fname,masked_)
        print(img1_fname+" masked(exclude region)")
        if(_is_debugging_set.lower() != "false"):
            cv2.imshow("Masked excluding the specified region", masked_)
            cv2.waitKey(0)
        idx = idx + 1
        img1_fname, img2_fname = getFileName(tmp_img1,tmp_img2,idx,[],realtime)
        if(realtime != "true"):
            return


# created on 05-Oct-2020 02:05 AM # 
# updates on 05-Oct-2020 02:20 AM, 24-Nov-2020 11:50 PM #
def runtime_imgs_apply_mask_excluding_region(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set):
    print("img category : runtime, action : apply mask, mask action on : excluding the specified region")
    logging.info("img category : runtime, action : apply mask, mask action on : excluding the specified region")
    c_x1_, c_y1_, c_x2_, c_y2_ = readMaskArea(mask_area)
    img1_path = os.path.dirname(tmp_img1)
    img2_path = os.path.dirname(tmp_img2)
    #if(img_files_[key] is False):
    img2_fname = os.path.join(img2_path, os.path.basename(tmp_img2))
    tmp_ref_file2 = os.path.basename(tmp_img2).split('_')
    idx = int(tmp_ref_file2[1].split('.')[0])
    print("runtime image --> temp image path : ", img2_path)
    base_img_cnt, runtime_img_cnt = get_img_count(img1_path,img2_path)
    print("base_img_cnt,run img cnt:",base_img_cnt," ",runtime_img_cnt)
    print("mask region :",(int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)))
    logging.info("mask region :("+ str(c_x1_) + ","+ str(c_y1_) + "), (" + str(c_x2_) + "," + str(c_y2_) + ")")

    for x in range(1, runtime_img_cnt+1, 1):
        image = cv2.imread(img2_fname)
        mask_ = np.zeros(image.shape[:2], dtype = "uint8")
        h,w,c = image.shape
        #print("image : ",img2_fname," --> width, height, channel:", w, h, c)
        cv2.rectangle(mask_, (int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)), (255,0,0), -1)
        masked_ = cv2.bitwise_and(image, image, mask = mask_)
        cv2.imwrite(img2_fname, masked_)
        print(img2_fname+" masked(exclude region)")
        if(_is_debugging_set != "false"):
            cv2.imshow("Masked excluding the specified region", masked_)
            cv2.waitKey(0)
        idx = idx + 1
        img1_fname, img2_fname = getFileName(tmp_img1,tmp_img2,idx,[],realtime)
        if(realtime != "true"):
            return

# updates on 05-Oct-2020 02:00 AM, 02:20 AM, 24-Nov-2020 11:50 PM #
def baselineImages_apply_mask(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set):
    print("img category : baseline, action : apply mask, mask action on : specified region")
    logging.info("img category : baseline, action : apply mask, mask action on : specified region")
    c_x1_, c_y1_, c_x2_, c_y2_ = readMaskArea(mask_area)
    img1_path = os.path.dirname(tmp_img1)
    img2_path = os.path.dirname(tmp_img2)
    img1_fname = os.path.join(img1_path, os.path.basename(tmp_img1))
    tmp_ref_file1 = os.path.basename(tmp_img1).split('_')
    idx = int(tmp_ref_file1[1].split('.')[0])
    print("baseline image --> temp image path :",img1_path)
    base_img_cnt, runtime_img_cnt = get_img_count(img1_path,img2_path)
    print("base_img_cnt,run img cnt:",base_img_cnt," ",runtime_img_cnt)
    print("mask region :",(int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)))
    logging.info("mask region :("+ str(c_x1_) + ","+ str(c_y1_) + "), (" + str(c_x2_) + "," + str(c_y2_) + ")")

    for x in range(1, base_img_cnt+1, 1):
        image = cv2.imread(img1_fname)
        h,w,c = image.shape
        #print("image : ",img1_fname," --> width, height, channel:", w, h, c)
        masked_image = image
        masked_image[int(c_y1_):int(c_y2_),int(c_x1_):int(c_x2_)] = (0,0,0)
        cv2.imwrite(img1_fname,masked_image)
        print(img1_fname+" masked")
        if(_is_debugging_set!="false"):
            cv2.imshow("Masked baseline image", masked_image)
            cv2.waitKey(0)
        idx = idx + 1
        img1_fname, img2_fname = getFileName(tmp_img1,tmp_img2,idx,[],realtime)
        if(realtime != "true"):
            return


# updates on 05-Oct-2020 01:55 AM, 02:20 AM, 24-Nov-2020 11:50 PM #
def runtime_imgs_apply_mask(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set):
    print("img category : runtime, action : apply mask, mask action on : the specified region")
    logging.info("img category : runtime, action : apply mask, mask action on : the specified region")
    c_x1_, c_y1_, c_x2_, c_y2_ = readMaskArea(mask_area)
    img1_path = os.path.dirname(tmp_img1)
    img2_path = os.path.dirname(tmp_img2)
    img2_fname = os.path.join(img2_path, os.path.basename(tmp_img2))
    print("img2_fname:",img2_fname)
    tmp_ref_file2 = os.path.basename(tmp_img2).split('_')
    idx = int(tmp_ref_file2[1].split('.')[0])
    #print("runtime image --> temp image path :",img2_path)
    base_img_cnt, runtime_img_cnt = get_img_count(img1_path,img2_path)
    print("base_img_cnt,run img cnt:",base_img_cnt," ",runtime_img_cnt)
    print("mask region :",(int(c_x1_), int(c_y1_)), (int(c_x2_), int(c_y2_)))
    logging.info("mask region :("+ str(c_x1_) + ","+ str(c_y1_) + "), (" + str(c_x2_) + "," + str(c_y2_) + ")")
    #print("============runtime_img_cnt+1:",runtime_img_cnt+1)
    for x in range(1, runtime_img_cnt+1, 1):
        image = cv2.imread(img2_fname)
        h,w,c = image.shape
        #print("image : ",img2_fname," --> width, height, channel:", w, h, c)
        masked_image = image
        masked_image[int(c_y1_):int(c_y2_),int(c_x1_):int(c_x2_)] = (0,0,0)
        cv2.imwrite(img2_fname,masked_image)
        print(img2_fname+" masked")
        if(_is_debugging_set != "false"):
            cv2.imshow("Masked runtime image", masked_image)
            cv2.waitKey(0)
        idx = idx + 1
        img1_fname, img2_fname = getFileName(tmp_img1,tmp_img2,idx,[],realtime)
        if(realtime != "true"):
            return



# updates on 04-Oct-2020 09:45 PM, 24-Nov-2020 12:20 AM, 24-Nov-2020 11:50 PM #
def apply_mask_parallel(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set):
    start_time = time.time()
    if __name__ == '__main__':
        print("Inside apply_mask_parallel and __name==__main ")
        p1 = Process(target=baselineImages_apply_mask, args=(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set))
        p1.start()
        p2 = Process(target=runtime_imgs_apply_mask, args=(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set))
        p2.start()
        p1.join()
        p2.join()
    else:
        print("starting apply_mask_parallel : non-parallel run")
        baselineImages_apply_mask(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set)
        runtime_imgs_apply_mask(tmp_img1, tmp_img2, mask_area, realtime, _is_debugging_set)

    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished masking the region in "+ str(elapsed_time) +" minutes...")

        

# updates on 24-Nov-2020 11:50 PM #
def apply_mask_excluding_region_parallel(tmp_img1, tmp_img2, mask_area_excl, realtime, _is_debugging_set):
    start_time = time.time()
    if __name__ == '__main__':
        print("invoking apply_mask_excluding_region_parallel and __name==__main... ")
        p1 = Process(target=baseline_apply_mask_excluding_region, args=(tmp_img1, tmp_img2, mask_area_excl, realtime, _is_debugging_set))
        p1.start()
        p2 = Process(target=runtime_imgs_apply_mask_excluding_region, args=(tmp_img1, tmp_img2, mask_area_excl, realtime, _is_debugging_set))
        p2.start()
        p1.join()
        p2.join()
    else:
        print("invoking apply_mask_excluding_region_parallel...")
        baseline_apply_mask_excluding_region(tmp_img1, tmp_img2, mask_area_excl, realtime, _is_debugging_set)
        runtime_imgs_apply_mask_excluding_region(tmp_img1, tmp_img2, mask_area_excl, realtime, _is_debugging_set)

    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished masking - exlcude region - in "+ str(elapsed_time) +" minutes...")



def resize(imFile,width,height):
    img = Image.open(imFile)
    out = img.resize((width,height))
    print("out------------------:",out.size)
    return out
    #out.save("D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/body-resized-1.png")

# updates on 24-Nov-2020 12:50 AM #
def createTempWorkspace(runTimePath):
    base_tmp_img_path = os.path.join(os.path.dirname(runTimePath),"b_temp")
    run_tmp_img_path = os.path.join(os.path.dirname(runTimePath),"r_temp")
    if(os.path.exists(base_tmp_img_path) is False):
        os.mkdir(base_tmp_img_path)
    if(os.path.exists(run_tmp_img_path) is False):
        os.mkdir(run_tmp_img_path)
    logging.info("temp workspace paths:" + base_tmp_img_path + run_tmp_img_path)
    return base_tmp_img_path, run_tmp_img_path

def getTempFileNames(image1, image2, runTimePath):
    base_tmp_img_path, run_tmp_img_path = createTempWorkspace(runTimePath)
    tmp_img1 = os.path.basename(image1)
    tmp_img2 = os.path.basename(image2)
    tmp_img1 = os.path.join(base_tmp_img_path,tmp_img1)
    tmp_img2 = os.path.join(run_tmp_img_path,tmp_img2)
    return tmp_img1,tmp_img2

# updates on 08-Oct-2020 02:35 AM #
def get_img_count(base_path, runtime_path, result_list=[]):
    #print("basepath1:",base_path)
    #print("runtime_path1:",runtime_path)
    #base_path = os.path.dirname(base_path)
    #runtime_path = os.path.dirname(runtime_path)
    #print("basepath:",base_path)
    #print("runtime_path:",runtime_path)
    if(len(result_list) > 0):
        base_img_cnt = len(result_list)
        runtime_img_cnt = len(result_list)
        return base_img_cnt,runtime_img_cnt
    base_img_cnt = 0
    runtime_img_cnt = 0
    base_img_cnt = len([name for name in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, name)) and name.split('.')[1] == "png"])
    runtime_img_cnt = len([name for name in os.listdir(runtime_path) if os.path.isfile(os.path.join(runtime_path, name)) and name.split('.')[1] == "png"])
    return base_img_cnt,runtime_img_cnt


# updates on 04-Dec-2020 03:05 AM #
def copyFiles(img_files_, img1, img2, tmp_img1, tmp_img2, dt):
    #tmp_ref_file1 = os.path.basename(img1).split('_')
    #idx = int(tmp_ref_file1[1].split('.')[0])
    img1_path = os.path.dirname(img1)
    img2_path = os.path.dirname(img2)
    tmp_img1_path = os.path.dirname(tmp_img1)
    tmp_img2_path = os.path.dirname(tmp_img2)
    runtime_img = os.path.basename(img2)
    print("img_files_:",img_files_)
    print("img1_path:",img1_path)
    print("img2_path:",img2_path)
    print("tmp_img1_path:",tmp_img1_path)
    print("tmp_img1_path:",tmp_img2_path)
    #time.sleep(8)
    logging.info("copying baseline and runtime images to tmp processing path....")
    for key in img_files_:
        if(dt["compare_args"]["sliding_window_active"] == "true"):
            print(key, '->', img_files_[key])
            img1_fname = os.path.join(img1_path, key)
            img2_fname = os.path.join(img2_path, runtime_img)
            tmp_img1_fname = os.path.join(tmp_img1_path, key)
            tmp_img2_fname = os.path.join(tmp_img2_path, runtime_img)
            if(dt["compare_args"]["copied_baseline_to_temp_location"] == "false"):
                copyfile(img1_fname, tmp_img1_fname)   
                print("copied to temp basleine")         
                #time.sleep(10)
            
            copyfile(img2_fname, tmp_img2_fname)
            print("img1_fname_sliding:",img1_fname)
            print("img2_fname_sliding:",img2_fname)
            print("tmp_img1_fname_sliding:",tmp_img1_fname)
            print("tmp_img2_fname_sliding:",tmp_img2_fname)
            #time.sleep(1)
            return

        
        print(key, '->', img_files_[key])
        #if(img_files_[key] is False):
        img1_fname = os.path.join(img1_path, key)
        img2_fname = os.path.join(img2_path, key)
        tmp_img1_fname = os.path.join(tmp_img1_path, key)
        tmp_img2_fname = os.path.join(tmp_img2_path, key)
        copyfile(img1_fname, tmp_img1_fname)            
        copyfile(img2_fname, tmp_img2_fname)
                    

# updates on 24-Nov-2020 01:00 AM, 11:50 PM #
def downsizeAndEqualizeImages(tmp_img1, tmp_img2, diff_img_files_, dt):
    #image1 = cv2.imread(image1)
    #image2 = cv2.imread(image2)
    print("beginning the downsize and equalizing process...")
    start_time = time.time()
    logging.info("beginning the downsize and equalizing process...")
    img_size_op = {}
    for key in diff_img_files_:
        if(diff_img_files_[key] is False):
            img_file1 = os.path.join(os.path.dirname(tmp_img1), key)
            img_file2 = os.path.join(os.path.dirname(tmp_img2), key)
            if(dt["compare_args"]["sliding_window_active"] == "true"):
                img_file2 = tmp_img2
                print("img_file2-downsizeAndEqualizeImages():",img_file2)
                #time.sleep(1)
       
            image1 = Image.open(img_file1)
            image2 = Image.open(img_file2)
            if(image1.size[0] > image2.size[0] or image1.size[1] > image2.size[1]):
                print("image1 is resized")
                #imageA = cv2.resize(imageA, (image1.shape[1], image2.shape[0]))
                image1 = image1.resize((image2.size[0], image2.size[1]))
                image1.save(img_file1)
                image2.save(img_file2)
            if(image2.size[0] > image1.size[0] or image2.size[1] > image1.size[1]):
                print("image2 is resized")
                image2 = image2.resize((image1.size[0], image1.size[1]))
                image1.save(img_file1)
                image2.save(img_file2)
            print("after resize - image1:",image1.size[0],"x",image1.size[1])
            print("after resize - image2:",image2.size[0],"x",image2.size[1])
            if(image1.size == image2.size):
                img_size_op = {key:True}
            else:
                img_size_op = {key:False}
            if(not os.path.exists(img_file1)):
                time.sleep(1)
            if(not os.path.exists(img_file2)):
                time.sleep(1)

    logging.info("downsize and equalizing process...done")
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished with downsizing and equalizing the images in "+ str(elapsed_time) +" minutes....OK")
    return img_size_op   


# updates on 24-Nov-2020 11:50 PM #
def find_aspect_ratio_and_equalize(tmp_img1, tmp_img2, diff_img_files_, dt):
    start_time = time.time()
    logging.info('finding aspect ratio and equalizing the images....')
    img_size_op = {}
    for key in diff_img_files_:
        if(diff_img_files_[key] is False):
            img_file1 = os.path.join(os.path.dirname(tmp_img1), key)
            img_file2 = os.path.join(os.path.dirname(tmp_img2), key)
            if(dt["compare_args"]["sliding_window_active"] == "true"):
                img_file2 = tmp_img2
                print("img_file2:",img_file2)
                #time.sleep(1)
            print("image:",img_file1)
            image1 = Image.open(img_file1)
            image2 = Image.open(img_file2)
            print(image1.size)
            print(image2.size)
            print(image1.size[0],"x", image1.size[1])
            if(image1.size[0] > image2.size[0]):
                print("image1 width resized")
                width_ratio = image2.size[0]/image1.size[0]
                print("ratio:",width_ratio)
                new_height = int(width_ratio * image1.size[1])
                print("new_height",new_height)
                dim = (image2.size[0], new_height)
                print("dim:",dim)
                image1 = image1.resize(dim)
                image1.save(img_file1)
                image2 = resize(img_file2,image1.size[0],image1.size[1])
                image2.save(img_file2)
                print(image1.size)
                print(image2.size)
            if(image1.size[1] > image2.size[1]):
                print("image1 height resized")
                height_ratio = image2.size[1]/image1.size[1]
                new_width = int(height_ratio * image1.size[0])
                dim = (new_width, image2.size[1])
                image1 = image1.resize(dim)
                image1.save(img_file1)
                image2 = resize(img_file2,image1.size[0],image1.size[1])
                image2.save(img_file2)
            if(image2.size[0] > image1.size[0]):
                print("image2 width resized")
                width_ratio = image1.size[0]/image2.size[0]
                new_height = int(width_ratio * image2.size[1])
                dim = (image1.size[0], new_height)
                image2 = image2.resize(dim)
                image2.save(img_file2)
                image1 = resize(img_file1,image2.size[0],image2.size[1])
                image1.save(img_file1)
            if(image2.size[1] > image1.size[1]):
                print("image2 height resized")
                height_ratio = image1.size[1]/image2.size[1]
                new_width = int(height_ratio * image2.size[0])
                dim = (new_width, image1.size[1])
                image2 = image2.resize(dim)
                image2.save(img_file2)
                image1 = resize(img_file1,image2.size[0],image2.size[1])
                image1.save(img_file1)
            print("After resize - image1:",image1.size[0],"x",image1.size[1])
            print("After resize - image2:",image2.size[0],"x",image2.size[1])
            if(image1.size == image2.size):
                img_size_op = {key:True}
            else:
                img_size_op = {key:False}
            if(not os.path.exists(img_file1)):
                time.sleep(1)
            if(not os.path.exists(img_file2)):
                time.sleep(1)

    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finding aspect ratio and equalizing the images in "+ str(elapsed_time) +" minutes....done")
    return img_size_op

# updates on 08-Oct-2020 02:55 AM, 24-Nov-2020 11:50 PM # 
def getFileName(img1, img2, idx, result_list=[],realtime="true"):
    if(len(result_list) > 0 and idx < len(result_list)):
        idx = idx - 1
        #base_ref_file = os.path.join(result_list[idx]["base_img_path"], result_list[idx]["image"])
        #runtime_ref_file = os.path.join(result_list[idx]["runtime_img_path"], result_list[idx]["image"])
        base_ref_file = os.path.join(result_list[0]["base_img_path"], result_list[idx]["image"])
        runtime_ref_file = os.path.join(result_list[0]["runtime_img_path"], result_list[idx]["image"])
        #base_ref_file = os.path.join(result_list[0]["base_img_path"], result_list[0]["image"])
        #runtime_ref_file = os.path.join(result_list[0]["runtime_img_path"], result_list[0]["image"])
        #print("result_list-getFileName():",base_ref_file," ",runtime_ref_file)
        return base_ref_file, runtime_ref_file

    if(realtime != "true"):
        return "", ""
    tmp_ref_file1 = os.path.basename(img1).split('_')
    tmp_img_filepart = tmp_ref_file1[0]
    tmp_img_extpart = tmp_ref_file1[1].split('.')[1]
    tmp_img_filename = tmp_img_filepart+"_"+str(idx)+"."+tmp_img_extpart

    base_ref_file = os.path.join(os.path.dirname(img1),tmp_img_filename)
    runtime_ref_file = os.path.join(os.path.dirname(img2),tmp_img_filename)
    #print("base_ref_file, runtime_ref_file:::::getFileName()",base_ref_file,runtime_ref_file)
    return base_ref_file, runtime_ref_file

# updates on 24-Nov-2020 11:50 PM, 03-Dec-2020 01:20 AM #
def find_diff_sized_realtime_images(img1, img2):
    start_time = time.time()
    logging.info('finding diff sized real-time images....')
    idx = 1
    img_files_ = {}
    missing_imgs_ = {}
    image1 = None
    image2 = None
    comp_result = True
    img1_path = os.path.dirname(img1)
    img2_path = os.path.dirname(img2)
    tmp_ref_file1 = os.path.basename(img1).split('_')
    idx = int(tmp_ref_file1[1].split('.')[0])
    base_ref_file = img1
    runtime_ref_file = img2
    base_img_cnt, runtime_img_cnt = get_img_count(img1_path,img2_path)
    print(base_ref_file)
    print(runtime_ref_file)
    print("find_diff_sized_realtime_images:::::",base_img_cnt,"+++++",runtime_img_cnt)
    if(base_img_cnt != runtime_img_cnt):
        print("image count :: baseline != runtime :",base_img_cnt,"!=",runtime_img_cnt,"....Not OK ")
    while(idx <= base_img_cnt):
        a1 = os.path.exists(base_ref_file) 
        a2 = os.path.exists(runtime_ref_file)
        print("---++++a1:",a1," ",a2)
        if(os.path.exists(base_ref_file) and os.path.exists(runtime_ref_file)):
            image1 = Image.open(base_ref_file)
            image2 = Image.open(runtime_ref_file)
            img_files_[os.path.basename(base_ref_file)] = True
            print("1++++++++++++++++++++++",base_ref_file,"**** ",runtime_ref_file)
        elif(os.path.exists(base_ref_file) is False and os.path.exists(runtime_ref_file)):
            missing_imgs_["B_"+os.path.basename(base_ref_file)] = False
            #print("&&&&&&&&&&","R_"+os.path.basename(base_ref_file))
            #print("2++++++++++++++++++++++",base_ref_file,"**** ",runtime_ref_file)
            idx = idx + 1
            base_ref_file, runtime_ref_file = getFileName(img1,img2,idx,[],"true")
            continue
        elif(os.path.exists(runtime_ref_file) is False and os.path.exists(base_ref_file)):            
            missing_imgs_["R_"+os.path.basename(runtime_ref_file)]  = False
            #print("3++++++++++++++++++++++",base_ref_file,"**** ",runtime_ref_file)
            idx = idx + 1
            base_ref_file, runtime_ref_file = getFileName(img1,img2,idx,[],"true")
            continue

        if(image1.size != image2.size):
            print(base_ref_file, "  size !=  ", runtime_ref_file,"-->",image1.size,"!=",image2.size)
            comp_result = False
            img_files_[os.path.basename(base_ref_file)]  = False
        idx = idx + 1
        base_ref_file, runtime_ref_file = getFileName(img1,img2,idx,[],"true")
        #print("base_ref_file:",base_ref_file)
        #print("runtime_ref_file:",runtime_ref_file)
    #print("img_files_:",img_files_,"&&&&&&",missing_imgs_)
    print(comp_result,img_files_,missing_imgs_)
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("diff sized images count :"+str(len(img_files_)))
    logging.info("done with finding diff sized images in "+ str(elapsed_time) +" minutes....OK")
    print("diff sized images count :"+str(len(img_files_)))
    print("done with finding diff sized images in "+ str(elapsed_time) +" minutes....OK")

    return comp_result, img_files_, missing_imgs_


# updates on 24-Nov-2020 11:50 PM #
def find_diff_sized_nonrealtime_images(img1, img2):
    start_time = time.time()
    logging.info('finding diff sized non-realtime images....')
    img_files_ = {}
    missing_imgs_ = {}
    image1 = None
    image2 = None
    comp_result = True
    images_exist = False
    if(os.path.exists(img1) and os.path.exists(img2)):
        image1 = Image.open(img1)
        image2 = Image.open(img2)
        images_exist = True
        img_files_[os.path.basename(img1)]  = True
    elif(os.path.exists(img1) is False and os.path.exists(img2)):
        missing_imgs_["B_"+os.path.basename(img1)]  = False
    elif(os.path.exists(img1) is False and os.path.exists(img2)):            
        missing_imgs_["R_"+os.path.basename(img2)]  = False

    if(images_exist):
        if(image1.size != image2.size):  
            print(img1, "  size !=  ", img2,"-->",image1.size,"!=",image2.size)
            comp_result = False
            img_files_[os.path.basename(img1)]  = False
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("diff sized images count :"+str(len(img_files_)))
    logging.info("done with finding diff sized images in "+ str(elapsed_time) +" minutes....OK")
    print("diff sized images count :"+str(len(img_files_)))
    print("done with finding diff sized images in "+ str(elapsed_time) +" minutes....OK")
    return comp_result, img_files_, missing_imgs_


# updates on 04-Dec-2020 03:00 AM #
def comp_img_size(img1, img2, realtime):
    comp_result = False
    diff_img_files_ = {}
    missing_imgs_ = {}
    if(realtime == "true"):
        comp_result, diff_img_files_, missing_imgs_ =  find_diff_sized_realtime_images(img1,img2)
        return comp_result, diff_img_files_, missing_imgs_
    if(realtime == "false" or realtime == ""):
        comp_result, diff_img_files_, missing_imgs_ = find_diff_sized_nonrealtime_images(img1,img2)
    return comp_result, diff_img_files_, missing_imgs_ 
   

 # updates on 08-Oct-2020 02:20 AM, 22-Nov-2020 02:15 AM, 24-Nov-2020 11:50 PM, 04-Dec-2020 03:00 AM #
def preprocess_images(dt, result_list, special_state):
    files_copied_to_tmppaths = False
    missing_imgs_ = {}

    # 02-Aug-2021 02:00 AM
    # To limit the scope in v2, the below code block has been introduced. To be removed/enhanced further in v3 based on the requirements
    if(special_state): 
        img1 = str(dt["compare_args"]["baselineImage"])
        img2 = str(dt["compare_args"]["runtime_img_path"])
        return img1, img2, missing_imgs_

    #if(not preprocess_needed):
    #    img1 = str(dt["compare_args"]["baselineImage"])
    #    img2 = str(dt["compare_args"]["runtime_img"])
    #    print("func:preprocess_images:::preprocess_needed:",preprocess_needed)
    #    return img1, img2, missing_imgs_

    if(len(result_list) > 0 and not special_state):
        tmp_img1 = os.path.join(result_list[0]["base_img_path"],result_list[0]["image"])
        tmp_img2 =  os.path.join(result_list[0]["runtime_img_path"],result_list[0]["image"])
        print("File name check::::-::",tmp_img1, tmp_img2)
        return tmp_img1, tmp_img2, missing_imgs_
    else:
        start_time = time.time()
        logging.info('starting the preprocess operation....')

    downsize_op = {}
    realtime = str(dt["compare_args"]["realtime"]).lower()
    img1 = str(dt["compare_args"]["baselineImage"])
    img2 = str(dt["compare_args"]["runtime_img"])
    print("img1:",img1)
    print("img2:",img2)
    mask_area = ""
    mask_area_excl = ""
    if(str(dt["compare_args"]["maskRegion"]) != ""):
        mask_area = str(dt["compare_args"]["maskRegion"])
    elif(str(dt["compare_args"]["maskRegionExcluding"]) != ""):
        mask_area_excl = str(dt["compare_args"]["maskRegionExcluding"])
    debug = str(dt["compare_args"]["intermediate_output"])

    diff_img_path = os.path.join(str(dt["compare_args"]["comp_reports_path"]))
    
    #base_cnt, runtime_cnt = get_img_count(img1,img2,realtime)
    img_size_comp_result, diff_img_files_, missing_imgs_  = comp_img_size(img1,img2,realtime)
    if(img_size_comp_result is False):
        runtime_path = os.path.dirname(img2)
        aspect_ratio_cfg = str(dt["compare_args"]["aspect_ratio_required"])
        tmp_img1, tmp_img2 = getTempFileNames(img1, img2, runtime_path)
        print("tmp_img1:",tmp_img1,"tmp_img2:",tmp_img2)
        print("img1:",img1,"img2:",img2)
        #time.sleep(1)
        copyFiles(diff_img_files_, img1, img2, tmp_img1, tmp_img2, dt)
        files_copied_to_tmppaths = True

        if(aspect_ratio_cfg.lower() == "false"):
            downsize_op = downsizeAndEqualizeImages(tmp_img1,tmp_img2,diff_img_files_,dt)
        else:
            print("diff_img_files:",diff_img_files_)
            downsize_op = find_aspect_ratio_and_equalize(tmp_img1, tmp_img2, diff_img_files_,dt)
    else:
        tmp_img1 = img1
        tmp_img2 = img2

    if(mask_area != "" or mask_area_excl != "") and files_copied_to_tmppaths is False: ###added on 04-Dec-2020 03:00 AM
        runtime_path = os.path.dirname(img2)
        aspect_ratio_cfg = str(dt["compare_args"]["aspect_ratio_required"])
        tmp_img1, tmp_img2 = getTempFileNames(img1, img2, runtime_path)
        copyFiles(diff_img_files_, img1, img2, tmp_img1, tmp_img2, dt)
        files_copied_to_tmppaths = True


    if(mask_area != ""):
        print("masking the defined region....",mask_area)
        apply_mask_parallel(tmp_img1, tmp_img2, mask_area, realtime, debug)
    elif(mask_area_excl != ""):
        print("masking excluding the defined region....",mask_area_excl)
        apply_mask_excluding_region_parallel( tmp_img1, tmp_img2, mask_area_excl, realtime, debug)
    
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished the preprocess operation in "+ str(elapsed_time) +" minutes....OK")
    return tmp_img1, tmp_img2, missing_imgs_



# Updates on : 28-Sep-2020 03:45 PM, 02-Oct-2020 11:10 PM, 03-Oct-2020 01:05 AM, 07-Oct-2020 03:10 PM, 18-Oct-2020 03:45 AM  #
def determine_match_outcome(comp_algo, original_score, eval_operator, dt, exp_score_type="int"):
    if(exp_score_type == "int"):
        algo_exp_score = int(get_algo_expected_score(comp_algo,dt))
    else:
        algo_exp_score = float(get_algo_expected_score(comp_algo,dt))

    print("in determine_match_outcome - exp:",algo_exp_score)
    print("in determine_match_outcome - act",original_score)
    act_score = 723, 734
    exp_score = 720, 735
    0.98 >= 0.95
    2 <= 1
    2 <= 1
    723 >= 720 and 723 <= 735
    734 >= 720 and 734 <= 735
    744 >= 720 and 744 <= 735
    719 >= 720 and 719 <= 735
    1 >= 4

    algo_perf_result_ = False
    if(eval_operator == ">="):
        algo_perf_result_  = bool(original_score >= algo_exp_score)
    elif(eval_operator == "<="):
        print("comp algo:",comp_algo)
        print("^^^^^^^ - original_score:",original_score)
        algo_perf_result_  = bool(original_score <= algo_exp_score)
        print("^^^^^^^ - exp_score:",algo_exp_score)
        print("^^^^^^^ - algo_perf_result:",algo_perf_result_)
    elif(eval_operator == ">"):
        algo_perf_result_  = bool(original_score > algo_exp_score)
    elif(eval_operator == "<"):
        algo_perf_result_  = bool(original_score < algo_exp_score)
    elif(eval_operator == "=="):
        algo_perf_result_  = bool(original_score == algo_exp_score)
    elif(eval_operator == "!="):
        algo_perf_result_  = bool(original_score != algo_exp_score)
    else:
        algo_perf_result_ = False    
    return algo_perf_result_
    
# Updates on : 30-Sep-2020 02:35 AM, 02-Oct-2020 06:15 PM #
def determine_match_within_range(comp_algo, score, max, min, dt):
    #algo_exp_score = get_algo_expected_score(comp_algo,dt)
    if(score >= min and score <= max):
        algo_perf_result_ = True
    else:
        algo_perf_result_ = False    
    return algo_perf_result_


# Updates on 02-Oct-2020 06:30 PM, 03-Oct-2020 07:45 PM #
def get_algo_expected_score(algo,dt):
    #print("get_alg_expected_score - algo name:",algo)
    algos = dt["compare_args"]["similarity"]
    #print("get_alg_expected_score --- alogs:",algos)
    exp_score = ""
    idx = 0
    #print("&&&&&",algos)
    for i in algos:
        #print(list(i.values())[0])
        #print(list(i.values())[1])
        #print("i-",i)
        #print("algo-",idx,"***",i[0]['method1'])
        #print("algo-",idx,"***",i[0]['m1_score'])
        #print("#################")
        #idx=idx+1
        if(str(list(i.values())[0])==algo):
            exp_score = str(list(i.values())[1])
            print("exp_score::::get_algo_exp_score():",exp_score)
            #time.sleep(3)
            #print("match found for algo-name:",str(list(i.values())[0]))
            #print("match found for algo-score:",exp_score)
    if(exp_score==""):
        print("algo : ",algo ," was not found...selecting default : SSI")
        for i in algos:
            if(str(list(i.values())[0])==comp_algos.ssi):
                exp_score = str(list(i.values())[1])
    return exp_score


def resize_pad(image, width,height):
    # read image
    img = cv2.imread(image)
    ht, wd, cc= img.shape
    print("img size: h-",ht," w-",wd)

    # create new image of desired size and color (blue) for padding
    #ww = 1920
    ##hh = 1080
    #(ww,hh) = pygui.size()
    ww = width
    hh = height

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
    cv2.imwrite("D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/resized-pad-1.png", result)




#resiz("D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/body_1.png",1200,600)
#resize_pad('D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/resized-1.png',448,44)
#file1="D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/body_1.png"
#file2="D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/body-resized-1.png"

#file1 = "D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/104244__B.png"
#file2 = "D:/Automation/DW/SDV/src/test-inputs/images/login/realtime/chrome/baseline/104244__A.png"
#SSI_Compare(file1,file2)