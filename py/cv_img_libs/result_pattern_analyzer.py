#/##################################################################
# Authors : Aptha, Yusuf
# Created : 22-Jul-2021 10:30 AM
# Updated : 04-Aug-2021 11:55 PM, 05-Aug-2021, 23-Oct-2021 10:45 AM to 11:30 PM
####################################################################
import sys
import os

from numpy.core import numeric
sys.path.insert(0, os.path.realpath(os.path.pardir))
import logging
import time
import argparse
import json
import shutil
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
import numpy as np
from skimage.measure import compare_ssim
import pyautogui as pygui
from cv_img_libs import BRISK_FLANN_baseline_utils_lib
from cv_img_libs import config_utils_lib
from cv_img_libs import gen_utils
from cv_img_libs import img_comp_utils
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.cons_results_data_model import cons_results_data_model
import cv2
import imutils
import imagehash
import jsonpickle
from data_models.net_analysis_report_data_model import net_analysis_report


def analyze_result_pattern(result_pattern_dict:dict, dt):
    print()
    if str(dt["compare_args"]["realtime"]).lower() == "true":
        print("========================")
        print("Result Pattern Analyzer")
        print("========================")
    else:
        print("=====================")
        print("Net Comparison Result")
        print("=====================")
    print(result_pattern_dict)
    max_true = 0
    max_false = 0
    result = False
    last_max_true = 0
    last_max_false = 0
    total_pass = 0
    total_failed = 0
    result_dict = {}
    
    # score pattern
    score_pattern = int(str(dt["compare_args"]["result_pattern_analyzer"]["failure_pattern_succession_density"]))
    number_of_failures = 0
    result_set = gen_utils.sort(list(result_pattern_dict.items()))
    for key, value in result_set:
        if value == False:
            number_of_failures = number_of_failures + 1
            max_false = max_false + 1
            max_true = 0
            total_failed = total_failed + 1
            if last_max_false < max_false:
                last_max_false = max_false
            
        elif number_of_failures >= score_pattern:
            max_true = max_true + 1
            max_false = 0
            total_pass = total_pass + 1
            if last_max_true < max_true:
                last_max_true = max_true
            break
        else:
            number_of_failures  = 0
            max_true = max_true + 1
            max_false = 0
            total_pass = total_pass + 1
            if last_max_true < max_true:
                last_max_true = max_true
            print("true", number_of_failures)
    
    # printing result
    print("=================================")
    a = "number_of_failures:{}".format(number_of_failures)
    console_verbose_out("number_of_failures:{}".format(number_of_failures),dt)
    console_verbose_out("failure_pattern_succession_density:{}".format(score_pattern),dt)

    if number_of_failures <= score_pattern or number_of_failures == 0: #and number_of_failures != 0 :
        if(number_of_failures == 0):
            print("match operation : succeeded")
        else:
            console_verbose_out("number_of_failures <= failure_pattern_succession_density : {} <= {}".format(number_of_failures,score_pattern),dt)
        #print("net evaluation result : true")
        display_label(dt, total_pass, total_failed, last_max_true, last_max_false)
        result = True
    else:
        console_verbose_out("number_of_failures > failure_pattern_succession_density : {} > {}".format(number_of_failures,score_pattern),dt)
        print("match operation : not succeeded")
        display_label(dt, total_pass, total_failed, last_max_true, last_max_false)
        result = False
    #print("==========================================")
    result_dict["net_comp_result"] = result
    result_dict["max_consecutive_failures"] = str(last_max_false)
    result_dict["max_consecutive_pass_results"] = str(last_max_true)
    result_dict["total_pass_results"] = str(total_pass)
    result_dict["total_failures"] = str(total_failed)

    return result_dict


def display_label(dt, total_pass, total_failed,  last_max_true, last_max_false):
    print("=========================================")    
    if str(dt["compare_args"]["realtime"]).lower() != "true":
        return
    
    print('Max consecutive failures      :',last_max_false)
    print('Max consecutive pass results  :',last_max_true)
    print("Total pass results            :",total_pass)
    print("Total failures                :",total_failed)
    print("=========================================")    
    

def console_verbose_out(info, dt):
    if(str(dt["compare_args"]["intermediate_output"]) == "true"):
        print(info)