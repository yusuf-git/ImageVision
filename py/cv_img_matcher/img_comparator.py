#/############################################################
# Author : Yusuf
# Date & Time : 19-Apr-2020 12:00 AM To 06:30 AM, 21-Apr-2020 03:10 AM, 01-May-2020 05:00 AM to 8:00 AM, 16-Aug-2020 07:00 PM, 28-Sep-2020 04:40 PM, 29-Sep-2020 02:45 AM, 30-Sep-2020 02:45 AM, 03-Oct-2020 01:30 AM, 06-Oct-2020 08:15 PM, 11-Oct-2020 02:30 PM to 11:50 PM, 12-Oct-2020 02:00 AM, 13-Oct-2020 04:00 AM, 14-Oct-2020 04:10 AM, 15-Oct-2020 03:20 AM, 16-Oct-2020 02:45 AM, 17-Oct-2020 03:10 AM, 18-Oct-2020 03:45 AM, 28-Jul-2021 01:30 AM, 31-Jul-2021 09:00 AM to 11:55 PM, 07-Aug-2021 11:55 PM, 24-Oct-2021 02:50 AM, 21-Nov-2011 01:00 PM to 09:45 PM
###############################################################
# create a thumbnail of an image
from posixpath import split
import sys
import os

from numpy.lib.function_base import diff
sys.path.insert(0, os.path.realpath(os.path.pardir))
from genericpath import exists
from os import mkdir
import logging
import time
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
from matplotlib import pyplot as plt
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils
import imagehash
from skimage.measure import compare_ssim
import pyautogui as pygui
from cv_img_libs import img_comp_utils
from cv_img_matcher.algos_namelist import comp_algos
from data_models.hang_issue_checker_data_model import hang_issue_checker_data_model
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from cv_img_libs import gen_utils
from cv_img_libs import BF_baseline_eval_mgmt_utils


tasks = {}
task = lambda f: tasks.setdefault(f.__name__, f)

# Created on 07-Aug-2021 07:15 PM
def log_diff_files(diff_file_cnt, special_state):
    if special_state:
        return
    if(diff_file_cnt > 0):
        logging.info("total diff files created for mismatches :{0}".format(diff_file_cnt))
    else:
        logging.info("no mismatches --> no diff files created  :{0}".format(diff_file_cnt))


# Created on 07-Aug-2021 07:45 PM
def write_diff_file(score, diff_file, img2, diff_file_cnt, special_state):
    #if(special_state):
    #    return diff_file_cnt
    if(score < 1.0):
        print("ssi-->score < 1. diff_file:",diff_file)
        cv2.imwrite(diff_file,img2)
        diff_file_cnt = diff_file_cnt + 1
        return diff_file_cnt
    return diff_file_cnt

# Updates on 02-Oct-2020 09:45 PM, 03-Oct-2020 01:05 AM, 08:00 PM, 18-Oct-2020 03:45 AM, 22-Nov-2020 11:45 AM to 11:00 PM #
#@task
def SSI_compare(dt, result_list, special_state):
    start_time = time.time()
    logging.info("##############################################################")
    logging.info("active algo : structural similarity index")
    logging.info("##############################################################")
    result_dict = {}
    diff_file_cnt = 0
    result_msg = ""
    algo_perf_result = ""
    missing_imgs_added_to_result = False
    realtime = str(dt["compare_args"]["realtime"]).lower()
    #diff_path = str(dt["compare_args"]["comp_reports_path"])
    debugging = str(dt["compare_args"]["intermediate_output"])
    diff_path = get_diff_path(dt, result_list, "ssi", special_state)

    print('')
    print('')
    print('')
    print("##############################################################")
    print("active algo : structural similarity index")
    print("##############################################################")
    # get expected score for the current algo #
    algo_exp_score = float(img_comp_utils.get_algo_expected_score(comp_algos.ssi,dt))
    img_file1, img_file2, missing_imgs_  = img_comp_utils.preprocess_images(dt, result_list, special_state)
    print(img_file1, img_file2)
    print("SSI:check temp paths")
    #time.sleep(15)
    #time.sleep(5)
    idx, base_img_cnt = get_idx_baseimgcnt(realtime, img_file1, img_file2, result_list)
    print("base_img_cnt:",base_img_cnt)
    base_path = os.path.dirname(img_file1)
    runtime_path = os.path.dirname(img_file2)
    print("base_path",base_path)
    print("runtime_path",runtime_path)
    base_cnt, runtime_cnt = img_comp_utils.get_img_count(base_path,runtime_path,result_list)
    print("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    print("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    logging.info("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    logging.info("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    while(idx <= base_img_cnt):
        b_tmp_fname = "B_"+os.path.basename(img_file1)
        r_tmp_fname = "R_"+os.path.basename(img_file2)
        print("SSI --> current image ::"+img_file1)
        if(b_tmp_fname in missing_imgs_):
            #if(idx==1):
            imageops.image_match_outcome_list.append(imageops(b_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "SSI", algo_exp_score, "-999.99", False, "missing baseline"))
            #elif(idx > 1):
            #imageops.image_match_outcome_list.append(imageops(b_tmp_fname, "", "", "SSI", algo_exp_score, "-999.99", False, "missing baseline"))
            #di_container.image_match_outcome_dict[b_tmp_fname] = {"no score":"no image"}
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing baseline img:"+b_tmp_fname)
            continue
        elif(r_tmp_fname in missing_imgs_):
            imageops.image_match_outcome_list.append(imageops(r_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "SSI", algo_exp_score, "-999.99", False, "missing runtime"))
            #elif(idx > 1):
            #imageops.image_match_outcome_list.append(imageops(r_tmp_fname, "", "", "SSI", algo_exp_score, "-999.99", False, "missing runtime"))
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing runtime img:"+r_tmp_fname)
            continue

        diff_file = get_diff_file(diff_path,img_file1,img_file2,special_state)
        #print(img_file1,"  ",img_file2)
        #time.sleep(10)
        img1 = cv2.imread(img_file1)
        img2 = cv2.imread(img_file2)
        
        grayA = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        #(score, diff) = compare_ssim(grayA, grayB, full=True)
        (score, diff) = ssim(grayA, grayB, multichannel = True, full=True)
        diff = (diff * 250).astype("uint8")
        thresh = cv2.threshold(diff, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
	        (x, y, w, h) = cv2.boundingRect(c)
	        #cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 155), 2)
	        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 155), 2)
        diff_file_cnt = write_diff_file(score, diff_file, img2, diff_file_cnt, special_state)


            #cv2.rectangle(diff, (x, y), (x + w, y + h), (0, 0, 155), 2)
            #fileName = str(Path(str(baseline)).resolve())//throws OS error
            #print("diff_"+desc)
            #cv2.imwrite(diff_file,img2)
            
        if(debugging=="true"):
            cv2.imshow("Original", img1)
            cv2.imshow("Runtime", img2)
            cv2.imshow("Diff", diff)
            #cv2.imshow("Thresh", thresh)
            cv2.waitKey(0)
        result_msg = str(score)
        score = round(score,2)
        print("Match similarity (1.0 = 100% match): {}".format(score))
        #algo_exp_score = img_comp_utils.get_algo_expected_score(comp_algos.perceptual_hashing,dt)
        if(not special_state):
            algo_perf_result = img_comp_utils.determine_match_outcome(comp_algos.ssi, score, ">=", dt, "float")
        else:
            algo_perf_result = img_comp_utils.determine_match_outcome(comp_algos.ssi, score, "<=", dt, "float")
        #print("SSI_compare:algo_perf_result-1:",algo_perf_result)
        result_dict = {os.path.basename(img_file1):{score:algo_perf_result}}
        gen_utils.console_verbose_out("Match result :{}".format(result_dict),dt)
        print("##############################################################")
        result_msg = build_result_msg(algo_perf_result, result_msg, special_state)
        #if(idx==1):
        #time.sleep(2)
        if(not special_state):
            imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "SSI", algo_exp_score, str(score), algo_perf_result, result_msg))
        else:
            hang_issue_checker_data_model.tmp_img_match_result_list.append(hang_issue_checker_data_model(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "SSI", algo_exp_score, str(score), algo_perf_result, result_msg))
            #time.sleep(4)
        #elif(idx > 1):
        #imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), "", "", "SSI", algo_exp_score, str(score), algo_perf_result, ""))
        #di_container.image_match_outcome_dict[os.path.basename(img_file1)] = {score:algo_perf_result}
        idx = idx + 1
        if(special_state or dt["compare_args"]["sliding_window_active"] == "true"):
            break
        img_file1, img_file2 = img_comp_utils.getFileName(img_file1, img_file2, idx, result_list, realtime)
        
        #print("Final comp result::p-hashing: ",di_container.image_match_outcome_dict)
        
    #di_container.image_match_outcome_dict = result_dict
    if(missing_imgs_added_to_result == False and missing_imgs_ is not None):
        for key in missing_imgs_:
            if key not in missing_imgs_.values():
                #if(idx==1):
                imageops.image_match_outcome_list.append(imageops(key, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "SSI", algo_exp_score, "-999.99", False, "missing image"))
                logging.error("missing img:"+img_file1)
                #elif(idx > 1):
                #imageops.image_match_outcome_list.append(imageops(key, "", "", "SSI", algo_exp_score, "-999.99", False, "missing image"))
            #di_container.image_match_outcome_dict[key] = {"no score":"no image"}
    if(debugging=="true"):
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("******************cumulative match result --> algo :: SSI*****************************",dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("Is it correct:?{}".format(imageops.image_match_outcome_list),dt)      
        gen_utils.console_verbose_out("****************************************************************************************",dt)        #print("Exp-result_dict::Final comp result::p-hashing: ",result_dict)
    logging.info("##############################################################")
    elapsed_time = round((time.time() - start_time)/60,2)
    log_diff_files(diff_file_cnt,special_state)

    logging.info("finished the SSI algo operation in "+ str(elapsed_time) +" minutes...OK")
    logging.info("##############################################################")
    logging.info("")
    logging.info("")
    logging.info("")
    #print("before returning....",imageops.image_match_outcome_list)
    #time.sleep(6)
    return imageops.image_match_outcome_list, hang_issue_checker_data_model.tmp_img_match_result_list

 # updates on 22-Nov-2020 11:45 AM to 11:00 PM #
#@task
def perceptual_hash_match(dt, result_list, special_state):
    start_time = time.time()
    logging.info("##############################################################")
    logging.info("active algo : p-hash")
    logging.info("##############################################################")
    result_dict = {}
    result_msg = ""
    algo_perf_result = ""
    missing_imgs_added_to_result = False
    realtime = str(dt["compare_args"]["realtime"]).lower()
    #diff_path = str(dt["compare_args"]["comp_reports_path"])
    debugging = str(dt["compare_args"]["intermediate_output"])
    hashsize = str(dt["compare_args"]["p_hash_parametric"]["hash_size"])
    diff_path = get_diff_path(dt, result_list, "phash", special_state)
    print('')
    print('')
    print('')
    print("##############################################################")
    print("active algo : perceptual_hashing")
    print("##############################################################")
    # get expected score for the current algo #
    algo_exp_score = int(img_comp_utils.get_algo_expected_score(comp_algos.perceptual_hashing,dt))
    img_file1, img_file2, missing_imgs_  = img_comp_utils.preprocess_images(dt, result_list, special_state) #########
    #img_file1, img_file2, missing_imgs_  = img_comp_utils.preprocess_images(dt, result_list, special_state)

    idx, base_img_cnt = get_idx_baseimgcnt(realtime, img_file1, img_file2, result_list)
    base_path = os.path.dirname(img_file1)
    runtime_path = os.path.dirname(img_file2)
    base_cnt, runtime_cnt = img_comp_utils.get_img_count(base_path,runtime_path,result_list)
    print("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    print("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    logging.info("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    logging.info("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")###")
    while(idx <= base_img_cnt):
        b_tmp_fname = "B_"+os.path.basename(img_file1)
        r_tmp_fname = "R_"+os.path.basename(img_file2)
        print("phash --> current image ::"+img_file1)
        if(b_tmp_fname in missing_imgs_):
            imageops.image_match_outcome_list.append(imageops(b_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "perceptual_hashing", algo_exp_score, "-999.99", False, "missing baseline"))
            #di_container.image_match_outcome_dict[b_tmp_fname] = {"no score":"no image"}
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing baseline img:"+b_tmp_fname)
            continue
        elif(r_tmp_fname in missing_imgs_):
            #print("Missing runtime image :",r_tmp_fname.replace("R_",""))
            imageops.image_match_outcome_list.append(imageops(r_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "perceptual_hashing", algo_exp_score, "-999.99", False, "missing runtime"))
            #di_container.image_match_outcome_dict[r_tmp_fname] = {"no score":"no image"}
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing runtime img:"+r_tmp_fname)
            continue

        diff_file = os.path.join(diff_path,"diff_"+os.path.basename(img_file1))
        if(len(hashsize) > 0):
            baseline_hash = imagehash.phash(Image.open(img_file1),int(hashsize))
            actual_hash = imagehash.phash(Image.open(img_file2),int(hashsize))
        else:
            baseline_hash = imagehash.phash(Image.open(img_file1))
            actual_hash = imagehash.phash(Image.open(img_file2))
        distance = baseline_hash - actual_hash        
        if(baseline_hash == actual_hash):
            print("P-hashing ::",os.path.basename(img_file1),": baseline == runtime. Score =",distance)
        else:
            print("P-hashing ::",os.path.basename(img_file1),": baseline != runtime. Score =",distance)
        
        #distance = round(score,2)
        print("p-hash match distance (0 = 100% match): {}".format(distance))
        if(not special_state):
            algo_perf_result = img_comp_utils.determine_match_outcome(comp_algos.perceptual_hashing, distance, "<=", dt)
        else:
            algo_perf_result = img_comp_utils.determine_match_outcome(comp_algos.perceptual_hashing, distance, ">=", dt)
        result_dict = {os.path.basename(img_file1):{distance:algo_perf_result}}
        gen_utils.console_verbose_out("Match result :{}".format(result_dict),dt)
        print("##############################################################")
        result_msg = build_result_msg_for_hashings(algo_perf_result, hashsize, special_state)

        if(not special_state):
            imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "p-hash", algo_exp_score, str(distance), algo_perf_result, result_msg))
            #print("imageops model : p-hash")
            #print("p-jash result:",imageops.image_match_outcome_list)
            #time.sleep(3)
            #print("=======================================================================")
        else:
            hang_issue_checker_data_model.tmp_img_match_result_list.append(hang_issue_checker_data_model(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "p-hash", algo_exp_score, str(distance), algo_perf_result, result_msg))
        #di_container.image_match_outcome_dict[os.path.basename(img_file1)] = {score:algo_perf_result}
        idx = idx + 1
        if(special_state or dt["compare_args"]["sliding_window_active"] == "true"):
            break
        img_file1, img_file2 = img_comp_utils.getFileName(img_file1, img_file2, idx, result_list, realtime)
        
        
    if(missing_imgs_added_to_result == False and missing_imgs_ is not None):
        for key in missing_imgs_:
            if key not in missing_imgs_.values(): 
                imageops.image_match_outcome_list.append(imageops(key, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "perceptual_hashing", algo_exp_score, "-999.99", False, "missing image"))
                logging.error("missing img:"+img_file1)
    if(debugging=="true"):        
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("******************cumulative match result --> algo :: perceptual-hashing*****************************",dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("Is it correct:?{}".format(imageops.image_match_outcome_list),dt)      
        gen_utils.console_verbose_out("****************************************************************************************",dt)    
    logging.info("##############################################################")
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished the p-hashing algo operation in "+ str(elapsed_time) +" minutes...OK")
    logging.info("##############################################################")
    #print("p-hash - for debugging:",imageops.image_match_outcome_list)
    #time.sleep(5)
    return imageops.image_match_outcome_list, hang_issue_checker_data_model.tmp_img_match_result_list


# updates on 22-Nov-2020 11:45 AM to 11:00 PM #
#@task
def diff_hash_match(dt, result_list, special_state):
    start_time = time.time()
    logging.info("##############################################################")
    logging.info("active algo : d-hashing")
    logging.info("##############################################################")
    result_dict = {}
    result_msg = ""
    missing_imgs_added_to_result = False
    realtime = str(dt["compare_args"]["realtime"]).lower()
    #diff_path = str(dt["compare_args"]["comp_reports_path"])
    debugging = str(dt["compare_args"]["intermediate_output"])
    hashsize = str(dt["compare_args"]["d_hash_parametric"]["hash_size"])
    diff_path = get_diff_path(dt, result_list, "dhash", special_state)
    print('')
    print('')
    print('')
    print("##############################################################")
    print("active algo : differential_hashing")
    print("##############################################################")
    # get expected score for the current algo #
    algo_exp_score = int(img_comp_utils.get_algo_expected_score(comp_algos.diff_hashing, dt))
    img_file1, img_file2, missing_imgs_  = img_comp_utils.preprocess_images(dt, result_list, special_state)
    idx, base_img_cnt = get_idx_baseimgcnt(realtime, img_file1, img_file2, result_list)
    base_path = os.path.dirname(img_file1)
    runtime_path = os.path.dirname(img_file2)
    base_cnt, runtime_cnt = img_comp_utils.get_img_count(base_path,runtime_path,result_list)
    print("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    print("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    logging.info("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    logging.info("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")###")

    while(idx <= base_img_cnt):
        b_tmp_fname = "B_"+os.path.basename(img_file1)
        r_tmp_fname = "R_"+os.path.basename(img_file2)
        print("d-hash --> current image ::"+img_file1)
        if(b_tmp_fname in missing_imgs_):
            imageops.image_match_outcome_list.append(imageops(b_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "diff_hashing", algo_exp_score, "-999.99", False, "missing baseline"))
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing baseline img:"+b_tmp_fname)
            continue
        elif(r_tmp_fname in missing_imgs_):
            imageops.image_match_outcome_list.append(imageops(r_tmp_fname, os.path.dirname(img_file1), os.path.dirname(img_file2), "diff_hashing", algo_exp_score, "-999.99", False, "missing runtime"))
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,[],realtime)
            missing_imgs_added_to_result = True
            logging.error("missing runtime img:"+r_tmp_fname)
            continue

        diff_file = os.path.join(diff_path,"diff_"+os.path.basename(img_file1))
        if(len(hashsize) > 0):
            baseline_hash = imagehash.dhash(Image.open(img_file1),int(hashsize))
            actual_hash = imagehash.dhash(Image.open(img_file2),int(hashsize))
        else:
            baseline_hash = imagehash.dhash(Image.open(img_file1))
            actual_hash = imagehash.dhash(Image.open(img_file2))
        distance = baseline_hash - actual_hash
       
        if(baseline_hash == actual_hash):
            print("diff-hashing ::",os.path.basename(img_file1),": baseline == runtime. Score =",distance)
        else:
            print("diff-hashing ::",os.path.basename(img_file1),": baseline != runtime. Score =",distance)
        
         #distance = round(score,2)
        print("d-hash match distance (0 = 100% match): {}".format(distance))
        algo_perf_result = img_comp_utils.determine_match_outcome(comp_algos.diff_hashing, distance, "<=", dt)
        result_dict = {os.path.basename(img_file1):{distance:algo_perf_result}}
        print("Match result :",result_dict)
        print("##############################################################")
        if(algo_perf_result==False):
            result_msg = "0"
        else:
            result_msg = "1"
        if(len(hashsize) > 0):
            result_msg = result_msg + " [hs:"+hashsize+"]"
        else:
            result_msg = result_msg + " [hs:def]"
        #if(idx==1):
        imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "diff_hashing", algo_exp_score, str(distance), algo_perf_result, result_msg))
        #elif(idx>1):
        #imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), "", "", "diff_hashing", algo_exp_score, str(distance), algo_perf_result, ""))
        idx = idx + 1
        img_file1, img_file2 = img_comp_utils.getFileName(img_file1, img_file2, idx, result_list, realtime)
        
        
    if(missing_imgs_added_to_result == False and missing_imgs_ is not None):
        for key in missing_imgs_:
            if key not in missing_imgs_.values(): 
                imageops.image_match_outcome_list.append(imageops(key, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), "diff_hashing", algo_exp_score, "-999.99", False, "missing image"))
                logging.error("missing img:"+img_file1)

    if(debugging=="true"):        
        print('')
        print('')
        print('')
        print("******************cumulative match result --> algo :: diff-hashing***********************")
        print('')
        print(imageops.image_match_outcome_list)
        print("****************************************************************************************")
    logging.info("##############################################################")
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished the diff-hashing algo operation in "+ str(elapsed_time) +" minutes...OK")
    logging.info("##############################################################")

    return imageops.image_match_outcome_list, None


## updates on 31-Oct-2020 12:30 AM, 22-Nov-2020 11:45 AM to 11:00 PM, 23-Nov-2020 01:25 AM #
def BRISK_FLANN_match(dt, result_list, special_state):
    start_time = time.time()
    logging.info("##############################################################")
    logging.info("active algo : BRISK-FLANN")
    logging.info("##############################################################")
    BRISK_FLANN_err_ops = []
    missing_imgs_added_to_result = False
    realtime = str(dt["compare_args"]["realtime"]).lower()
    #diff_path = str(dt["compare_args"]["comp_reports_path"])
    debugging = str(dt["compare_args"]["intermediate_output"])
    diff_path = get_diff_path(dt, result_list, "BRISK_FLANN", special_state)
    print('')
    print('')
    print('')
    print("##############################################################")
    print("active algo : BRISK-FLANN")
    print("##############################################################")
    # get expected score for the current algo #
    algo_exp_score = int(img_comp_utils.get_algo_expected_score(comp_algos.brisk_flann,dt))
    img_file1, img_file2, missing_imgs_  = img_comp_utils.preprocess_images(dt, result_list, special_state)
    idx, base_img_cnt = get_idx_baseimgcnt(realtime, img_file1, img_file2, result_list)
    base_path = os.path.dirname(img_file1)
    runtime_path = os.path.dirname(img_file2)
    base_cnt, runtime_cnt = img_comp_utils.get_img_count(base_path,runtime_path,result_list)
    print("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    print("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    logging.info("baseline imgs path: {0} --> img count:{1}".format(base_path, base_cnt))
    logging.info("runtime imgs path: {0} --> img count:{1}".format(runtime_path, runtime_cnt))
    logging.info("##############################################################")
    print("##############################################################")
    
    while(idx <= base_img_cnt):
        b_tmp_fname = "B_"+os.path.basename(img_file1)
        r_tmp_fname = "R_"+os.path.basename(img_file2)
        print("BRISK-FLANN --> current image ::"+img_file1)
        if(b_tmp_fname in missing_imgs_):
            print("Missing baseline image :",b_tmp_fname.split('_')[1])
            imageops.image_match_outcome_list.append(imageops(b_tmp_fname, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"),"BRISK-FLANN", str(base_max_kp)+"-"+str(base_min_kp), "-999.99", False, "missing baseline"))
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx, [], realtime)
            missing_imgs_added_to_result = True
            logging.error("missing baseline img:"+b_tmp_fname)
            continue
        elif(r_tmp_fname in missing_imgs_):
            print("Missing runtime image :",r_tmp_fname.split('_')[1])
            imageops.image_match_outcome_list.append(imageops(r_tmp_fname, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/") ,"BRISK-FLANN", str(base_max_kp)+"-"+str(base_min_kp), "-999.99", False, "missing runtime"))
            idx = idx + 1
            img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx, [], realtime)
            missing_imgs_added_to_result = True
            logging.error("missing runtime img:"+r_tmp_fname)
            continue

        kp_1 = 0
        kp_2 = 0
        diff_file = os.path.join(diff_path,"diff_"+os.path.basename(img_file1))
        print(img_file1)
        img1_arr = cv2.imread(img_file1)
        img2_arr = cv2.imread(img_file2)
        descriptor = cv2.BRISK_create()
        kp_1, desc_1 = descriptor.detectAndCompute(img1_arr, None)
        kp_2, desc_2 = descriptor.detectAndCompute(img2_arr, None)
       
        #kp_1, kp_2, good_points, goodpoints_percent =  FLANNMatch(img1_arr, img2_arr, kp_1, kp_2, desc_1, desc_2, img_file1, dt)
        kp_1, kp_2, good_points, goodpoints_percent =  FLANNMatch(img1_arr, img2_arr, kp_1, kp_2, desc_1, desc_2, diff_file, dt)
       
###################code block for baseline data generation - to be used in benchmark-util.py right after BRISK-FLANN algo is run########################
        cap_kp_variance = kp_1 - kp_2
        if(str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_bl_confirmed_variance_auto_update(disabled)"]).lower() == "true"):
            # for storing into BF baseline json only if the baseline json is not yet generated - 01-Nov-2020 05:30 AM, 02-Nov-2020 11:20 PM #
            # keep the below code block commented until the need arises. Activate it on the need basis - 01-Nov-2020 05:42 AM
            #conf_kp_variance = kp_1 - kp_2 # uncommented on 17-Jul-2021 05:15 PM
            BF_base_data_model.BF_algo_baseline_list.append(BF_base_data_model(os.path.basename(img_file1), str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),str(cap_kp_variance),"est.kp_vari:"+str(cap_kp_variance)))
            #BF_base_data_model.BF_algo_baseline_list.append(BF_base_data_model(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),str(cap_kp_variance),str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),str(conf_kp_variance),"confirmed_kp_variance - auto updated"))
            pass
        else: #uncomment the next line to capture/process additional info, as the need arises. If enabled, needs update in data model too - 13-Nov-2020 11:50 PM
            #BF_base_data_model.BF_algo_baseline_list.append(BF_base_data_model(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/"), str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),str(cap_kp_variance),str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),"","confirmed_kp_variance - manual update needed"))
            BF_base_data_model.BF_algo_baseline_list.append(BF_base_data_model(os.path.basename(img_file1), str(kp_1), str(kp_2), str(good_points), str(goodpoints_percent),"","est.kp_vari:"+str(cap_kp_variance)+".Need conf."))
        dt["compare_args"]["BF_algo_baseline"] = BF_base_data_model.BF_algo_baseline_list
        ###################end of code block for baseline data generation########################################################

        #######################code block for result evaluation and postings##########################################
        dt["compare_args"]["runtime_conf_kp_variance"] = ""
        dt["compare_args"]["conf_kp_variance"] = ""
        dt["compare_args"]["kp_1"] = kp_1
        dt["compare_args"]["kp_2"] = kp_2
        dt["compare_args"]["good_points"] = good_points
        dt["compare_args"]["goodpoints_percent"] = goodpoints_percent
        confirmed_base_range_kp, base_range_gp, base_range_gpp, res1, dt, BF_result_msg = BF_baseline_eval_mgmt_utils.determine_match_within_range(comp_algos.brisk_flann, os.path.basename(img_file1), dt)
        conf_kp_variance = dt["compare_args"]["conf_kp_variance"]
        runtime_conf_kp_variance = dt["compare_args"]["runtime_conf_kp_variance"]
        combined_base_scores = "[kp:confirmed=" + str(confirmed_base_range_kp) + ",current=" + str(kp_1) + "] [gp:" + str(base_range_gp) + "] [gpp:" + str(base_range_gpp) + "] [kp_variance:" + str(conf_kp_variance) + "]"
        combined_act_scores =  "[kp:" + str(kp_2) + "] [gp:" + str(good_points) + "] [gpp:" + str(goodpoints_percent) + "] [kp_variance:" + str(runtime_conf_kp_variance) + "]"
        if(len(imageops.image_match_outcome_list) <= 0):
            imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/") ,"BRISK-FLANN", combined_base_scores, combined_act_scores, res1, BF_result_msg))
        else:
            imageops.image_match_outcome_list.append(imageops(os.path.basename(img_file1), "", "", "BF", combined_base_scores, combined_act_scores, res1, BF_result_msg))
        #######################end of code block for result evaluation and postings##########################################
        idx = idx + 1
        img_file1, img_file2 = img_comp_utils.getFileName(img_file1,img_file2,idx,result_list, realtime)
        
    
    if(missing_imgs_added_to_result == False and missing_imgs_ is not None):
        for key in missing_imgs_:
            if key not in missing_imgs_.values(): 
                imageops.image_match_outcome_list.append(imageops(key, str(os.path.dirname(img_file1)).replace("\\","/"), str(os.path.dirname(img_file2)).replace("\\","/") ,"BRISK-FLANN", "", "-999.99", False, "missing image"))
                logging.error("missing img:"+img_file1)

    if(debugging=="true"):        
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("******************cumulative match result --> algo :: BRISK-FLANN*****************************",dt)
        gen_utils.console_verbose_out('',dt)
        gen_utils.console_verbose_out("Is it correct:?{}".format(imageops.image_match_outcome_list),dt)      
        gen_utils.console_verbose_out("****************************************************************************************",dt)    
    logging.info("##############################################################")
    elapsed_time = round((time.time() - start_time)/60,2)
    logging.info("finished the BRISK-FLANN algo operation in "+ str(elapsed_time) +" minutes...OK")
    logging.info("##############################################################")
    return imageops.image_match_outcome_list, None

# updates on 13-Oct-2020 02:45 AM, 23-Nov-2020 02:05 AM #
def FLANNMatch(img_arr1, img_arr2, kp_1, kp_2, desc_1, desc_2, diff_file, dt):
    #index_params = dict(algorithm=0, trees=5)
    FLANN_accuracy = str(dt["compare_args"]["BRISK_FLANN_parametric"]["FLANNmatcher_accuracy"])
    debugging = str(dt["compare_args"]["intermediate_output"])    #desc_1 = np.float32(desc_1)
    #desc_2 = np.float32(desc_2)
    try:
        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH,
                    table_number = 6, # 12
                    key_size = 12,     # 20
                    multi_probe_level = 1) #2
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        knn_matches = flann.knnMatch(desc_1, desc_2, k=2)
        #if(len(knn_matches) <= 0):
        #   return len(kp_1), len(kp_2), 0, 0
        #matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        #knn_matches = matcher.knnMatch(desc_1, desc_2, 2)
        #print(knn_matches)
        good_points = []
        #for (m,n) in knn_matches:
        #for i,(m,n) in enumerate(knn_matches): #this too is working fine - 29-Sep-2020 12:51 AM
        for i,m_n in enumerate(knn_matches): #this too is working fine - 29-Sep-2020 12:51 AM
            #print("m_n.queryIdx:",m_n.queryIdx)
            #print("m_n.trainIdx:",m_n.trainIdx)
            #time.sleep(3)
            if len(m_n) != 2:
                continue
            (m,n) = m_n
            if m.distance < float(FLANN_accuracy)*n.distance:
                good_points.append(m)


        #src_pts = np.float32([ kp_1[m.queryIdx].pt for m in good_points     ]).reshape(-1,1,2)
        #dst_pts = np.float32([ kp_2[m.trainIdx].pt for m in good_points ]).reshape(-1,1,2)
        #src_pts = np.float32([ kp_1[m.queryIdx].pt for m in enumerate(knn_matches)     ]).reshape(-1,1,2)
        #dst_pts = np.float32([ kp_2[m.trainIdx].pt for m in enumerate(knn_matches) ]).reshape(-1,1,2)
        #M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        #corrected_img = cv2.warpPerspective(img_arr1, m, (img_arr2.shape[1], img_arr2.shape[0]))
        #print("src_pts:",src_pts)
        #print("dst_pts:",dst_pts)
        #print("M:",M)
        #cv2.imshow("warped:",corrected_img)
        #cv2.waitKey(0)
        #print("mask:",mask)
        #time.sleep(6)

        # Define how similar they are
        number_keypoints = 0
        if len(kp_1) <= len(kp_2):
            number_keypoints = len(kp_1)
        else:
            number_keypoints = len(kp_2)

        goodpoints_percent = round((len(good_points) / number_keypoints * 100),2)
        print("keypoints baseline image  : ", str(len(kp_1)))
        print("keypoints runtime image   : ", str(len(kp_2)))
        print("good matches              : ", len(good_points))
        print("how good it's the match ? : ", format(goodpoints_percent))
        print("               *****                  ")
        if(len(good_points) > 0):
            result = cv2.drawMatches(img_arr1, kp_1, img_arr2, kp_2, good_points, None)
            cv2.imwrite(diff_file, result)
        if(debugging=="true" and len(good_points > 0)):
            result = cv2.drawMatches(img_arr1, kp_1, img_arr2, kp_2, good_points, None)
            cv2.imshow("result", cv2.resize(result, None, fx=0.9, fy=0.9))
        return len(kp_1), len(kp_2), len(good_points), goodpoints_percent
    except:
        print("exception :: FLANNMatch --> Result : good points = 0)")
        return len(kp_1), len(kp_2), 0, 0.0
###################End of the function####################################


def doperceptualhashing(imageAStr, imageBStr):
    baselineHash = imagehash.phash(Image.open(imageAStr))
    print('Original Picture: ' + str(baselineHash))

    actualHash = imagehash.phash(Image.open(imageBStr))
    print('Actual Picture: ' + str(actualHash))

    if(baselineHash == actualHash):
        print("Perceptual Hashing :: The pictures are perceptually the same !")
    else:
        distance = baselineHash - actualHash
        print("Perceptual Hashing :: The pictures are different, distance: " + str(distance))
###################End of the function####################################


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
###################End of the function####################################





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
    
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
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

# updates on 08-Oct-2020 12:25 AM #
def get_idx_baseimgcnt(realtime, img_file1, img_file2, result_list):
    base_img_cnt = 1
    idx = 1
    if(len(result_list) > 0):
        base_img_cnt = len(result_list)
        return idx, base_img_cnt
    if(realtime=="true"):
        img1_path = os.path.dirname(img_file1)
        img2_path = os.path.dirname(img_file2)
        base_img_cnt, runtime_img_cnt = img_comp_utils.get_img_count(img1_path,img2_path)
        tmp_ref_file1 = os.path.basename(img_file1).split('_')
        idx = int(tmp_ref_file1[1].split('.')[0])
    return idx, base_img_cnt


#  created on 08-Oct-2020 02:15 AM #
# updates on 25-Oct-2020 08:45 PM, 26-Oct-2020 02:40 AM, 27-Oct-2020 01:50 AM, 22-Nov-2020 04:30 PM, 01-Aug-2021 09:30 PM #
# added on 22-Nov-2020 04:30 PM #
def get_diff_path(dt, result_list, algo_diff_path="ssi", special_state=False):
    diff_path=""
    algo_diff_path = str(algo_diff_path)
    if(not special_state):
        diff_path = str(os.path.join(str(dt["compare_args"]["comp_reports_path"])))
        runtime_path = str(dt["compare_args"]["runtime_img"])
    else:
        diff_path = str(os.path.join(str(dt["compare_args"]["hang_issue_reports_path"])))
        runtime_path = str(dt["compare_args"]["runtime_img_path"])

    
    
     ########### in case the diff path is empty in config file######################
    if(diff_path == ""): 
        if(not special_state):
            diff_path = str(os.path.join(os.path.abspath(os.path.join(runtime_path, os.pardir)),"diff"))
        else:
            diff_path = str(os.path.join(os.path.abspath(os.path.join(runtime_path, os.pardir)),"diff"))
            diff_path = str(os.path.join(diff_path,"hang_issue"))
    ###############################################################################
    diff_path = str(os.path.join(diff_path,algo_diff_path))
    #if(len(result_list) > 0):
        #if(not special_state):
        #    print("get_diff_path:",result_list[0]["runtime_img_path"])
        #    diff_path = os.path.join(result_list[0]["runtime_img_path"])
        #else:
        #    print("get_diff_path:",result_list[0]["img_path"])
        #    diff_path = os.path.join(result_list[0]["img_path"])
        #return diff_path

    
    if(os.path.exists(diff_path) == False):
        os.makedirs(diff_path)
    return diff_path


# Created on 01-Aug-2021 12:50 AM
def build_result_msg(algo_perf_result, result_msg, special_state):
    if(algo_perf_result==False):
        result_msg = result_msg + " - failure"
    else:
        result_msg = result_msg + " - pass"
    return result_msg


def build_result_msg_for_hashings(algo_perf_result, hashsize, special_state):
    result_msg = ""
    print("build_result_msg_for_hashings-special state:",special_state)
    if(algo_perf_result==False):
        result_msg = "0"
    else:
        result_msg = "1"
    if(len(hashsize) > 0):
        result_msg = result_msg + " [hs:"+hashsize+"]"
    else:
        result_msg = result_msg + " [hs:def]"
    
    return result_msg

#Created on 01-Aug-2021 10:55 PM
def get_diff_file(diff_path, img_file1, img_file2, special_state):
    if(not special_state):
        diff_file = str(os.path.join(diff_path,"diff_"+os.path.basename(img_file1)))
    else:
        print("img_file2:",img_file2)
        diff_file = str(os.path.join(diff_path,"diff_"))+str(os.path.basename(img_file1)).split(".")[0]+"_"
        img_file2_arr = str(img_file2).split("_")
        img_file2_idx = len(img_file2_arr)
        print("img_file2_idx:",img_file2_idx)
        diff_file = str(os.path.join(diff_file+img_file2_arr[img_file2_idx-1]))
        print("diff_file",diff_file)
        #time.sleep(7)
    return diff_file













'''
# created on 13-Oct-2020 02:00 AM #
def FLANNMatch_1(img_arr1, img_arr2, kp_1, kp_2, desc_1, desc_2, diff_file, dt):
    #index_params = dict(algorithm=0, trees=5)
    FLANN_accuracy = str(dt["compare_args"]["FLANNmatcher_accuracy"])
    debugging = str(dt["compare_args"]["debugging"])
    #desc_1 = np.float32(desc_1)
    #desc_2 = np.float32(desc_2)
    desc_1 = desc_1.astype(np.float32)
    desc_2 = desc_2.astype(np.float32)
    #desc_1.convertTo(desc_1, CV_32F)
    #desc_2.convertTo(desc_2, CV_32F)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(desc_1,desc_2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    good_points = []
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
            good_points.append(m)

    draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = 0)

    img3 = cv2.drawMatchesKnn(img_arr1,kp_1,img_arr2,kp_2,matches,None,**draw_params)

    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    goodpoints_percent = len(good_points) / number_keypoints * 100
    print("keypoints baseline image : " + str(len(kp_1)))
    print("keypoints runtime image  : " + str(len(kp_2)))
    print("good matches:", len(good_points))
    print("how good it's the match ? : ", goodpoints_percent)

    #plt.imshow(img3,),plt.show())
    cv2.imshow("result", cv2.resize(img3, None, fx=0.9, fy=0.9))
    return len(kp_1), len(kp_2), len(good_points), goodpoints_percent
###################End of the function####################################

# created on 13-Oct-2020 01:45 AM #

def FLANNMatch_prev(img_arr1, img_arr2, kp_1, kp_2, desc_1, desc_2, diff_file, dt):
    #index_params = dict(algorithm=0, trees=5)
    FLANN_accuracy = str(dt["compare_args"]["FLANNmatcher_accuracy"])
    debugging = str(dt["compare_args"]["debugging"])
    #desc_1 = np.float32(desc_1)
    #desc_2 = np.float32(desc_2)
    FLANN_INDEX_LSH = 6
    index_params= dict(algorithm = FLANN_INDEX_LSH,
                    table_number = 6, # 12
                    key_size = 12,     # 20
                    multi_probe_level = 1) #2
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    knn_matches = flann.knnMatch(desc_1, desc_2, k=2)
    #if(len(knn_matches) <= 0):
     #   return len(kp_1), len(kp_2), 0, 0
    #matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    #knn_matches = matcher.knnMatch(desc_1, desc_2, 2)
    #print(knn_matches)
    good_points = []
    #for (m,n) in knn_matches:
    #for i,(m,n) in enumerate(knn_matches): #this too is working fine - 29-Sep-2020 12:51 AM
    for i,m_n in enumerate(knn_matches): #this too is working fine - 29-Sep-2020 12:51 AM
        if len(m_n) != 2:
            continue
        (m,n) = m_n
        if m.distance < float(FLANN_accuracy)*n.distance:
            good_points.append(m)

    # Define how similar they are
    number_keypoints = 0
    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    goodpoints_percent = len(good_points) / number_keypoints * 100
    print("keypoints baseline image : " + str(len(kp_1)))
    print("keypoints runtime image  : " + str(len(kp_2)))
    print("good matches:", len(good_points))
    print("how good it's the match ? : ", goodpoints_percent)
    if(len(good_points) > 0):
        result = cv2.drawMatches(img_arr1, kp_1, img_arr2, kp_2, good_points, None)
        cv2.imwrite(diff_file, result)
    if(debugging=="true" and len(good_points > 0)):
        cv2.imshow("result", cv2.resize(result, None, fx=0.9, fy=0.9))
    return len(kp_1), len(kp_2), len(good_points), goodpoints_percent
###################End of the function####################################

# added below on 22-Nov-2020 04:30 PM
if(len(str(dt["compare_args"]["comp_reports_path"])) == 0):
        import datetime
        diff_path = os.path.dirname(str(dt["compare_args"]["runtime_img"]))
        x = datetime.datetime.now()
        dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
        diff_path = os.path.join(diff_path,"/image_ops/diffs/",dt_part,algo_diff_path)

'''