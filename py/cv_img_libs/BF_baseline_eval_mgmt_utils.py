# created on 23-Nov-2020 01:15 AM #

import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
import argparse
import os.path
import time
import json
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
from cv_img_libs import img_comp_utils
from cv_img_matcher.algos_namelist import comp_algos
from data_models.imageops_data_model import CustomEncoder
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
import logging


# Updates on : 30-Sep-2020 02:35 AM, 02-Oct-2020 06:15 PM, 02-Nov-2020 03:00 AM, 04:00 AM, 08:00 AM, 01:25 PM, 03-Nov-2020 04:00 AM, 04-Nov-2020 03:10 AM, 10:15 PM, 07-Nov-2020 02:15 AM, 04:25 PM, 11:50 PM, 08-Nov-2020 03:10 AM, 09-Nov-2020 04:00 AM, 14-Nov-2020 02:50 PM #
def determine_match_within_range(comp_algo, imgfile, dt):
    #algo_exp_score = get_algo_expected_score(comp_algo,dt)
    comp_result = False
    BF_algo_net_result = False
    base2base_kp = ""
    baseline_kp = dt["compare_args"]["kp_1"]
    kp = dt["compare_args"]["kp_2"]
    gp = dt["compare_args"]["good_points"]
    gpp = dt["compare_args"]["goodpoints_percent"]
    
    # read from BF baseline json, if present. If not, read from the data object being populated at the time of algo operation
    BF_algo_read_result, BF_base, _is_origin_data_object = read_BF_algo_baseline(dt)
    
    # if the BF-base is False, there's no baseline json available for BF algo
    if not BF_algo_read_result:
        print("Img file:{0} not found in the baseline json or error reading it".format(imgfile))
        return "", "", "", False, dt, "unable to read BRISK-FLANN baseline data or empty records"
    
    # loop through for the supplied image file. Retrieve the corresponding json node details, if the image file is present 
    imgfound, tmp_BF_base, erratic_img, dt = find_image_in_BF_baseline_recs(imgfile, BF_base, dt, False)
     
    # when the specified image is not found in the json file and the previous search scope of the image not happened in the data object, this must be a new image and should be added to the new image buffer in BF_baseline_data_model
    if not imgfound and not _is_origin_data_object:
        n = 0
        BF_resJson = json.dumps([o.dump() for o in dt["compare_args"]["BF_algo_baseline"]])
        BF_base = json.loads(BF_resJson)
        imgfound, tmp_BF_base, erratic_img, dt = find_image_in_BF_baseline_recs(imgfile, BF_base, dt, True)


    # get either the min-max range or the absolute value for the specified image - for the baseline
    base_min_kp, base_max_kp, kp_min_max_truthy, base_range_kp = get_minmax_BF_algo(imgfile, tmp_BF_base["confirmed_baseline_kp"], False)
    base_min_gp, base_max_gp, gp_min_max_truthy, base_range_gp = get_minmax_BF_algo(imgfile, tmp_BF_base["confirmed_good_points"], False)
    base_min_gpp, base_max_gpp, gpp_min_max_truthy, base_range_gpp = get_minmax_BF_algo(imgfile, tmp_BF_base["confirmed_good_points_percent"], True )

    if not imgfound:
        print("Img file {0} not found in the BF baseline".format(imgfile))
        #return base_min_kp, base_max_kp, base_min_gp, base_max_gp, base_min_gpp, base_max_gpp, False, "Img file not found in the BF baseline"
        return base_range_kp, base_range_gp, base_range_gpp, False, dt, "Img file not found in the BF baseline" 
    
    if erratic_img:
        print("Img file {0}. Zero keypoint error".format(imgfile))
        print("captured baseline kp --->",BF_base[0]["confirmed_baseline_kp"])
        return base_range_kp, base_range_gp, base_range_gpp, False, dt, "Zero keypoint error"
    
    # if the confirmed keypoints variance is empty, the baseline values remain unverified and effectively this means there's no authentic baseline
    conf_kp_variance = str(tmp_BF_base["confirmed_kp_variance"])
    if(conf_kp_variance == ""):
        print("FAILURE :: Img file :{0} --> confirmed keypoints variance empty. Baseline min-max and the runtime score :[{1}],[{2}]".format(imgfile,base_range_kp,kp))
        return base_range_kp, base_range_gp, base_range_gpp, False, dt, "kp variance empty"

    # perform a set of comparisons of the baseline with the actual score in the corresponding category
    kp_algo_perf_result_, runtime_conf_kp_variance, msg = evaluate_BF_runtime_score(imgfile, baseline_kp, kp, base_max_kp, kp_min_max_truthy, "kp", "", base_range_kp, base_min_kp, conf_kp_variance, True)
    dt["compare_args"]["conf_kp_variance"] = conf_kp_variance
    dt["compare_args"]["runtime_conf_kp_variance"] = runtime_conf_kp_variance
    gp_algo_perf_result_, runtime_conf_kp_variance, msg = evaluate_BF_runtime_score(imgfile, baseline_kp, gp, base_max_gp, gp_min_max_truthy, "gp", msg, base_range_gp, base_min_gp, conf_kp_variance, False)
    gpp_algo_perf_result_, runtime_conf_kp_variance, msg = evaluate_BF_runtime_score(imgfile, baseline_kp, gpp, base_max_gpp, gpp_min_max_truthy, "gpp", msg, base_range_gpp, base_min_gpp, conf_kp_variance, False)
    if str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"]).lower() == "true":
        BF_algo_net_result = bool(kp_algo_perf_result_ and gp_algo_perf_result_ and gpp_algo_perf_result_)
    elif str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"]).lower() == "false":
        msg = msg + "," + "[gp-gpp check disabled]"
        BF_algo_net_result = bool(kp_algo_perf_result_)
    
    if BF_algo_net_result == False:
        prev_base_range_kp = base_range_kp
        comp_result, base2base_kp =  compare_current_prev_baseline_and_update(imgfile, prev_base_range_kp, baseline_kp, dt)
        if(comp_result == True):
            BF_basetobase_comp_data_model.basetobase_kp_update_list.append(BF_basetobase_comp_data_model(imgfile, comp_result, base2base_kp))    
    return base_range_kp, base_range_gp, base_range_gpp, BF_algo_net_result, dt, msg

# created on 02-Nov-2020 02:20 AM, 13-Nov-2020 02:10 AM #
def get_minmax_BF_algo(imgfile, BF_base_rec, do_roundoff):
    base_score = str(BF_base_rec)
    base_score_min = ""
    base_score_max = ""
    base_score_range = ""
    min_max_truthy = False
    if("-" in base_score):
        base_score_min = str(BF_base_rec).split("-")[0]
        base_score_max = str(BF_base_rec).split("-")[1]
        if(do_roundoff == True):
            base_score_min, base_score_max = roundoff_decimal(base_score_max, base_score_min)
        base_score_range = base_score_min+"-"+base_score_max
        min_max_truthy = True
        logging.info("Img file : {0}. BRISK-FLANN baseline range {1}-{2}:".format(imgfile, base_score_min, base_score_max))
    else:
        base_score_min = ""
        base_score_max = str(BF_base_rec)
        if(do_roundoff == True):
            _, base_score_max = roundoff_decimal(base_score_max, "")
        base_score_range = base_score_max
        min_max_truthy = False
        logging.info("Img file : {0}. BRISK-FLANN baseline value:{1}".format(imgfile, base_score_max))
    print("min-max info:",base_score_min, base_score_max, min_max_truthy, base_score_range)
    return base_score_min, base_score_max, min_max_truthy, base_score_range


# created on 06-Nov-2020 12:40 AM to 03:25 AM #
def compare_current_prev_baseline_and_update(imgfile, prev_base_kp, current_kp, dt):
    base_score = str(prev_base_kp)
    base_score_min = ""
    base_score_max = ""
    base_score_range = ""
    _is_update_done = False
    
    if(str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_baseline_metrics_auto_update(disabled)"]).lower() == "false"):
        return False, prev_base_kp
    if str(prev_base_kp) == "0" or str(prev_base_kp) == "" :
        return False, prev_base_kp

    if("-" in base_score):
        base_score_min = str(prev_base_kp).split("-")[0]
        base_score_max = str(prev_base_kp).split("-")[1]
        
        if(current_kp >= base_score_min and current_kp <= base_score_max):
            base_score_range = prev_base_kp
            return False, base_score_range
        base_score_range = current_kp
        logging.info("{0} --> prev baseline kp : {1} updated with {2}".format(imgfile, prev_base_kp, current_kp))
        _is_update_done = True
        return _is_update_done, base_score_range
    else:
        base_score_min = ""
        base_score_max = str(prev_base_kp)
        if(base_score_max == current_kp):
            base_score_range = prev_base_kp
            return False, base_score_range
        if(base_score_max != current_kp):
            _is_update_done = True
            base_score_range = current_kp
            logging.info("{0} --> prev baseline kp : {1} updated with {2}".format(imgfile, prev_base_kp, current_kp))
    return _is_update_done, base_score_range


# created on 04-Nov-2020 09:00 PM #
# updates on 05-Nov-2020 02:30 AM, 14-Nov-2020 02:50 PM #
def find_image_in_BF_baseline_recs(imgfile, BF_base, dt, _shouldbuffer_newimgs):
    n=0
    tmp_BF_base = None
    imgfound = False
    erratic_img = False
    while(n < len(BF_base)):
        if(BF_base[n]["image"] == imgfile):
            imgfound = True
            tmp_BF_base = BF_base[n]

            # if the specified image has been newly added, this needs to be added to baseline json. Hence, it's buffered here for later use
            if _shouldbuffer_newimgs == True:
                dt = buffer_newimgs(imgfile, dt)

            if(BF_base[n]["confirmed_baseline_kp"] == "0" or BF_base[n]["confirmed_runtime_kp"] == "0"):
                erratic_img = True
            break
        n = n + 1
    return imgfound, tmp_BF_base, erratic_img, dt


# created on 04-Nov-2020 11:10 PM #
# updates on 05-Nov-2020 02:30 AM #
def buffer_newimgs(imgfile, dt):
    baseline_kp = dt["compare_args"]["kp_1"]
    kp = dt["compare_args"]["kp_2"]
    gp = dt["compare_args"]["good_points"]
    gpp = dt["compare_args"]["goodpoints_percent"]
    cap_kp_variance = baseline_kp - kp
    # uncomment the below line, when the need arises related to captured and baseline and runtime paths - 14-Nov-2020 2:25 AM
    #BF_base_data_model.newimgs_baseline_buffer.append(BF_base_data_model(os.path.basename(imgfile), "", "", str(baseline_kp), str(kp), str(gp), str(gpp),str(cap_kp_variance),str(baseline_kp), str(kp), str(gp), str(gpp),"","new img -> confirmed_kp_variance - manual update needed"))
    BF_base_data_model.newimgs_baseline_buffer.append(BF_base_data_model(os.path.basename(imgfile), str(baseline_kp), str(kp), str(gp), str(gpp),"","new img:est.kp_vari:"+str(cap_kp_variance)+".Need conf."))
    print(imgfile + "-> new image buffered for BF algo baselining")
    logging.info(imgfile + "-> new image buffered for BF algo baselining")
    dt["compare_args"]["newimgs_baselinebuffer"] = BF_base_data_model.newimgs_baseline_buffer
    return dt

# created on 03-Nov-2020 02:10 AM #
def roundoff_decimal(score_max, score_min=""):
    min_gpp=""
    max_gpp=""
    if score_min != "":
        min_gpp = float(score_min)
        min_gpp = round(min_gpp,2)
    max_gpp = float(score_max)
    max_gpp = round(max_gpp,2)
    return str(min_gpp), str(max_gpp)

# created on 02-Nov-2020 02:20 AM #
# updates on 02-Nov-2020 04:00 AM, 05-Nov-2020 01:20 AM, 07-Nov-2020 02:05 AM, 03:15 PM, 11:50 PM, 08-Nov-2020 03:10 AM, 03:10 PM #
def evaluate_BF_runtime_score(imgfile, baseline_kp, score, max, min_max_truthy, eval_type, eval_result_msg, base_score_range, min="0", conf_kp_variance="-zzz", _is_kp_comparison=True):
    algo_perf_result_ = False
    runtime_conf_kp_variance = ""
    msg = eval_result_msg

    if(conf_kp_variance != "-zzz" and _is_kp_comparison == True):
        runtime_conf_kp_variance = int(baseline_kp) - int(score)
        runtime_conf_kp_variance = str(runtime_conf_kp_variance)
        print("baseline confirmed_kp_variance:",conf_kp_variance,"runtime confirmed_kp_variance:",runtime_conf_kp_variance)
        if(runtime_conf_kp_variance != conf_kp_variance):
            print("{0} --> kp_variance match : FAIL. ".format(imgfile))
            print("baseline conf_kp_variance <> runtime conf_kp_variance : {0} <> {1}".format(conf_kp_variance, runtime_conf_kp_variance))
            msg = "[kp:FAILED-->"
            msg = msg + "{0}<>{1}]".format(conf_kp_variance, runtime_conf_kp_variance)
            return False, runtime_conf_kp_variance, msg
        elif runtime_conf_kp_variance == conf_kp_variance:
            print("{0} --> kp_variance match : PASS. ".format(imgfile))
            print("Baseline kp - runtime kp - kp_variance :[{0}] - [{1}] = [{2}]".format(baseline_kp, score, conf_kp_variance))
            msg = "[kp:PASSED],"
            return True, runtime_conf_kp_variance, msg
        

    if min_max_truthy == True:
        if(eval_type == "gp"):
            score = int(score)
            min = int(min)
            max = int(max)
        elif(eval_type == "gpp"):
            score = float(score)
            min = float(min)
            max = float(max)

        if(score >= min and score <= max):
            algo_perf_result_ = True
            print("{0} --> BRISK-FLANN algo match : PASS".format(imgfile))
            print("min, max and actual score :{0}, {1}, {2}".format(min, max, score))
            if(eval_type == "gp"):
                msg = msg + "[gp:PASSED],"
            elif(eval_type == "gpp"):
                msg = msg + "[gpp:PASSED]"
        else:
            print("{0} --> BRISK-FLANN algo match : FAIL".format(imgfile))
            print("min, max and actual score :{0}, {1}, {2}".format(min, max, score))
            if(eval_type == "gp"):
                msg = msg + "[gp:FAILED-->"
                msg = msg + "{0}<>{1}],".format(base_score_range, score)
            elif(eval_type == "gpp"):
                msg = msg + "[gpp:FAILED-->"
                msg = msg + "{0}<>{1}]".format(base_score_range, score)
            
    if min_max_truthy == False:
        if(str(score) == str(max)):
            algo_perf_result_ = True
            print("Img file : {0} --> BRISK-FLANN algo match : PASS".format(imgfile))
            print("baseline and actual score :{0}={1}".format(max, score))
            if(eval_type == "gp"):
                msg = msg + "[gp:PASSED],"
            elif(eval_type == "gpp"):
                msg = msg + "[gpp:PASSED]"
        else:
            print("Img file : {0} --> BRISK-FLANN algo match : FAIL".format(imgfile))
            print("baseline and actual score :{0}<>{1}".format(max, score))
            if(eval_type == "gp"):
                msg = msg + "[gp:FAILED-->"
                msg = msg + "{0}<>{1}],".format(base_score_range, score)
            elif(eval_type == "gpp"):
                msg = msg + "[gpp:FAILED-->"
                msg = msg + "{0}<>{1}]".format(base_score_range, score)

    return algo_perf_result_, runtime_conf_kp_variance, msg



def read_BF_algo_result(file):
    #f = open(file, "a")
    f = open(file, "r")
    return f.read()
    #print("BF_algo_baseline_read:",f.read())

# created on 01-Nov-2020 10:20 PM #
# updates on 02-Nov-2020 11:45 PM, 04-Nov-2020 02:45 AM, 05:50 PM, 08:50 PM, 11:30 PM, 05-Nov-2020 02:15 AM, 11-Nov-2020 12:30 AM #
def read_BF_algo_baseline(dt):
    tmp_obj = None
    _is_origin_data_object  = False
    base_file = dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"]
     # if the data object is empty and the baseline json is not present, then return false with empty object
    if len(str(dt["compare_args"]["BF_algo_baseline"])) <= 0 and not os.path.exists(base_file) :
        return False, tmp_obj, _is_origin_data_object
    
    if(os.path.exists(base_file)):
        BF_algo_base = img_comp_utils.readJson_plain(base_file)
        BF_algo_base = json.dumps(BF_algo_base)
        BF_algo_base = str(BF_algo_base)
        BF_res_obj_json = json.loads(BF_algo_base)
        return True, BF_res_obj_json, _is_origin_data_object
    
    # if the baseline json is not present, then read the contents from the data object
    BF_resJson = json.dumps([o.dump() for o in dt["compare_args"]["BF_algo_baseline"]])
    BF_res_obj_json = json.loads(BF_resJson)
    _is_origin_data_object = True
 
    return True, BF_res_obj_json, _is_origin_data_object
