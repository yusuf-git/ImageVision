# Author : Yusuf
# Created Date : 19-Jul-2020 02:00 AM
# Updates on : 02-Aug-2020 05:15 AM, 03-Aug-2020 02:00 AM, 04-Aug-2020 03:05 AM, 08-Dec-2020 03:30 PM, 10-Dec-2020 03:10 AM, 08:30 PM, 11-Dec-2020 02:00 AM, 13-Dec-2020 02:10 AM, 14-Dec-2020 02:00 AM, 17-Dec-2020 02:00 AM, 12:00 PM to 08:00 PM, 21-Dec-2020 01:45 AM, 22-Dec-2020 12:15 PM to 11:00 PM, 24-Dec-2020 02:20 PM to 05:00 PM, 25-Dec-2020 06:00 PM to 08:45 PM
######################################

import logging
import sys
#sys.path.insert(0,"C:\Program Files\Python-3.7.4\Lib\site-packages")
from shutil import copyfile
#import pyExp
#sys.path.insert(0,"C:\Program Files\Python-3.7.4\Lib\site-packages\pyautogui")
#sys.path.insert(0,"C:\Program Files\Python-3.7.4\Lib\site-packages\PIL")
#sys.path.insert(0,"C:\Program Files\Python-3.7.4\Lib\site-packages\pyscreeze")
#sys.path.insert(0,"C:\Program Files\Python-3.7.4\Lib\site-packages\pyscreenshot")
#import pyautogui
import argparse
import datetime
import os.path
import time
import json
import traceback
#import numpy as np
import cv2
from PIL import ImageGrab
from PIL import Image
import numpy as np
#import pyscreenshot as ImageGrab
#import matplotlib.pyplot as plt
#filepath = "D:/SDV/scr.jpg"

def del_file(file):
    result = False
    if not os.path.exists(file):
        print(f'Baseline overwrite --> Img : {file} is not located for deletion...delete operation result = True')
        logging.info(f'Baseline overwrite --> Img : {file} is not located for deletion...delete operation result = True')
        return True
    folder = os.path.dirname(file)
    curr_file = ""
    for filename in os.listdir(folder):
        curr_file = os.path.join(folder, filename)
        try:
            if (os.path.isfile(curr_file) or os.path.islink(curr_file)) and curr_file == file:
                #print(f'Baseline overwrite --> Img : {file}. Located the file for deletion....deleting...')
                #logging.info(f'Baseline overwrite --> Img : {file}. Located the file for deletion....deleting...')
                #tmp_copy = os.path.join(os.path.dirname(curr_file), "bb_"+os.path.basename(curr_file))
                #copyfile(curr_file,tmp_copy)
                os.unlink(curr_file)
                print(f'Baseline overwrite --> Img : {file}. Deleted...OK')
                logging.info(f'Baseline overwrite --> Img : {file}. Deleted...OK')
                return True
            #elif os.path.isdir(file_path):
            #    shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (curr_file, e))
            logging.error('Failed to delete %s. Reason: %s' % (curr_file, e))
            result=False
            #writeToFile("dir_deletion_exception.txt",'Failed to delete %s. Reason: %s' % (file_path, e))
    #workspace_base = folder
    if(os.path.exists(file)):
        logging.error(f'{file} still exists')
        result = False
    else:
        logging.info(f'{file} has been deleted')
        result = True
    return result


def readJson(jsonFile_):
    f_ = open(jsonFile_) 
    data_ = json.load(f_) 
    f_.close()
    return data_


def writeResult(res_json_file, result, msg, dt):
    imgfile = str(dt["args"][0]["imgFile"])
    imgArchivesPath = str(dt["args"][0]["imgArchivesPath"])
    baselineApproval = str(dt["args"][0]["approvedAsBaseline"])
    baselineImage = str(dt["args"][0]["baselineImage"])
    result_path = str(dt["args"][0]["resultPath"])
    baseline_path = os.path.dirname(baselineImage)
    ##fname = os.path.basename(res_json_file)
    fname = str(res_json_file).split(".")[0]
    #resFile = os.path.join(result_path, str(fname)+"-cap.json")
    if(os.path.exists(res_json_file)):
        x = datetime.datetime.now()
        dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
        #resFile = os.path.join(result_path, str(fname) + "-cap-" + dt_part + ".json")
        res_json_file = os.path.join(str(fname) + "_" + dt_part + ".json")
    tmp_img_file = os.path.basename(imgfile)
    tmp_runtime_path = os.path.dirname(imgfile)
    resultStr = {"img":tmp_img_file, "baseline_path":baseline_path, "runtime_path":tmp_runtime_path, "result":result, "message":msg, "result_path":result_path }
    resJson = json.dumps(resultStr, indent=4)
    with open(res_json_file,"w") as json_out:
        json_out.write(resJson)


def get_log_filename(dt):
    imgfile = str(dt["args"][0]["imgFile"])
    result_path = str(dt["args"][0]["resultPath"])
    fname = os.path.basename(imgfile)
    fname = str(fname).split(".")[0]
    log_file = os.path.join(result_path, str(fname)+"_grab.log")
    if(os.path.exists(log_file)):
        x = datetime.datetime.now()
        dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
        log_file = os.path.join(result_path, str(fname) + dt_part + "_grab.log")
    return log_file



def getFileName(imgfile_, dt_, idx_):
    fname_ = ""
    if(str(dt_["args"][0]["realtime"]).lower() == "true" ):
        tmp_fname = imgfile_.split('.')
        fname_ = tmp_fname[0] + "_" + str(idx_) + "." + tmp_fname[1]
        print(fname_)
    else:
        fname_ = imgfile_
    return fname_


def calc_x2_y2(c_y2_, c_x2_, im_):
    if(str(c_y2_) == "len(height)"):
          c_y2_ = im_.shape[0]
    if(str(c_x2_) == "len(width)"):
          c_x2_ = im_.shape[1]
    return c_y2_, c_x2_


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


def readCycles(realtimeImgGrabDurationMins_, def_cycles, interval_, realtime_):
    if(realtimeImgGrabDurationMins_ > 0.0 and realtime_ == "true" ):
        cnt_ = (realtimeImgGrabDurationMins_ * 60) / interval_
        print("Image collection mode : time-bound. Total img count:",int(cnt_))
    else:
        cnt_ = def_cycles
    return int(cnt_)


def handle_mask(imgname,img,dt):
    mask_excluded = str(dt["args"][0]["maskRegionExcluding"])
    maskarea =  str(dt["args"][0]["maskRegion"])
    masked = None
    if(mask_excluded == "" and maskarea == ""):
        return img
    pil_image = img.convert('RGB') 
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    if(mask_excluded != ""):
        masked = apply_mask_exclude_region(imgname, open_cv_image,dt)
        pil_img = convert_openCV_to_PIL_Image(masked)
        return pil_img
    if(maskarea != ""):
        masked = apply_mask(imgname, open_cv_image, dt)
        pil_img = convert_openCV_to_PIL_Image(masked)
        return pil_img


def convert_openCV_to_PIL_Image(img):
    pil_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(pil_img)
    return pil_img


def convert_PIL_Image_to_openCV(img):
    pil_image = img.convert('RGB') 
    open_cv_image = np.array(pil_image) 
    # Convert RGB to BGR 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    return open_cv_image


def apply_mask_exclude_region(imgname, img, dt):
    mask_excluded = str(dt["args"][0]["maskRegionExcluding"])
    c_x1,c_y1,c_x2,c_y2 = readMaskArea(mask_excluded)
    (c_y2, c_x2) = calc_x2_y2(c_y2,c_x2,img)
    
    mask_ = np.zeros(img.shape[:2], dtype = "uint8")
    #print("image : ",img1_fname," --> width, height, channel:", w, h, c)
    cv2.rectangle(mask_, (int(c_x1), int(c_y1)), (int(c_x2), int(c_y2)), (255,0,0), -1)
    masked_ = cv2.bitwise_and(img, img, mask = mask_)
    print("applied mask - img:"+imgname+", mask region excluded:"+c_x1,c_y1,c_x2,c_y2)
    return masked_


def apply_mask(imgname, img, dt):
    maskarea = str(dt["args"][0]["maskRegion"])
    c_x1,c_y1,c_x2,c_y2 = readMaskArea(maskarea)
    (c_y2, c_x2) = calc_x2_y2(c_y2,c_x2,img)
  
    #print("image : ",img1_fname," --> width, height, channel:", w, h, c)
    masked_image = img
    masked_image[int(c_y1):int(c_y2),int(c_x1):int(c_x2)] = (0,0,0)
    print("applied mask - img:"+imgname+", mask region:"+c_x1,c_y1,c_x2,c_y2)
    return masked_image


def get_interval_config(realtime, dt):
    interval = str(dt["args"][0]["interval"])
    if(realtime == "true" and (interval == "" or interval == "0" or interval == "0.0")):
        interval = "1.0"
    if(interval == "" and realtime == "false"):
        interval = "0.0"
    interval = float(interval)
    return interval


def get_capture_duration(realtime, cycles, dt):
    realtimeImgGrabDurationMins = dt["args"][0]["realtimeImgGrabDurationMins"]
    if(realtime == "true" and (realtimeImgGrabDurationMins == "" or realtimeImgGrabDurationMins == "0" or realtimeImgGrabDurationMins == "0.0") and (cycles == "" or cycles == "0")):
        realtimeImgGrabDurationMins = "1.0"
    
    if(realtime == "true" and (realtimeImgGrabDurationMins == "" or realtimeImgGrabDurationMins == "0" or realtimeImgGrabDurationMins == "0.0") and (cycles != "")):
        realtimeImgGrabDurationMins = "0.0"

    if(realtimeImgGrabDurationMins == "" and realtime == "false"):
        realtimeImgGrabDurationMins = "0.0"
    realtimeImgGrabDurationMins = float(realtimeImgGrabDurationMins)
    return realtimeImgGrabDurationMins


def get_cycles(dt):
    cnt = 0
    if(len(str(dt["args"][0]["cycles"])) == 0):
        cnt = 0
    elif(len(str(dt["args"][0]["cycles"])) >= 1 ):
        cnt = int(dt["args"][0]["cycles"])
    return cnt


def handle_baselining_messages(loc_cnt, src, dest, msg):
    print("====================")
    print(f'{str(loc_cnt)}. {msg}')
    print(f'source : {src}')
    print(f'destination:{dest}')
    print("====================")


def evaluate_baseline_preexists(src, base_file, overwritten_cnt, loc_cnt):
    if not del_file(base_file):
        print(f'Img name {base_file} : the previous baseline was not deleted....logging the error')
        logging.error(f'Img name {base_file} : the previous baseline was not deleted...logged the error')
        #return False
    copyfile(src, base_file)
    overwritten_cnt = overwritten_cnt + 1
    handle_baselining_messages(loc_cnt,src,base_file,'Overwritten the previous baseline')
    return overwritten_cnt


def evaluate_baseline_preexists_no_overwrite(src, base_file, not_overwritten_cnt, loc_cnt):
    not_overwritten_cnt = not_overwritten_cnt + 1
    handle_baselining_messages(loc_cnt,src,base_file,'Baseline already exists, but overwrite not configured')
    return not_overwritten_cnt


def evaluate_new_baseline(src, base_file, newfile_cnt, loc_cnt):
    copyfile(src, base_file)
    newfile_cnt = newfile_cnt + 1
    handle_baselining_messages(loc_cnt,src,base_file,'New baseline done')
    return newfile_cnt


def log_baseline_messages(overwritten_cnt, not_overwritten_cnt, newfile_cnt):
    logging.info(f'baseline - total overwritten     :{overwritten_cnt}')
    logging.info(f'baseline - total retained        :{not_overwritten_cnt}')
    logging.info(f'baseline - total newly baselined :{newfile_cnt}')


def evaluate_baseline_result(overwritten_cnt, not_overwritten_cnt, newfile_cnt, runtimeImgList):
    if((overwritten_cnt+not_overwritten_cnt+newfile_cnt) == len(runtimeImgList)):
        print("Baselining process result : true")
        logging.info("Baselining process result : true")
        return True
    else:
        print("Baselining process result : false")
        logging.error("Baselining process result : false")
        return False

def do_baselining_tasks(overwriteBaseline):
    overwritten_cnt = 0
    not_overwritten_cnt = 0
    newfile_cnt = 0
    loc_cnt = 1

    if(str(baselineApproval).lower() == "false"):
        return True

    for el in runtimeImgList:
        fname = os.path.basename(el)
        baseimg_path = os.path.dirname(baselineImage)
        base_file = os.path.join(baseimg_path, fname)
        if(overwriteBaseline.lower() == "true" and os.path.exists(base_file)):
           overwritten_cnt = evaluate_baseline_preexists(el, base_file, overwritten_cnt, loc_cnt)
            
        if(overwriteBaseline.lower() == "false" and os.path.exists(base_file)):
            not_overwritten_cnt = evaluate_baseline_preexists_no_overwrite(el, base_file, not_overwritten_cnt, loc_cnt)
            
        if(not os.path.exists(base_file)):
            newfile_cnt = evaluate_new_baseline(el, base_file, newfile_cnt, loc_cnt)
        loc_cnt = loc_cnt + 1
            
    log_baseline_messages(overwritten_cnt, not_overwritten_cnt, newfile_cnt)
    result = evaluate_baseline_result(overwritten_cnt, not_overwritten_cnt, newfile_cnt, runtimeImgList)
    return result



def copyToBaseline(runtimeImgList, dt):
    baselineApproval = str(dt["args"][0]["approvedAsBaseline"])
    baselineImage = str(dt["args"][0]["baselineImage"])
    overwriteBaseline = dt["args"][0]["overwriteBaseline"]
    if(str(baselineApproval).lower() == "false" or str(baselineApproval) == ""):
        print("baselineApproval == false, copyToBaseline true")
        return True
    if((len(runtimeImgList) == 0 or runtimeImgList is None) and str(baselineApproval).lower() == "true"):
        print("runtimeimglist == 0 or none")
        return False
    do_baselining_tasks(overwriteBaseline)
    

def get_result_file(dt):    
    imgfile = str(dt["args"][0]["imgFile"])
    result_path = str(dt["args"][0]["resultPath"])
    fname = os.path.basename(imgfile)
    fname = str(fname).split(".")[0]
    resFile = os.path.join(result_path, str(fname)+"-cap.json")    
    return resFile        




result = False
message=""
imgfile_g=""
imgArchivesPath=""
dt = None
try:
    #global imgfile_g
    #global message
    ##global result
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json", required=True, help="json arg file name")
    args = vars(ap.parse_args())
    #pyautogui.screenshot(args["file"])
    #im = pyautogui.screenshot(region=(20,50,500,550))
    dt = readJson(args["json"])
    print("ImageVision v6 - ImageCreative module activated....")
    logfile = get_log_filename(dt)
    logging.basicConfig(filename=logfile, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.INFO)

    imgfile = str(dt["args"][0]["imgFile"])
    imgArchivesPath = str(dt["args"][0]["imgArchivesPath"])
    imgfile_g = imgfile
    realtime = str(dt["args"][0]["realtime"]).lower()
    cnt = get_cycles(dt)
    realtimeImgGrabDurationMins = get_capture_duration(realtime, cnt, dt)
    interval = get_interval_config(realtime, dt)
    
    cnt = readCycles(realtimeImgGrabDurationMins, cnt, interval, realtime)
    # x1=int(dt["args"][0]["x1"])
    # y1=int(dt["args"][0]["y1"])
    # x2=int(dt["args"][0]["x2"])
    # y2=int(dt["args"][0]["y2"])
    x1=int(dt["args"][0]["x1"].split(".")[0])
    y1=int(dt["args"][0]["y1"].split(".")[0])
    x2=int(dt["args"][0]["x2"].split(".")[0])
    y2=int(dt["args"][0]["y2"].split(".")[0])
    ##print(x1," ",y1," ",x2," ",y2)

    baselineApproval = str(dt["args"][0]["approvedAsBaseline"])
    baselineImage = str(dt["args"][0]["baselineImage"])
    
    
    j=1
    runtimeImgList = []

    while j <= int(cnt):
        #im = pyautogui.screenshot(region=(int(args["tlx"]),int(args["tly"]),args["brx"],args["bry"]))
        #im = ImageGrab.grab(bbox=(int(args["tlx"]),int(args["tly"]),int(args["brx"]),int(args["bry"])))  # X1,Y1,X2,Y2
        img = ImageGrab.grab(bbox=(x1,y1,x2,y2))  # X1,Y1,X2,Y2
        runtime_fname=getFileName(imgfile,dt,j)
        #h,w,c = img.shape

        img = handle_mask(runtime_fname, img, dt)
        img.save(runtime_fname)
        #cv2.imwrite(runtime_fname,img)
        runtimeImgList.append(runtime_fname)
        
        j = j+1
        print(f'created runtime image :{runtime_fname}')
        time.sleep(interval)
    
    print(f'done with image grab -> count :{j}')
    logging.info(f'done with image grab -> count :{j}')
    j=1
    result = True
    message = "OK"
    copyRes = copyToBaseline(runtimeImgList, dt)
    if(copyRes is False):
        result = False
        message = "Copy to baseline failed"
    
except:
    #exc_traceback = sys.exc_info()
    #print("exception in capturesnap.py ",sys.exc_info())
    result=False
    message=str(sys.exc_info())
    print(traceback.format_exc())
    #print("*** tb_lineno:", exc_traceback.lineno)
    
finally:
    print("image creation operation result | msg:"+str(result) + " | " +message)
    resfile = get_result_file(dt)
    print("result file_py:",resfile)
    if(result == True):
        #writeResult(imgfile_g, "true", message, os.path.dirname(imgfile_g))
        writeResult(resfile, "true", message, dt)
    else:
        writeResult(resfile, "false", message, dt)
    if(os.path.exists(resfile)):
        print("resfile:",resfile," exists")
    else:
        print("resfile:",resfile," not exists")
    print("result file name - check - py:",resfile)
    print("*********************************************")
    print("imagevision v1 operation....completed")
    print("*********************************************")
    

##class ImageSubclass(ImageGrab):





#ap.add_argument("-f", "--file", required=True, help="File Name")
#ap.add_argument("-c", "--cycles", required=False, default="1", help="No. of iterations")
#ap.add_argument("-i", "--interval", required=False, default="1", help="Interval between iterations")
#ap.add_argument("-tx", "--tlx", required=True, help="Top left x coord")
#ap.add_argument("-ty", "--tly", required=True, help="Top left y coord")
#ap.add_argument("-bx", "--brx", required=True, help="Bottom right x coord")
#ap.add_argument("-by", "--bry", required=True, help="Bottom right y coord")
