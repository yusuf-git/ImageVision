#/############################################################
# Author : Yusuf
# Created : 28-Nov-2020 10:45 AM
# updates on : 29-Nov-2020 02:50 AM, 24-Oct-2021 02:40 AM
###############################################################
# create a thumbnail of an image
import sys
import os
#sys.path.insert(0, 'path/to/your/py_file')
sys.path.insert(0, os.path.realpath(os.path.pardir))
import logging
import time
import argparse
import json
import shutil
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
#import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import compare_ssim
import pyautogui as pygui
from cv_img_libs import BRISK_FLANN_baseline_utils_lib
from cv_img_libs import config_utils_lib
from cv_img_libs import img_comp_utils
from algos_namelist import comp_algos
from cv_img_libs import gen_utils
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.cons_results_data_model import cons_results_data_model
import cv2
import imutils
import imagehash
import jsonpickle
#from di_container import di_container
import img_comparator



# created on 17-Nov-2020 02:25 AM #
def write_consolidated_result(cons_result_file, nonserializable_result_obj, stringformat=True, filemode = "w"):
    cons_res_string = json.dumps([o.dump() for o in nonserializable_result_obj])
    serializable_result_obj = json.loads(cons_res_string) 
    img_comp_utils.writeJson(cons_result_file, serializable_result_obj, stringformat, filemode)


# created on 16-Nov-2020 08:15 PM
def get_phash_result_metrics(p_hash_algo_op, res_obj_dict, k):
    phash_img = ""
    phash_score = ""
    phash_msg = ""
    if(p_hash_algo_op == False):
        return phash_img, phash_score, phash_msg
    res_obj = res_obj_dict["phash"]
    phash_img = res_obj[k]["image"]
    phash_score = res_obj[k]["original_score"]
    phash_msg = res_obj[k]["msg"]
    return phash_img, phash_score, phash_msg

# created on 16-Nov-2020 08:30 PM
def get_dhash_result_metrics(d_hash_algo_op, res_obj_dict, k):
    dhash_img = ""
    dhash_score = ""
    dhash_msg = ""
    if(d_hash_algo_op == False):
        return dhash_img, dhash_score, dhash_msg
    res_obj = res_obj_dict["dhash"]
    dhash_img = res_obj[k]["image"]
    dhash_score = res_obj[k]["original_score"]
    dhash_msg = res_obj[k]["msg"]
    return dhash_img, dhash_score, dhash_msg

# created on 16-Nov-2020 08:30 PM
def get_ssi_result_metrics(ssi_algo_op, res_obj_dict, k):
    ssi_img = ""
    ssi_score = ""
    if(ssi_algo_op == False):
        return ssi_img, ssi_score
    #gen_utils.console_verbose_out("printing ssi metrics - res_obj_dict:{}".format(res_obj_dict), dt)
    res_obj = res_obj_dict["ssi"]
    ssi_img = res_obj[k]["image"]
    ssi_score = res_obj[k]["original_score"]
    return ssi_img, ssi_score

# created on 16-Nov-2020 08:35 PM
def get_BF_result_metrics(BF_algo_op, res_obj_dict, k):
    BF_img = ""
    BF_expscore = ""
    BF_originalscore = ""
    if(BF_algo_op == False):
        return BF_img, BF_expscore, BF_originalscore
    res_obj = res_obj_dict["BF"]
    BF_img = res_obj[k]["image"]
    BF_expscore = res_obj[k]["expscore"]
    BF_originalscore = res_obj[k]["original_score"]
    return BF_img, BF_expscore, BF_originalscore


# created on 16-Nov-2020 11:55 PM
def validate_img_name_is_same(phash_img,BF_img,ssi_img,dhash_img):
    tmp = []
    result = True
    tmp_img = ""
    tmp.append(phash_img)
    tmp.append(BF_img)
    tmp.append(ssi_img)
    tmp.append(dhash_img)
    for i in tmp:
        if(i == ""):
            continue
        if(tmp_img == ""):
            tmp_img = i
        if(tmp_img != i):
            result = False
    return tmp_img, result


# created on 16-Nov-2020 03:25 PM #
def check_resultfiles_presence(result_path):
    pixel_comparison_op = bool(os.path.exists(os.path.join(result_path, ssi_result)))
    ssi_algo_op = bool(os.path.exists(os.path.join(result_path, ssi_result)))
    BF_algo_op = bool(os.path.exists(os.path.join(result_path, BF_result)))
    p_hash_algo_op = bool(os.path.exists(os.path.join(result_path, p_hash_result)))
    d_hash_algo_op = bool(os.path.exists(os.path.join(result_path, d_hash_result)))
    haar_cascade_algo_op = bool(os.path.exists(os.path.join(result_path, ssi_result)))
    return pixel_comparison_op, p_hash_algo_op, BF_algo_op, ssi_algo_op, d_hash_algo_op, haar_cascade_algo_op

# created on 16-Nov-2020 04:30 PM #
def read_result_files(result_file_list,dt):
    gen_utils.console_verbose_out(result_file_list,dt)
    #time.sleep(10)
    res_obj_dict = {}
    res_dict_elem_cnt = {}
    for result_file in result_file_list:
        result_obj = img_comp_utils.readJson_plain(result_file)
        result_str = json.dumps(result_obj)
        result_str = str(result_str)
        result_obj_json = json.loads(result_str)

        if(os.path.basename(result_file)==ssi_result):
            res_obj_dict["ssi"] = result_obj_json
            res_dict_elem_cnt["ssi"] = len(result_obj_json)
        elif(os.path.basename(result_file)==BF_result):
            res_obj_dict["BF"] = result_obj_json
            res_dict_elem_cnt["BF"] = len(result_obj_json)
        elif(os.path.basename(result_file)==p_hash_result):
            res_obj_dict["phash"] = result_obj_json
            res_dict_elem_cnt["phash"] = len(result_obj_json)
        elif(os.path.basename(result_file)==d_hash_result):
            res_obj_dict["dhash"] = result_obj_json
            res_dict_elem_cnt["dhash"] = len(result_obj_json)
        elif(os.path.basename(result_file)==pixel_result):
            res_obj_dict["pixelcomp"] = result_obj_json
            res_dict_elem_cnt["pixelcomp"] = len(result_obj_json)
        elif(os.path.basename(result_file)==pixel_result):
            res_obj_dict["haar"] = result_obj_json
            res_dict_elem_cnt["haar"] = len(result_obj_json)
    gen_utils.console_verbose_out("res_obj_dict, res_dict_elem_cnt:::{},{}".format(res_obj_dict, res_dict_elem_cnt),dt)
    #time.sleep(10)
    return res_obj_dict, res_dict_elem_cnt



# added on 28-Nov-2020 02:35 AM
# updates on 29-Nov-2020 02:50 AM  #
def consolidate_result(result_file_list,dt):
    k=0
    img = ""
    consolidation_result = True
    if len(result_file_list) <= 0:
        logging.info("Not a single result file found. Consolidated result won't be generated")
        print("Not a single result file found. Consolidated result won't be generated")
        return cons_results_data_model.consolidated_result_list, False
    
    pixel_comp_op, p_hash_algo_op,  BF_algo_op, ssi_algo_op, d_hash_algo_op, haar_cascade_algo_op = check_resultfiles_presence(os.path.dirname(result_file_list[0]))

    res_obj_dict, res_dict_elem_cnt = read_result_files(result_file_list,dt)

    #res_max_cnt = max(res_dict_elem_cnt, key= lambda x: res_dict_elem_cnt[x])   # this prints the key with max value
    res_dict_img_cnt_values = res_dict_elem_cnt.values()
    print("res_dict_img_cnt_values",res_dict_img_cnt_values)
    res_max_cnt = max(res_dict_img_cnt_values)
    print("res_max_cnt",res_max_cnt)

    while(k < res_max_cnt):
        phash_img, phash_score, phash_msg = get_phash_result_metrics(p_hash_algo_op, res_obj_dict, k)
        BF_img, BF_exp_score, BF_orig_score = get_BF_result_metrics(BF_algo_op, res_obj_dict, k)
        ssi_img, ssi_score = get_ssi_result_metrics(ssi_algo_op, res_obj_dict, k)
        dhash_img, dhash_score, dhash_msg = get_dhash_result_metrics(d_hash_algo_op, res_obj_dict, k)

        img, imgname_check = validate_img_name_is_same(phash_img, BF_img, ssi_img, dhash_img)
    
        if imgname_check == False:
            consolidation_result = False
            logging.error("img name :"+phash_img+" ==> image names shouldn't differ among the algos. Idx:"+str(k))
            print("img name :"+phash_img+" ==> image names shouldn't differ among the algos. Idx:"+str(k))
            phash_score = ""
            phash_msg = "image names shouldn't differ among the algos. Idx:"+str(k)
            BF_exp_score = ""
            BF_orig_score = ""
            ssi_score = ""
            dhash_score = ""
            dhash_msg = "image names shouldn't differ among the algos. Idx:"+str(k)
        
        cons_results_data_model.consolidated_result_list.append(cons_results_data_model(img, phash_score, phash_msg, BF_exp_score, BF_orig_score, ssi_score, dhash_score, dhash_msg))
        k = k + 1
    if(consolidation_result == False):
        logging.error("result consolidation is unsuccessful")
    return cons_results_data_model.consolidated_result_list, consolidation_result        

ssi_result = "ssi_report.json"
BF_result = "brisk-flann_report.json"
p_hash_result = "perceptual_hashing_report.json"
d_hash_result = "diff_hashing_report.json"
pixel_result = "pixel_report.json"
haar_cascade_result = "haar_cascade_report.json"
