#/############################################################
# Author : Yusuf
# Created : 28-Nov-2020 02:45 AM
# Updates : 26-Jul-2021 12:50 PM, 07-Aug-2021 11:55 PM
###############################################################
# create a thumbnail of an image
import sys
import os

from numpy.lib.function_base import diff
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
#from algos_namelist import comp_algos
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.cons_results_data_model import cons_results_data_model
import cv2
import imutils
import imagehash
import jsonpickle
#from di_container import di_container
#import img_comparator


# added on 28-Nov-2020 02:30 AM #
# updates on 28-Nov-2020 11:55 PM #
def del_prev_artifacts(img_ops_session_rootpath,should_purge_oldlog):
    try:
        prev_sessionspath = os.path.join(img_ops_session_rootpath)
        if(should_purge_oldlog.lower() == "true" and os.path.exists(prev_sessionspath) is True):
            shutil.rmtree(prev_sessionspath)
    except:
        print("error :: deleting prev. artifacts....Not done")



# added on 28-Nov-2020 02:30 AM #
# updates on 28-Nov-2020 11:55 PM #
def createartifactspaths(dt):
    import datetime
    img_ops_session_rootpath = str(dt["compare_args"]["img_ops_session_rootpath"])
    should_purge_oldlog = str(dt["compare_args"]["purge_old_artifacts"])
    #x = datetime.datetime.now()
    #dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
    del_prev_artifacts(img_ops_session_rootpath, should_purge_oldlog)
    diff_path = os.path.join(str(dt["compare_args"]["comp_reports_path"]))
    log_results_path = os.path.join(os.path.abspath(os.path.join(diff_path, os.pardir)),"reports")
    if not os.path.exists(log_results_path):
        os.makedirs(log_results_path)
    print("algo operation reports path:",log_results_path," created...")
    return log_results_path



def WriteJsonlog(curr_algo_log, comp_result_data, _is_img_path_update_needed=True):
    n=0
    #comp_result_data.extend(tmp_match_data)
    while(len(comp_result_data) > 0 and n < len(comp_result_data) and _is_img_path_update_needed):
        if(n > 0):
            comp_result_data[n]["base_img_path"] = ""
            comp_result_data[n]["runtime_img_path"] = ""
        n = n + 1
    if(os.path.exists(curr_algo_log)):
        os.unlink(curr_algo_log)    
    img_comp_utils.writeJson(curr_algo_log,comp_result_data,True)
    #img_comp_utils.writeJson("match_op_log.json",comp_result_data, True)   


##########################################REPORTS PATH HANDLER###############################
# Created on 02-Aug-2021 09:20 AM
# Updates on 07-Aug-2021 07:50 AM, 04:40 PM
def del_repo_result_paths(repo_result_path, should_purge_oldlog):
    try:
        if(os.path.isfile(repo_result_path)):
            repo_result_path = os.path.dirname(repo_result_path)
        if(should_purge_oldlog.lower() == "true" and os.path.exists(repo_result_path)):
            shutil.rmtree(repo_result_path)
            #for filename in os.listdir(repo_result_path):
            #    curr_item = os.path.join(repo_result_path, filename)
            #    if os.path.isfile(curr_item):
            #        os.unlink(curr_item)
            #    elif os.path.isdir(curr_item):
            #        shutil.rmtree(curr_item)
            logging.info("all files deleted in the path:",repo_result_path)
            #print("all files deleted in the path:",repo_result_path)
            #time.sleep(10)
    except:
        print("ImageVision error:<can't delete files in ",repo_result_path,">")
        logging.error("ImageVision error:<can't delete files in ",repo_result_path,">")



# Created on 02-Aug-2021 11:30 AM, 11:15 PM
# Updates on 07-Aug-2021 10:15 AM, 04:30 PM
def create_reports_path(repo_result_path):
    try:
        if(os.path.isfile(repo_result_path)):
            repo_result_path = os.path.dirname(repo_result_path)
        if(not os.path.exists(repo_result_path)):
            os.makedirs(repo_result_path)
        logging.info(repo_result_path, " created")
    except:
        print("ImageVision error:<can't create ",repo_result_path,">")
        logging.error("ImageVision error:<can't create ",repo_result_path,">")


# Created on 03-Aug-2021 09:00 AM
# Updates on 07-Aug-2021 10:00 AM, 04:30 PM, 15-Aug-2021 08:40 PM, 08-Sep-2021 01:00 AM
def handle_report_result_paths(reports_path, net_result_path, should_purge_oldlog, output_path=""):
    misc_path = ""
    if(output_path == ""):
        misc_path = os.path.join(reports_path,"diffs")
    else:
        misc_path = output_path
    del_repo_result_paths(reports_path, should_purge_oldlog)
    del_repo_result_paths(net_result_path, should_purge_oldlog)
    create_reports_path(reports_path)
    create_reports_path(net_result_path)
    create_reports_path(misc_path)
    return


# Created on 15-Aug-2021 06:10 PM
def del_runtime_sliced_images(path, should_purge_oldlog):
    if(os.path.isfile(path)):
        path = os.path.dirname(path)
    if(should_purge_oldlog.lower() == "true" and os.path.exists(path)):
        shutil.rmtree(path)

    

# Created on 30-Aug-2021 12:50 AM
def del_files_in_folder(path):
    for f in os.listdir(path):
        os.remove(os.path.join(path, f))


# Created on 15-Aug-2021 11:00 PM
def create_runtime_sliced_imgs_path(runtime_sliced_imgs_path, should_create=False):
    if(not should_create):
        return
    if(not os.path.exists(runtime_sliced_imgs_path)):
        os.makedirs(runtime_sliced_imgs_path)
    return

# Created on 17-Aug-2021 01:45 AM
def create_failed_sliced_imgs_path(failed_sliced_imgs_path, should_create=False):
    if(not should_create):
        return
    if(not os.path.exists(failed_sliced_imgs_path)):
        os.makedirs(failed_sliced_imgs_path)
    return


