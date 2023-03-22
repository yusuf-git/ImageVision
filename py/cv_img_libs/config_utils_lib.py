#/############################################################
# Author : Yusuf
# Added on : 21-Nov-2020 08:30 PM
# Updates : 07-feb-2021 01:30 AM, 04-Apr-2021 02:00 AM
###############################################################
# create a thumbnail of an image
import sys
import os
#sys.path.insert(0, 'path/to/your/py_file')
sys.path.insert(0, os.path.realpath(os.path.pardir))
from PIL import Image, ImageEnhance
from skimage.metrics import structural_similarity as ssim
#import matplotlib.pyplot as plt
import numpy as np
import cv2
import imutils
import imagehash
from skimage.measure import compare_ssim
import argparse
import pyautogui as pygui
from cv_img_libs import img_comp_utils
from cv_img_matcher.algos_namelist import comp_algos
import jsonpickle
#from di_container import di_container
from cv_img_matcher import img_comparator
from data_models.imageops_data_model import imageops
import json


# updates on 21-Nov-2020 03:35 PM 
def get_algo_configs(dt):
    #print("get_alg_expected_score - algo name:",algo)
    algos = dt["compare_args"]["similarity"]
    #print("get_alg_expected_score --- alogs:",algos)
    exp_score = ""
    ret_dict = {}
 
    for i in algos:
        exp_score = str(list(i.values())[1])
        if(exp_score!=""):
            ret_dict[str(list(i.values())[0])] = str(list(i.values())[1])
    if(exp_score==""):
        print("default algo selected : SSI")
        for i in algos:
            if(str(list(i.values())[0])==comp_algos.ssi):
                exp_score = str(list(i.values())[1])
    return ret_dict


# added on 21-Nov-2020 03:45 PM #
def get_algo_runnable_details(dt):
    algos = dt["compare_args"]["similarity"]
    runnable_algos_dict = {}
    for i in algos:
        runnable_algos_dict[str(list(i.values())[0])] = str(list(i.values())[3])
    return runnable_algos_dict


def get_algo_mapper():
    return {
    "SSI":img_comparator.SSI_compare,
    "perceptual_hashing":img_comparator.perceptual_hash_match,
    "BRISK-FLANN":img_comparator.BRISK_FLANN_match,
    "diff_hashing":img_comparator.diff_hash_match
    }


# updates on 21-Nov-2020 03:45 PM #
def get_algo_name_list(dt):
    algo_configs = get_algo_configs(dt)
    algo_name_list = []
    for key in algo_configs.keys():
        algo_name_list.append(key)
    return algo_name_list


def get_algo_match_operator(dt):
    algos = dt["compare_args"]["similarity"]
    ret_dict = {}
    for i in algos:
        operator = str(list(i.values())[2])
        if operator == "":
            operator = "and"
        ret_dict[str(list(i.values())[0])] = str(list(i.values())[2])
    return ret_dict

def get_algo_eval_groupID(dt):
    algos = dt["compare_args"]["similarity"]
    ret_dict = {}
    for i in algos:
        groupID = str(list(i.values())[4])
        ret_dict[str(list(i.values())[0])] = str(list(i.values())[4])
    return ret_dict


def get_algo_group_eval_operator(dt):
    algos = dt["compare_args"]["similarity"]
    ret_dict = {}
    for i in algos:
        group_operator = str(list(i.values())[5])
        ret_dict[str(list(i.values())[0])] = str(list(i.values())[5])
    return ret_dict


def get_runnable_group_eval_operator_against_groupID(dt):
    algos = dt["compare_args"]["similarity"]
    ret_groupID_dict = {}
    for i in algos:
        runnable_state = str(list(i.values())[3])
        if(runnable_state == "1"):
            ret_groupID_dict[str(list(i.values())[4])] = str(list(i.values())[5])
    return ret_groupID_dict
