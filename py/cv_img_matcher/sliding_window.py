# ##########################################################
# Author : Yusuf
# Created on 08-Aug-2021 10:00 AM 
# Updates on : 08-Aug-2021 11:55 PM, 09-Aug-2021 02:30 AM, 14-Aug-2021 10:30 AM to 11:55 PM. 15-Aug-2021 01:30 AM, 08:30 AM to 11:55 PM, 16-Aug-2021 02:55 AM, 17-Aug-2021 02:00 AM, 17-Aug-2021 11:55 PM, 18-Aug-2021 12:30 AM, 18-Aug-2021 11:55 PM, 19-Aug-2021 03:10 AM, 20-Aug-2021 02:30 AM, 01:00 PM to 21-Aug-2021 03:00 AM, 10:30 AM to 22-Aug-2021 02:30 AM, 23-Aug-2021 06:30 AM, 10:30 AM, 11:00 PM, 29-Aug-2021 03:00 AM, 30-Aug-2020 02:10 AM, 31-Aug-2021 02:20 AM, 31-Aug-2021 10:45 PM,01-Sep-2021 03:50 AM to 04:45 AM, 07:15 AM, 11:00 PM, 02-Sep-2021 06:15 AM to 09:30 AM, 11:30 PM
# ##########################################################
#from cv_img_libs.logical_gate_evaluator import compare_results

import logging
#from py_v3.cv_img_libs.img_comp_utils import runtime_imgs_apply_mask
import sys
import os

from numpy.lib.shape_base import _dstack_dispatcher
#from typing_extensions import runtime
sys.path.insert(0, os.path.realpath(os.path.pardir))
from PIL import Image
import numpy as np
import imutils
#from helpers import sliding_window
import argparse
import time
#from helpers import pyramid
from skimage.transform import pyramid_gaussian
from numpy import asarray
import cv2
import logging
import sys
import os
from shutil import copyfile

import datetime
import re
import json
import argparse
import time
#from numpy.lib.function_base import select
from cv_img_libs import gen_utils
from cv_img_libs import config_utils_lib
from cv_img_libs import BRISK_FLANN_baseline_utils_lib
from cv_img_libs import algo_artifacts_handler
from cv_img_libs import img_comp_utils
from cv_img_libs import special_config_keys
from data_models.sliced_image_checker_negative_cond import sliced_image_checker_negative_cond
from data_models.sliding_window_negative_cond_summary import sliding_window_negative_cond_summary
from data_models.sliced_image_checker_positive_cond import sliced_image_checker_positive_cond
from data_models.sliding_window_positive_cond_summary import sliding_window_positive_cond_summary
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.net_analysis_report_data_model import net_analysis_report




def pyramid1(image, scale=3.5, minSize=(70, 70)):
	# yield the original image
	#yield image
	# keep looping over the pyramid
	while True:
		# compute the new dimensions of the image and resize it
		w = int(image.shape[1] / scale)
		image = imutils.resize(image, width=w)
		# if the resized image does not meet the supplied minimum
		# size, then stop constructing the pyramid
		if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
			break
		# yield the next image in the pyramid
		yield image

def pyramid(image, scale=3.5, minSize=(70, 70)):
    # compute the new dimensions of the image and resize it
    w = int(image.shape[1] / scale)
    image = imutils.resize(image, width=w)
	# if the resized image does not meet the supplied minimum
	# size, then stop constructing the pyramid
	#if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]:
    #break
	# yield the next image in the pyramid
    yield image





def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])
			#if(jump_next_y):
			#    print("jump_next:",x," ",y)
			#    time.sleep(8)
			#    break
		#print("After jumping-y:",y)
		#time.sleep(5)
               




def pyramid_gaussian(image, downscale=2):
    # METHOD #2: Resizing + Gaussian smoothing.
    for (i, resized) in enumerate(pyramid_gaussian(image, downscale)):
	    # if the image is too small, break from the loop
	    if resized.shape[0] < 30 or resized.shape[1] < 30:
		    break
		
	    # show the resized image
	    cv2.imshow("Layer {}".format(i + 1), resized)
	    cv2.waitKey(0)


#Created on 07-Aug-2021 05:45 PM
def retriveConfigs(args):
    dt = img_comp_utils.readJson(args["json"], "compare_args")
    reports_path = str(dt["compare_args"]["comp_reports_path"])
    
    net_result_path = str(dt["compare_args"]["net_result_path"])
    should_purge_oldlog = str(dt["compare_args"]["purge_old_artifacts"])
    if(not reports_path.endswith("/")):
        reports_path = reports_path + "/"
    if(not net_result_path.endswith("/")):
        net_result_path = net_result_path + "/"
    return dt, reports_path,net_result_path,should_purge_oldlog


def create_special_keys(dt):
    dt["compare_args"]["sliding_window_active"] = "true"
    dt["compare_args"]["hang_issue_reports_path"] = ""
    dt["compare_args"]["hang_issue_checker"] = {}
    dt["compare_args"]["hang_issue_checker"]["check_frequency_min"] = ""
    dt["compare_args"]["copied_baseline_to_temp_location"] = "false"
    dt["compare_args"]["done_aspect_ratio_baseline"] = "false"
    dt["compare_args"]["downscaled_baseline"] = "false"
    return dt


def get_runtime_paths(dt):
    runtime_img_path = str(dt["compare_args"]["runtime_imgs_path"])
    temp_runtime_path = os.path.join(str(dt["compare_args"]["runtime_imgs_path"]),"slices")
    return runtime_img_path, temp_runtime_path


def format_paths(dt):
    if not str(dt["compare_args"]["img_ops_session_rootpath"]).endswith("/"):
        dt["compare_args"]["img_ops_session_rootpath"] = dt["compare_args"]["img_ops_session_rootpath"] + "/"
    if not str(dt["compare_args"]["comp_reports_path"]).endswith("/"):
        dt["compare_args"]["comp_reports_path"] = dt["compare_args"]["comp_reports_path"] + "/"
    if not str(dt["compare_args"]["net_result_path"]).endswith("/"):
        dt["compare_args"]["net_result_path"] = dt["compare_args"]["net_result_path"] + "/"
    if not str(dt["compare_args"]["runtime_imgs_path"]).endswith("/"):
        dt["compare_args"]["runtime_imgs_path"] = dt["compare_args"]["runtime_imgs_path"] + "/"
    
    runtime_img_path, sliced_imgs_runtime_path = get_runtime_paths(dt)
    if not str(runtime_img_path).endswith("/"):
        runtime_img_path = runtime_img_path + "/"
    
    if not str(sliced_imgs_runtime_path).endswith("/"):
        sliced_imgs_runtime_path = sliced_imgs_runtime_path + "/"
    return dt, runtime_img_path, sliced_imgs_runtime_path


def get_files(path):
    img_list = []
    if not os.path.exists(path):
        return img_list
    for dirname, dirnames, filenames in os.walk(path):
        print("dirname:",dirname)
        #time.sleep(1)
        for filename in filenames:
            img_list.append(os.path.join(dirname, filename))
    img_list = gen_utils.sort(img_list)
    return img_list



def set_run_mode_to_historical(dt):
    if str(dt["compare_args"]["realtime"]).lower() == "true":
        dt["compare_args"]["realtime"] = "false"
    return dt



def call_func(dt, algo_idx, tmp_match_data, special_state=False):
    tmp_res = []
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_mapper = config_utils_lib.get_algo_mapper()
    print("algo active index | algo :",algo_idx, "|", algo_name_list[algo_idx])

    if(len(tmp_match_data) > 0):
        pass
    func, _ = algo_mapper[algo_name_list[algo_idx]](dt,tmp_match_data,special_state)
    if(callable(func)):
        #tmp_res = func()
        return algo_name_list, func
    else:
        return algo_name_list, func


def compare(orig_runimage, sliced_run_img, row_no, dt, positive_cond):
    result = False
    res_obj_json = []
    res_obj_json_persist = []

    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_cnt  = 2
    algo_idx = 0
    res_obj_json = []
    while(algo_idx < algo_cnt):
        if(algo_name_list[algo_idx] != "SSI" and algo_name_list[algo_idx] != "perceptual_hashing"): # uncomment the preceding commented statement to activate p-hash
            algo_idx = algo_idx + 1
            continue
        if(not positive_cond):
            res_obj_json, res_obj_json_persist, result, dt = compare_negative_images(sliced_run_img, algo_idx, row_no, dt)
        else:
            res_obj_json, res_obj_json_persist, result, dt = check_positive_condition(orig_runimage, algo_idx, row_no, dt)
            #res_obj_json, res_obj_json_persist, result, dt = check_positive_condition(algo_idx, row_no, dt)
        print("check the copied flag:",dt["compare_args"]["copied_baseline_to_temp_location"])
        algo_idx = algo_idx + 1
    return res_obj_json_persist, result, dt



def generate_report(res_obj_json_persist, original_report_path, report_file):
    res_obj_json_persist = gen_utils.convert_serializable(res_obj_json_persist)
    data_gap_detection_report = os.path.join(original_report_path, report_file)
    img_comp_utils.writeJson(data_gap_detection_report,res_obj_json_persist,True)
    return res_obj_json_persist



def compare_negative_images(orig_runimage, algo_idx, row_no, dt):
    i = 0
    result = True
    tmp_match_data = []
    res_obj_json = []
    special_state = False
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    sliced_image_checker_negative_cond.tmp_img_match_result_list = []
    all_baseline_imgs_list = get_files(str(os.path.dirname(dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"])))
    all_baseline_imgs_list = gen_utils.sort(all_baseline_imgs_list)
    debugging = str(dt["compare_args"]["intermediate_output"])
    #print(all_baseline_imgs_list)
    #time.sleep(1)
    failures_per_row = int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"])
    if(failures_per_row > 0):
        print("COMPARE_IMAGE:failures_per_row - INITIAL:",failures_per_row)
        #time.sleep(2)
    instance_cnt = 0
    #print("FAILURED_PER_ROW_ASSIGNMENT:",failures_per_row)
    #time.sleep(1)

    #print("res_obj_json-outside:",res_obj_json)
    #time.sleep(2)
    baseline_list_len = len(all_baseline_imgs_list)
    idx = 0
    for base_img_file in all_baseline_imgs_list:
        idx += 1
        dt["compare_args"]["baselineImage"] = os.path.join(os.path.dirname(dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"]), base_img_file)
        algo_name_list, tmp_match_data = call_func(dt,algo_idx,res_obj_json, special_state)
        resJson = json.dumps([o.dump() for o in tmp_match_data])
        res_obj_json = json.loads(resJson) 

        if(bool(res_obj_json[0]["result"]) == False):
            result = True
        elif(bool(res_obj_json[0]["result"]) == True):
            result = False

        base_img = str(os.path.basename(dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"]))
        sliced_runtime_img = str(os.path.basename(dt["compare_args"]["runtime_img"]))
        img_path = str(os.path.dirname(dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"])) + " && " + str(os.path.dirname(dt["compare_args"]["runtime_img"]))
        
        if(not result):
            if(len(sliced_image_checker_negative_cond.sliced_image_checker_result_list) <= 0):
                sliced_image_checker_negative_cond.tmp_img_match_result_list.append(sliced_image_checker_negative_cond(base_img_file, sliced_runtime_img, img_path, res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
                sliced_image_checker_negative_cond.sliced_image_checker_result_list.append(sliced_image_checker_negative_cond(base_img_file, sliced_runtime_img, img_path, res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
            else:
                sliced_image_checker_negative_cond.tmp_img_match_result_list.append(sliced_image_checker_negative_cond(base_img_file, sliced_runtime_img, "", res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
                sliced_image_checker_negative_cond.sliced_image_checker_result_list.append(sliced_image_checker_negative_cond(base_img_file, sliced_runtime_img, "", res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
            copyfile(str(dt["compare_args"]["runtime_img"]), str(os.path.join(dt["compare_args"]["failed_slices_path"],sliced_runtime_img)))
            copyfile(orig_runimage, str(os.path.join(dt["compare_args"]["failed_slices_path"],str(os.path.basename(orig_runimage)))))
            
            for rec in sliced_image_checker_negative_cond.sliced_image_checker_result_list:
                #print("FALSE RSULT::check run::",rec)
                if(str(rec).__contains__(str(os.path.basename(dt["compare_args"]["runtime_img"])))):
                    instance_cnt += 1


            if(instance_cnt == 1):
                failures_per_row += 1
                dt["compare_args"]["consecutive_failures_per_row_curr_cnt"] = str(failures_per_row)
                print("FALSE RESULT::RUN TIME IMAGE PREVIOUSLY NOT IN THE sliced_image_checker-list_INCREMENTED:",failures_per_row)
            else:
                print("FALSE RESULT::already INCREMENTED - sliced_runtime_img:",str(os.path.basename(dt["compare_args"]["runtime_img"]))," ",failures_per_row)

            instance_cnt = 0
            print("CHECK - FALSE........................................")
            print("dt[compare_args][consecutive_failures_per_row_curr_cnt]",dt["compare_args"]["consecutive_failures_per_row_curr_cnt"])
            print("!CHECK!---FALSE........................................")
            #print("base_img_file:",base_img_file)
            #time.sleep(1)
            break
        else:
            #print("CHECK - TRUE........................................")
            #print("dt[compare_args][consecutive_failures_per_row_curr_cnt]",dt["compare_args"]["consecutive_failures_per_row_curr_cnt"])
            #print("!CHECK!---TRUE........................................")
            #time.sleep(5)
            print('dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"] - bef bef:',dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"])
            print('dt["compare_args"]["runtime_img"] - bef bef:',dt["compare_args"]["runtime_img"])
            #time.sleep(5)

            #pos_result = check_positive_condition(dt)
            print('dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"] - back back:',dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"])
            print('dt["compare_args"]["runtime_img"] - back back:',dt["compare_args"]["runtime_img"])
            #time.sleep(5)


            rec_found = False
            for rec in sliced_image_checker_negative_cond.sliced_image_checker_result_list:
                #print(rec)
                if(str(rec).__contains__(str(os.path.basename(dt["compare_args"]["runtime_img"])))):
                    rec_found = True
                    print("RUN TIME IMAGE EXISTS/LOCATED - not to be reset:",str(os.path.basename(dt["compare_args"]["runtime_img"]))," ", failures_per_row)
                    break

            if(str(sliced_runtime_img).__contains__("slice_87.png") or str(sliced_runtime_img).__contains__("slice_93.png") or str(sliced_runtime_img).__contains__("slice_99.png")):
                print("YESSSS:",rec)
                #time.sleep(8)6

            if(not rec_found):
                print("rec IS NOT PRESENT")
                    #print("rec:",rec)
                print("str(os.path.basename(dt[compare_args][runtime_img]))):",str(os.path.basename(dt["compare_args"]["runtime_img"])))
                    
            #if(str(os.path.basename(dt["compare_args"]["runtime_img"])) not in sliced_image_checker_negative_cond.sliced_image_checker_result_list):
                if( idx == len(all_baseline_imgs_list)-1 ):
                    print("about to reset to zero:",dt["compare_args"]["runtime_img"]," ", failures_per_row)

                    if(int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"]) == 0):
                        failures_per_row = 0
                        dt["compare_args"]["consecutive_failures_per_row_curr_cnt"] = str(failures_per_row)
                        print("reset to zero done:",dt["compare_args"]["runtime_img"])
                    #time.sleep(1)

            res_obj_json = [] 
            tmp_match_data = []
            imageops.image_match_outcome_list = []
            if(sliced_runtime_img.__contains__("slice_87.png") or sliced_runtime_img.__contains__("slice_93.png") or sliced_runtime_img.__contains__("slice_99.png")):
                #time.sleep(5)
                pass

        ## the below stmts are important to successfully return to the caller after being done with just one image  21-Aug-2021 09:30 PM
    res_obj_json = [] 
    tmp_match_data = []
    imageops.image_match_outcome_list = []
    dt["compare_args"]["copied_baseline_to_temp_location"] = "true"
    #if(sliced_runtime_img.__contains__("slice_87.png") or sliced_runtime_img.__contains__("slice_93.png") or sliced_runtime_img.__contains__("slice_99.png")):
    #    print("compare_images-just before exit:",int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]))

    return sliced_image_checker_negative_cond.tmp_img_match_result_list, sliced_image_checker_negative_cond.sliced_image_checker_result_list, result, dt


# Created on 30-Aug-2021 01:30 AM
# Updates on 01-Sep-2021 04:45 AM
def check_positive_condition(orig_runimg, algo_idx, row_no, dt):
    result = False
    res_obj_json = []
    res_obj_json_persist = []
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_cnt  = 2
    res_obj_json = []
    positive_img_path = str(dt["compare_args"]["sliding_window"]["positive_conditions"]["positive_baseline_path"])
    pos_baseline_imgs_list = get_files(str(os.path.dirname(positive_img_path)))
    pos_baseline_imgs_list = gen_utils.sort(pos_baseline_imgs_list)
    idx = 0
    prev_m1_score = dt["compare_args"]["similarity"][0]["m1_score"]
    prev_m2_score = dt["compare_args"]["similarity"][1]["m2_score"]
    for base_img_file in pos_baseline_imgs_list:
        idx += 1
        dt["compare_args"]["baselineImage"] = os.path.join(positive_img_path, base_img_file)

            # temporarily update the original baseline score with the scores meant for positive conditions. This is to save additional coding effort and the associated complexities
        if(dt["compare_args"]["similarity"][0]["method1"] == "SSI"):
            dt["compare_args"]["similarity"][0]["m1_score"] = "1.0"
            dt["compare_args"]["similarity"][1]["m2_score"] = "0"
        else:
            dt["compare_args"]["similarity"][0]["m1_score"] = "0"
            dt["compare_args"]["similarity"][1]["m2_score"] = "1.0"
            
        print(prev_m1_score)
        print(prev_m2_score)
        print(dt["compare_args"]["similarity"][0]["m1_score"])
        print(dt["compare_args"]["similarity"][1]["m2_score"])
        #time.sleep(5)

            # call the algoritm delegate function
        algo_name_list, tmp_match_data = call_func(dt,algo_idx,res_obj_json, False)
        resJson = json.dumps([o.dump() for o in tmp_match_data])
        res_obj_json = json.loads(resJson) 

        if(bool(res_obj_json[0]["result"]) == False):
            result = False
        elif(bool(res_obj_json[0]["result"]) == True):
            result = True
            
            # assign back the original values to the baseline score fields
        dt["compare_args"]["similarity"][0]["m1_score"] = prev_m1_score
        dt["compare_args"]["similarity"][1]["m2_score"] = prev_m2_score

        #base_img = str(os.path.basename(dt["compare_args"]["sliding_window"]["positive_conditions"]["positive_baseline_path"]))
        sliced_runtime_img = str(os.path.basename(dt["compare_args"]["runtime_img"]))
        img_path = str(os.path.dirname(dt["compare_args"]["sliding_window"]["positive_conditions"]["positive_baseline_path"])) + " && " + str(os.path.dirname(dt["compare_args"]["runtime_img"]))
        
        # if the result is PASS, store the detailed result info to the respective data model
        if(result):
            if(len(sliced_image_checker_positive_cond.sliced_image_checker_result_list) <= 0):
                sliced_image_checker_positive_cond.tmp_img_match_result_list.append(sliced_image_checker_positive_cond(base_img_file, sliced_runtime_img, img_path, res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
                sliced_image_checker_positive_cond.sliced_image_checker_result_list.append(sliced_image_checker_positive_cond(base_img_file, sliced_runtime_img, img_path, res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
            else:
                sliced_image_checker_positive_cond.tmp_img_match_result_list.append(sliced_image_checker_positive_cond(base_img_file, sliced_runtime_img, "", res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
                sliced_image_checker_positive_cond.sliced_image_checker_result_list.append(sliced_image_checker_positive_cond(base_img_file, sliced_runtime_img, "", res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"], str(row_no), str(result),res_obj_json[0]["msg"]))
            sliding_window_positive_cond_summary.result_list.append(sliding_window_positive_cond_summary(base_img_file, orig_runimg, str(result).lower()))
            copyfile(orig_runimg, str(os.path.join(dt["compare_args"]["positive_cond_reports_path"],str(os.path.basename(orig_runimg)))))
            print("Matched - postive:",sliced_runtime_img)
            print("positive cond reports path:", str(os.path.join(dt["compare_args"]["positive_cond_reports_path"],str(os.path.basename(orig_runimg)))))
            time.sleep(1)
            break
        else:
            sliding_window_positive_cond_summary.result_list.append(sliding_window_positive_cond_summary(base_img_file, orig_runimg, str(result).lower()))
            copyfile(orig_runimg, str(os.path.join(dt["compare_args"]["positive_cond_reports_path"],str(os.path.basename(orig_runimg)))))
            print("check_postive_condition:failed")
            #a = cv2.imread(sliced_runtime_img)
            #cv2.imshow("Window", a)
            #time.sleep(15)

        res_obj_json = [] 
        tmp_match_data = []
        imageops.image_match_outcome_list = []

        search_full_region = str(dt["compare_args"]["sliding_window"]["positive_conditions"]["search_full_image_region"]).lower()
        multi_baselining = str(dt["compare_args"]["sliding_window"]["positive_conditions"]["multi_baselining"]).lower()
        if(search_full_region == "false" and multi_baselining == "false" ):
            print("breaking after first cycle:",dt["compare_args"]["sliding_window"]["positive_conditions"]["search_full_image_region"])
           # time.sleep(10)            
            break
    res_obj_json = [] 
    tmp_match_data = []
    imageops.image_match_outcome_list = []
    dt["compare_args"]["copied_baseline_to_temp_location"] = "true"

    return sliced_image_checker_positive_cond.tmp_img_match_result_list, sliced_image_checker_positive_cond.sliced_image_checker_result_list, result, dt



#def compare_image(sliced_run_img, dt):
#    baseline_img = os.path.join(str(dt["compare_args"]["sliding_window"]["negative_conditions"]["negative_baseline_path"]))
#    runtime_img_path = Image.open(sliced_run_img)
#    runtime_img = os.path.join(runtime_img_path + sliced_run_img)


def get_sliding_window_configs(dt):
    max_consecutive_failures_per_row = dt["compare_args"]["sliding_window"]["max_consecutive_failures_per_row_for_anomaly_condition"]
    max_rows_with_anomaly_for_failure_condition = dt["compare_args"]["sliding_window"]["max_rows_with_anomaly_for_failure_condition"]
    count_anomaly_only_in_consecutive_rows = dt["compare_args"]["sliding_window"]["count_anomaly_only_in_consecutive_rows"]
    window_width = dt["compare_args"]["sliding_window"]["window_width"]
    window_height = dt["compare_args"]["sliding_window"]["window_height"]
    stepsize = dt["compare_args"]["sliding_window"]["stepsize"]
    return max_consecutive_failures_per_row, max_rows_with_anomaly_for_failure_condition, count_anomaly_only_in_consecutive_rows, window_width, window_height, stepsize


def get_positive_img_list(dt):
    positive_img_path = str(dt["compare_args"]["sliding_window"]["positive_conditions"]["positive_baseline_path"])
    pos_baseline_imgs_list = get_files(str(os.path.dirname(positive_img_path)))
    pos_baseline_imgs_list = gen_utils.sort(pos_baseline_imgs_list)
    return pos_baseline_imgs_list, len(pos_baseline_imgs_list)
    

# Created on 01-Sep-2021 03:45 AM
def get_positive_imglist_idx(dt):
    positive_img_path = str(dt["compare_args"]["sliding_window"]["positive_conditions"]["positive_baseline_path"])
    pos_baseline_imgs_list, idx_list_cnt = get_positive_img_list(dt)
    idx_list = []
    for img in pos_baseline_imgs_list:
        idx = str(os.path.basename(img)).split("_")[1].split(".")[0]
        idx_list.append(idx)
   
    return idx_list , idx_list_cnt


# Created on 01-Sep-2021 07:00 AM, 01:30 PM
def positive_lookup_configured(dt, idx):
    positive_condition_lookup = False
    idx_list , idx_list_cnt = get_positive_imglist_idx(dt)
    if idx_list_cnt <= 0:
        return False,idx_list
    return True, idx_list

    
def should_do_positive_lookup(dt, idx):
    positive_condition_lookup = False
    lookup_configured_result, idx_list = positive_lookup_configured(dt, idx)
    if not lookup_configured_result:
        return False

    if(str(dt["compare_args"]["sliding_window"]["positive_conditions"]["search_full_image_region"]).lower() == "true"):
        return True
    if(str(dt["compare_args"]["sliding_window"]["positive_conditions"]["search_full_image_region"]).lower() == "false"):
        if(idx_list.__contains__(str(idx))):
            positive_condition_lookup = True
            print("found the match - pos_img_idx == idx:",idx)
            #time.sleep(3)
    return positive_condition_lookup
    
def resize(imFile,width,height):
    img = Image.open(imFile)
    out = img.resize((width,height))
    print("out------------------:",out.size)
    return out

        
def crop_images_for_baselining(dt):
    if(str(dt["compare_args"]["sliding_window"]["baseline_preparation"]["reference_run"]).lower() == "false"):
        return
    all_runtime_imgs_list = get_files(str(os.path.dirname(dt["compare_args"]["runtime_imgs_path"])))
    if(len(all_runtime_imgs_list) <= 0):
        print("no such path or no image files found in the path:",str(os.path.dirname(dt["compare_args"]["runtime_imgs_path"])))
        return False
    
    max_consecutive_failures_per_row, max_rows_with_anomaly_for_failure_condition, count_anomaly_only_in_consecutive_rows, window_width, window_height, stepsize = get_sliding_window_configs(dt)
    (winW, winH) = (int(window_width), int(window_height)) 
    prev_y = 0 
    prev_y1 = 0
    idx = 1
    row_no = 1
    jump_next_y = False
    imgs_with_anomaly = []
    net_result = True
    consecutive_failures_per_row_curr_cnt = 0
    consecutive_rows_with_anomaly_curr_cnt = 0
    runtime_img_path,temp_runtime_path = get_runtime_paths(dt)
    baseline_path = str(dt["compare_args"]["sliding_window"]["baseline_preparation"]["image_storage_path"]+"/")
    algo_artifacts_handler.del_runtime_sliced_images(baseline_path, "true")
    algo_artifacts_handler.create_reports_path(baseline_path)
    #image1 = image2 = resize(img_file2,image1.size[0],image1.size[1])
    #resize_imgs(dt)

    for image in all_runtime_imgs_list:
        #print("all_runtime_imgs_list:",all_runtime_imgs_list)
        #time.sleep(4)
        #print("sliding-window-runtime-image:",os.path.join(runtime_img_path,image))
        #time.sleep(2)

        run_img = cv2.imread(os.path.join(runtime_img_path,image))
        runtime_img = Image.open(os.path.join(runtime_img_path,image))

        # loop over the image pyramid
        for resized in pyramid(run_img, scale=1.5):
	        # loop over the sliding window for each layer of the pyramid
            for (x, y, window) in sliding_window(resized, stepSize=int(stepsize), windowSize=(winW, winH)): #, jump_next_y=False):
		        # if the window does not meet our desired window size, ignore it
                if window.shape[0] != winH or window.shape[1] != winW:
                    continue
                
                clone = resized.copy()
                x1 = (x + winW)
                y1 = (y + winH)
                sliced_img = os.path.join(baseline_path, "slice_"+str(idx)+".png")
                #dt["compare_args"]["runtime_img"] = sliced_img
                #numpydata = asarray(resized) # image converted to numpy array
                cv2.rectangle(clone, (x, y), (x1, y1), (0, 255, 0), 2)
                cv2.imshow("Window -"+image, clone)
                cv2.waitKey(1)

                img_cropped = runtime_img.crop((x,y,x1,y1))

                img_cropped.save(sliced_img)
                idx = idx + 1
    if(idx > 1):
        print("created image set for baselining...")
        return True
    else:
        print("Unable to create image set for baselining...")
        return False





def slide_window(all_runtime_imgs_list, dt):
    # if winW and winH are decremented, then correspondingly stepSize too must be adjusted i.e. stepSize shouldn't be much higher than winW and winH
    # stepSize denotes the steps to be skipped successively. 
    # If winW and winH are lesser than stepSize, then some regions won't be covered. Ex: (winW, winH) = (150, 150) and stepSize=200
    # presence vs. absence of anomalies : 
    #   - checking for the presence of anomalies is leading to more deterministic, conclusive and exploring within finite set of domain
    #   - On the other hand, checking for the presence of non-anomalies is leading to less deterministic, open-ended, and exploring within large set of unpredictable and unknown domain
    max_consecutive_failures_per_row, max_rows_with_anomaly_for_failure_condition, count_anomaly_only_in_consecutive_rows, window_width, window_height, stepsize = get_sliding_window_configs(dt)
    (winW, winH) = (int(window_width), int(window_height)) 
    prev_y = 0 
    prev_y1 = 0
    idx = 1
    row_no = 1
    imgs_with_anomaly = []
    sliced_run_img = ""
    row_moves = 1
    net_result = True
    jump_next_y = False
    consecutive_failures_per_row_curr_cnt = 0
    consecutive_rows_with_anomaly_curr_cnt = 0
    runtime_img_path,temp_runtime_path = get_runtime_paths(dt)
    #pos_img_idxlist, idxlist_cnt = get_positive_imglist_idx(dt)
    positive_condition_lookup = False
    dt["compare_args"]["max_consecutive_failures_per_row_for_anomaly_condition"] = ""
    dt["compare_args"]["max_rows_with_anomaly_for_failure_condition"] = ""
    dt["compare_args"]["consecutive_failures_per_row_curr_cnt"] = "0"
    dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"] = "0"
    dt["compare_args"]["count_anomaly_only_in_consecutive_rows"] = "false"
    for image in all_runtime_imgs_list:
        print("all_runtime_imgs_list:",all_runtime_imgs_list)
        #print("sliding-window-runtime-image:",os.path.join(runtime_img_path,image))
        #time.sleep(6)
        #time.sleep(4)
        run_img = cv2.imread(os.path.join(runtime_img_path,image))
        runtime_img = Image.open(os.path.join(runtime_img_path,image))
        row_no = 1
        row_marker = 0

        # loop over the image pyramid
        for resized in pyramid(run_img, scale=1.5):
	        # loop over the sliding window for each layer of the pyramid
            for (x, y, window) in sliding_window(resized, stepSize=int(stepsize), windowSize=(winW, winH)):
                print("image:",image)
		        # if the window does not meet our desired window size, ignore it
                print(window.shape[0]," ", winH)
                print(window.shape[1], " ", winW )
                #time.sl]eep(3)
                if (window.shape[0] != winH or window.shape[1] != winW): #or row_moves > 5:
                    #x=resized.shape[1]
                    #print("continue")
                    
                    #if(sliced_run_img.__contains__("slice_32.png") or sliced_run_img.__contains__("slice_33.png") or sliced_run_img.__contains__("slice_34.png")):
                    #    print('int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]',int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]))
                    #    print("consecutive_rows_with_anomaly_curr_cnt:",consecutive_rows_with_anomaly_curr_cnt)
                    #    time.sleep(5)
                    
                    #print("BBBBBBBBBBB:",int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]))
                    #time.sleep(7)
                    #if(int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]) >= int(dt["compare_args"]["max_consecutive_failures_per_row_for_anomaly_condition"])):
                    
                    spl_anomaly_classification = int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]) >= int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"])
                    print("crow_urr_cnt:",int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]))
                    print("-----val----:",int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"]))
                    print("spl_anomaly_classification:",spl_anomaly_classification)
                    time.sleep(4)
                    #print("spl_anomaly_condition:",spl_anomaly_classification)

                    #print("RUNTIME : MAX CONSECUTIVE FAILURES IN THE CURRENT ROW = ", int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]),", CONFIG : UNFULFILLED_MAX_CONSECUTIVE_FAILURES_DEEMED_ANOMALY = ", int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"]))
                    #print("RUNTIME : CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT-1 = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), ", CONFIG : MAX_ROWS_WITH_ANOMALY_FOR_FAILURE_CONDITION = ", int(max_rows_with_anomaly_for_failure_condition) )

                    #time.sleep(2) #--exp
                    #cv2.waitKey(1)

                    #if(int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]) == int(dt["compare_args"]["sliding_window"]["intermittent_failure_count_deemed_anomaly"])):
                    #    print("MACTHED-IMPLEMET THE SOLUTION:::::")
                    #    time.sleep(10)
                    
                    
                    if(int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]) >= int(max_consecutive_failures_per_row) or spl_anomaly_classification):
                        #if(dt["compare_args"]["count_anomaly_only_in_consecutive_rows"] == "true"):
                        if(count_anomaly_only_in_consecutive_rows == "true"):
                            print("row_marker:",row_marker)
                            print("row_no:",row_no)

                            if(row_marker == 0 or  (row_marker+1) == row_no or spl_anomaly_classification): # row_marker = 0 denotes a new image being scanned. Checking for (row_marker+1)==row_no is used to check that if an anomaly has occurred in back-to-back rows
                                #print("RUNTIME : CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT-1A = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), ", CONFIG : MAX_ROWS_WITH_ANOMALY_FOR_FAILURE_CONDITION = ", int(max_rows_with_anomaly_for_failure_condition) )
                                consecutive_rows_with_anomaly_curr_cnt += 1
                                dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"] = str(consecutive_rows_with_anomaly_curr_cnt)
                                row_marker = row_no
                                #print("consecutive_rows_with_anomaly_curr_cnt-+++++++:",consecutive_rows_with_anomaly_curr_cnt)
                                #print("RUNTIME : CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT-1B = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), ", CONFIG : MAX_ROWS_WITH_ANOMALY_FOR_FAILURE_CONDITION = ", int(max_rows_with_anomaly_for_failure_condition) )
                                #tihme.sleep(6) #--exp
                                cv2.waitKey(1)
                                if(str(os.path.basename(image)) not in imgs_with_anomaly):
                                    imgs_with_anomaly.append(str(os.path.basename(image)))
                                    ########### Add the entry to the data model list for the summary report generation ################
                                    sliding_window_negative_cond_summary.result_list.append(sliding_window_negative_cond_summary(image))
                                    #print("imgs_with_anomaly:",imgs_with_anomaly)
                                    #time.sleep(5)  --exp
                                    #cv2.waitKey(1)
                        else:
                            consecutive_rows_with_anomaly_curr_cnt += 1
                            dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"] = str(consecutive_rows_with_anomaly_curr_cnt)
                            if(str(os.path.basename(image)) not in imgs_with_anomaly):
                                imgs_with_anomaly.append(str(os.path.basename(image)))
                                ########### Add the entry to the data model list for the summary report generation ################
                                sliding_window_negative_cond_summary.result_list.append(sliding_window_negative_cond_summary(image))
                                #print("imgs_with_anomaly:",imgs_with_anomaly)
                                #time.sleep(5) --exp   
                                #cv2.waitKey(1)


                        #print("dt[compare_args][consecutive_failures_per_row_curr_cnt]:",dt["compare_args"]["consecutive_failures_per_row_curr_cnt"])
                        #print("consecutive_rows_with_anomaly_curr_cnt-INCREMENTED:",consecutive_rows_with_anomaly_curr_cnt)
                        
                        #print(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"])
                        #time.sleep(5)
                    else:
                        #print("consecutive_rows_with_anomaly_curr_cnt:",consecutive_rows_with_anomaly_curr_cnt)
                        #time.sleep(2)
                        #print("consecutive_rows_with_anomaly_curr_cnt:",consecutive_rows_with_anomaly_curr_cnt)
                        #print("RUNTIME : CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT-1C = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), ", CONFIG : MAX_ROWS_WITH_ANOMALY_FOR_FAILURE_CONDITION = ", int(max_rows_with_anomaly_for_failure_condition) )
                        consecutive_rows_with_anomaly_curr_cnt = 0
                        dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"] = str(consecutive_rows_with_anomaly_curr_cnt)
                        #print("RUNTIME : CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT-1D = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), ", CONFIG : MAX_ROWS_WITH_ANOMALY_FOR_FAILURE_CONDITION = ", int(max_rows_with_anomaly_for_failure_condition) )
                    
                        #time.sleep(2)


                    #if(int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]) >= int(dt["compare_args"]["max_rows_with_anomaly_for_failure_condition"])):
                    #print("RESULT-consecutive_rows_with_anomaly_curr_cnt-2:",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]), " ", int(max_rows_with_anomaly_for_failure_condition) )
                    #time.sleep(5) --exp
                    
                    print()
                    print()
                    print()
                    print("                             =================")
                    print("                             ANALYSIS SUMMARY")
                    print("                             =================")
                    print()
                    print("CONFIG : MAX NUMBER OF SLIDING ROWS WITH ANOMALY FOR FAILURE CONDITION         = ", int(max_rows_with_anomaly_for_failure_condition) )
                    if(len(str(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"])) > 0 and int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"]) != 0 ):
                        print("ANOMALY INFERENCE SPECIAL WAIVER : ENABLED.  CONFIG : UNFULFILLED_MAX_CONSECUTIVE_FAILURES_DEEMED_ANOMALY = ",int(dt["compare_args"]["sliding_window"]["unfulfilled_max_consecutive_failures_deemed_anomaly"]))
                    else:
                        print("ANOMALY INFERENCE SPECIAL WAIVER : DISABLED. CONFIG : UNFULFILLED_MAX_CONSECUTIVE_FAILURES_DEEMED_ANOMALY = 0")
                    print()
                    print("                              RUNTIME SECTION")
                    print("                              ****************")
                    print("RUNTIME : MAX CONSECUTIVE FAILURES DETECTED IN THE CURRENT SLIDING ROW = ", int(dt["compare_args"]["consecutive_failures_per_row_curr_cnt"]))
                    print("RUNTIME : TOTAL CONSECUTIVE SLIDING ROWS WITH ANOMALY  = ",int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]))

                    #cv2.waitKey(1)

                    if(int(dt["compare_args"]["consecutive_rows_with_anomaly_curr_cnt"]) >= int(max_rows_with_anomaly_for_failure_condition)):
                        net_result = False
                        #print("NET RESULT : FALSE. CONSECUTIVE_ROWS_WITH_ANOMALY_CURR_CNT:",consecutive_rows_with_anomaly_curr_cnt)
                    #    time.sleep(5)

                    if(net_result):
                        print("NET RUN RESULT  : NO ANOMALIES FOUND")
                    else:
                        print("NET RUN RESULT  : ANOMALIES FOUND")
                    print("ANOMALIES DETECTED IN IMAGES :",imgs_with_anomaly)
                    print()
                    print("============================================================================================================")
                    time.sleep(2)

                    #time.sleep(2)
                    dt["compare_args"]["consecutive_failures_per_row_curr_cnt"] = "0"
                    row_no += 1
                    prev_row = row_no
                    runtime_img_path, sliced_imgs_runtime_path = get_runtime_paths(dt)
                    #print("check this text now-----")
                    #time.sleep(5)
                    #winW = 22
                    #if(row_moves >= 5):
                    #    jump_next_y = True
                    #    row_moves = 1
                    continue
                
                positive_condition_lookup = should_do_positive_lookup(dt, idx)
                print("sliding_window():::positive_condition_lookup:",positive_condition_lookup)
                #time.sleep(3)

                clone = resized.copy()
                x1 = (x + winW)
                y1 = (y + winH)
                sliced_run_img = os.path.join(temp_runtime_path, "slice_"+str(idx)+".png")
                dt["compare_args"]["runtime_img"] = sliced_run_img
                #numpydata = asarray(resized) # image converted to numpy array
                cv2.rectangle(clone, (x, y), (x1, y1), (0, 255, 0), 2)
                img_cropped = runtime_img.crop((x,y,x1,y1))

                img_cropped.save(sliced_run_img)
                res_obj_json_persist, result,dt = compare(os.path.join(runtime_img_path,image), sliced_run_img, row_no, dt, False)
                print("sliding_window]()::negative cond",result)
                #time.sleep(2)
                
                if(result and positive_condition_lookup): # positive condition lookup
                    res_obj_json_persist, result,dt = compare(os.path.join(runtime_img_path,image),sliced_run_img, row_no, dt, True)
                    print("res_obj_json_persist:",res_obj_json_persist)
                    print("look for this ------   compare result:",result)
                    #time.sleep(10)
                    

                #print((x, y), (x1, y1))
                #if(y > prev_y and (y + winH) > prev_y1 ):
                if(y > prev_y and y1 > prev_y1):
                    print(y," ",prev_y,"======",y1," ",prev_y1)
                    prev_y = y
                    #prev_y1 = (y + winH)
                    prev_y1 = y1
                    #time.sleep(2)
                    row_no += 1
                cv2.imshow("Window -"+image, clone)
                cv2.waitKey(1)
                #time.slee0p(0.025)
                print("GETTING READY FOR THE NEXT ITERATION....")
                #time.sleep(0.05)
                #img2 = cv2.imread(str(idx)+".png")
                #cv2.imwrite("cropped.png",img2)
                del_sliced_imgs_upon_crossing_upper_limit()
                idx = idx + 1
                #row_moves += 1
                pos_cond_located = False
    return res_obj_json_persist, result , imgs_with_anomaly, net_result


# Created on 30-Aug-2021 01:00 AM
def del_sliced_imgs_upon_crossing_upper_limit():
    temp_runtime_path = os.path.join(str(dt["compare_args"]["runtime_imgs_path"]),"slices")
    if len([name for name in os.listdir(temp_runtime_path) if os.path.isfile(os.path.join(temp_runtime_path, name))]) > 500:
        print("total files:",len([name for name in os.listdir(temp_runtime_path) if os.path.isfile(os.path.join(temp_runtime_path, name))]))
        algo_artifacts_handler.del_files_in_folder(temp_runtime_path)


def compare_slices(dt):
    all_runtime_imgs_list = get_files(str(os.path.dirname(dt["compare_args"]["runtime_imgs_path"])))
    if(len(all_runtime_imgs_list) <= 0):
        print("no such path or no image files found in the path:",str(os.path.dirname(dt["compare_args"]["runtime_imgs_path"])))
        return [],False
    all_runtime_imgs_list = gen_utils.sort(all_runtime_imgs_list)
    total_images= len(all_runtime_imgs_list)
    result_set, result, imgs_with_anomaly, net_result = slide_window(all_runtime_imgs_list, dt)
    return result_set, result, imgs_with_anomaly, net_result


def preprocess_paths(dt, reports_path, net_result_path, should_purge_oldartifacts):
    if(str(dt["compare_args"]["sliding_window"]["baseline_preparation"]["reference_run"]).lower() == "true"):
        return "","","",dt
    dt, runtime_img_path, sliced_imgs_runtime_path = format_paths(dt)
    #runtime_img_path, sliced_imgs_runtime_path = get_runtime_paths(dt)
    runtime_baseline_tmp_path = os.path.join(runtime_img_path, "b_temp")
    runtime_tmp_path = os.path.join(runtime_img_path, "r_temp")
    failed_slices_path = os.path.join(reports_path,"failed_slices")
    dt["compare_args"]["failed_slices_path"] = failed_slices_path
    positive_cond_reports_path = os.path.join(reports_path,"positives")
    dt["compare_args"]["positive_cond_reports_path"] = positive_cond_reports_path
    original_reports_path = dt["compare_args"]["comp_reports_path"]
    dt["compare_args"]["comp_reports_path"] = str(os.path.join(original_reports_path, "diffs"))
    algo_artifacts_handler.handle_report_result_paths(reports_path, net_result_path, should_purge_oldartifacts)
    algo_artifacts_handler.del_runtime_sliced_images(sliced_imgs_runtime_path, should_purge_oldartifacts)
    algo_artifacts_handler.del_runtime_sliced_images(runtime_baseline_tmp_path, should_purge_oldartifacts)
    algo_artifacts_handler.del_runtime_sliced_images(runtime_tmp_path, should_purge_oldartifacts)
    algo_artifacts_handler.create_runtime_sliced_imgs_path(sliced_imgs_runtime_path, True)
    algo_artifacts_handler.create_failed_sliced_imgs_path(failed_slices_path, True)
    algo_artifacts_handler.create_failed_sliced_imgs_path(positive_cond_reports_path, True)
    return runtime_img_path, sliced_imgs_runtime_path, original_reports_path, dt

    

############################### driver program #######################################
preprocessing_needed = True
preprocessing_finished = False
start_time = time.time()
args = gen_utils.parse_args()
dt, reports_path, net_result_path, should_purge_oldartifacts = retriveConfigs(args)
dt = create_special_keys(dt)
dt = set_run_mode_to_historical(dt)
runtime_img_path, sliced_imgs_runtime_path, original_reports_path, dt = preprocess_paths(dt,reports_path, net_result_path, should_purge_oldartifacts)

logfile = str(os.path.join(reports_path,'sliding_window_scanner.log')).replace('\\','/')
#logging.basicConfig(filename=logfile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
#logging.getLogger().setLevel(logging.INFO)
if(str(dt["compare_args"]["sliding_window"]["baseline_preparation"]["reference_run"]).lower() == "false"):
    result_set, result,imgs_with_anomaly, net_result = compare_slices(dt)
else:
    crop_images_for_baselining(dt)
    sys.exit()

if(dt["compare_args"]["sliced_images_comparison_report_needed"]) == "true":
    sliced_detailed_report_obj = generate_report(sliced_image_checker_negative_cond.sliced_image_checker_result_list, original_reports_path, "data_gap_sliced_imgs_comp_report.json")

if(dt["compare_args"]["sliced_images_positive_comparison_report_needed"]) == "true":
    sliced_detailed_report_obj = generate_report(sliced_image_checker_positive_cond.sliced_image_checker_result_list, original_reports_path, "positive_cond_sliced_imgs_comp_report.json")

if(len(sliding_window_negative_cond_summary.result_list) > 0):
    sliding_window_summary_rep_obj = generate_report(sliding_window_negative_cond_summary.result_list, original_reports_path, "data_gap_detection_report.json")
else:
    file1 = open(os.path.join(original_reports_path,"no_anomalies.txt"), "a")
    file1.write("PASSED")

if(len(sliding_window_positive_cond_summary.result_list) > 0):
    sliding_window_summary_rep_obj = generate_report(sliding_window_positive_cond_summary.result_list, original_reports_path, "positive_condition_checker_report.json")
elif(not sliding_window_positive_cond_summary.result_list.__contains__("true")):
    file1 = open(os.path.join(original_reports_path,"failed_positive_conditions.txt"), "a")
    file1.write("FAILED")


if(net_result):
    imgs_with_anomaly = []
print('anomaly detected in :',  imgs_with_anomaly, net_result)
             
#print(sliced_image_checker_negative_cond.sliced_image_checker_result_list)



'''
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-s", "--scale", type=float, default=1.5, help="scale factor size")
args = vars(ap.parse_args())
# load the image
image = cv2.imread(args["image"])
# METHOD #1: No smooth, just scaling.
# loop over the image pyramid
for (i, resized) in enumerate(pyramid(image, scale=args["scale"])):
	# show the resized image
	cv2.imshow("Layer {}".format(i + 1), resized)
	cv2.waitKey(0)
# close all windows
cv2.destroyAllWindows()
# METHOD #2: Resizing + Gaussian smoothing.
#for (i, resized) in enumerate(pyramid_gaussian(image, downscale=2)):
	# if the image is too small, break from the loop
	#if resized.shape[0] < 30 or resized.shape[1] < 30:
#		break
		
	# show the resized image
#	cv2.imshow("Layer {}".format(i + 1), resized)
	#cv2.waitKey(0)
'''
    

'''
img=cv2.imread('C:/py/RTImages/realtime/test/RT_Time_Image_125.png')
scale=3
y_len,x_len,_=img.shape

mean_values=[]
for y in range(scale):
    for x in range(scale):
        cropped_image=img[(y*y_len)/scale:((y+1)*y_len)/scale,(x*x_len)/scale:((x+1)*x_len)/scale]

    mean_val,std_dev=cv2.meanStdDev(cropped_image)
    mean_val=mean_val[:3]

    mean_values.append([mean_val])
mean_values=np.asarray(mean_values)
print(mean_values.reshape(3,3,3))
'''