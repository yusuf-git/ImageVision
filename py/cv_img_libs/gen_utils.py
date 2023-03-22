#/############################################################
# Author : Yusuf
# Created : 05-Aug-2021 09:00 AM
# updates on : 07-Aug-2021 11:55 PM, 23-Oct-2021 11:45 PM
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
import re
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


# added on 21-Nov-2020 09:35 PM #
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json", required=True, help="json arg file name")
    args = vars(ap.parse_args())
    return args


def tryint(s):
    try:
        return int(s)
    except:
        return s


def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', str(s)) ]


def sort(l):
    l.sort(key=alphanum_key)
    return l

def convert_serializable(res_obj_json_persist):
    resJson = json.dumps([o.dump() for o in res_obj_json_persist])
    res_obj_json_persist = json.loads(resJson) 
    #print("convert:",res_obj_json_persist)
    return res_obj_json_persist

def console_verbose_out(info, dt):
    if(str(dt["compare_args"]["intermediate_output"]) == "true"):
        print(info)