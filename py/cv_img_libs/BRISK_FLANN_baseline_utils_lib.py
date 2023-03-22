#########################
# created on 21-Nov-2020 03:45 PM
# updates on 
#########################

from logging import log
import os
import sys
sys.path.insert(0, os.path.realpath(os.path.pardir))
from os.path import join, getsize
import pathlib
import time
from shutil import copyfile
import shutil
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2
import imutils
import argparse
import sys
import pyautogui as pygui
from cv_img_libs import img_comp_utils
from cv_img_libs import config_utils_lib
from cv_img_matcher.algos_namelist import comp_algos
import jsonpickle
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.cons_results_data_model import cons_results_data_model
import json
import logging


# updates on 05-Nov-2020 03:45 PM #
def write_BF_baseline_Json(BF_baseline, baseline_data_obj, filemode="w", del_current_file=True):
    #comp_result_data.extend(tmp_match_data)
    img_comp_utils.writeJson(BF_baseline,baseline_data_obj,True, filemode, del_current_file)



# created on 31-Oct-2020 11:05 PM #
# updates on 04-Nov-2020 02:35 AM #
def create_BF_algo_baseline_folder(baseline_path):
    if not os.path.exists(baseline_path):
        print("path for BF algo baseline created dynamically:"+baseline_path)
        logging.info("path for BF algo baseline created dynamically:"+baseline_path)
        os.makedirs(baseline_path)




# created on 03-Nov-2020 11:27 PM
# updates on 11-Nov-2020 12:30 AM
def check_BF_baseline_exists(dt):
    BF_algo_baseline = str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"])
    print("check_BF_baseline_exists",BF_algo_baseline)
    if not os.path.exists(BF_algo_baseline):
        print(":"+ str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"]))
        logging.info("unable to find BF_parametric baseline:"+ str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"]))
        return False
    else:
        return True




# created on 03-Nov-2020 11:50 PM
def check_BF_algo_ops_prereq(algo_idx, dt):
    if(config_utils_lib.get_algo_name_list(dt)[algo_idx] != "BRISK-FLANN"):
        return 2    # different active algo
    if(config_utils_lib.get_algo_name_list(dt)[algo_idx] == "BRISK-FLANN"):
        tmp = check_BF_baseline_exists(dt)
        if not tmp:
            print("BF algo parametric baseline will be generated...")
            logging.info("BF algo parametric baseline will be generated...")
            return 0 # the BF baseline does not exist
        else: # the Bunable to find BF_parametric baselineF baseline exists
            return 1



# created on 09-Nov-2020 12:40 AM #
# updates on 09-Nov-2020 01:05 AM, 11-Nov-2020 12:30 AM, 29-Nov-2020 01:10 AM #
########create, read and process BF algo baseline json - add new image entry to the baseline json###############
def add_new_BF_baseline_entry(_is_BF_active_algo, dt):
    if(len(BF_base_data_model.newimgs_baseline_buffer) <= 0 or _is_BF_active_algo == False):
        return
    i=0
    BF_baseline_file = str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"])
    #if(len(dt["compare_args"]["newimgs_baselinebuffer"]) > 0): /working fine - however, not needed
    BF_res_obj_json = img_comp_utils.readJson_plain(BF_baseline_file)
           
    # the dt data object for the BF is populated while BF algo operation #
    BF_resJson = json.dumps([o.dump() for o in dt["compare_args"]["newimgs_baselinebuffer"]])
    BF_new_entry_obj_json = json.loads(BF_resJson)
    while(i < len(BF_new_entry_obj_json)):
        BF_res_obj_json.append(BF_new_entry_obj_json[i])
        i = i + 1
    write_BF_baseline_Json(BF_baseline_file, BF_res_obj_json, "w", False)
    print("new image entries are auto-added to BRISK-FLANN baseline json")
    logging.info("new image entries are auto-added to BRISK-FLANN baseline json")




# created on 09-Nov-2020 12:40 AM #
# updates on 11-Nov-2020 12:30 AM, 29-Nov-2020 01:10 AM #
def generate_BF_baseline_from_dataobject(_should_generate_BF_baseline_file, dt):
    if(_should_generate_BF_baseline_file == True):
        print("active algo : BRISK-FLANN")
        print(dt["compare_args"]["BF_algo_baseline"])
        BF_baseline_file = str(dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"])
        # the dt data object for the BF is populated while BF algo operation
        BF_resJson = json.dumps([o.dump() for o in dt["compare_args"]["BF_algo_baseline"]])
        BF_res_obj_json = json.loads(BF_resJson) 
        create_BF_algo_baseline_folder(str(os.path.dirname(BF_baseline_file)))     
        write_BF_baseline_Json(BF_baseline_file, BF_res_obj_json)
