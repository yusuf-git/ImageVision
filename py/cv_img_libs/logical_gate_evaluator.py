#/############################################################
# Author : Yusuf
# Created : 21-Jul-2021 10:20 PM
# updates on : 22-07-2021 02:00 AM, 24-Oct-2021 01:10 AM
###############################################################
import sys
import os

from numpy.lib.function_base import gradient
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
from cv_img_libs import img_comp_utils
from cv_img_libs import gen_utils
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.cons_results_data_model import cons_results_data_model
import cv2
import imutils
import imagehash
import jsonpickle
from data_models.net_analysis_report_data_model import net_analysis_report


# created on 23-Jan-2021 03:35 PM #
# updates on 25-Jan-2021 04:35 PM #
def check_eval_group_transitioned(algo_curr_idx, algo_cnt, prev_eval_groupID, dt):
    if(prev_eval_groupID == "" or algo_curr_idx == 0):
        return False
    curr_eval_groupID, _ = get_current_eval_groupID_and_match_operator(algo_curr_idx, algo_cnt, dt)
    print("in check_eval_group_transitioned::::",prev_eval_groupID,"-----", curr_eval_groupID)
    if prev_eval_groupID != curr_eval_groupID:
        return True
    else:
        return False


# created on 22-Jan-2021 02:15 AM #
# updates on 24-Jan-2021 07:30 PM, 25-Jan-2021 01:00 AM, 26-Jan-2021 01:35 AM #
def check_AND_operator_in_curr_eval_group(algo_curr_idx, algo_cnt, dt):
    and_operator_present = False
    prev_eval_groupID = ""
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)

    while (algo_curr_idx < algo_cnt):
        curr_eval_groupID, curr_match_operator = get_current_eval_groupID_and_match_operator(algo_curr_idx, algo_cnt, dt)
        if prev_eval_groupID != "" and prev_eval_groupID != curr_eval_groupID:
            return and_operator_present

        prev_eval_groupID = curr_eval_groupID
        algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_curr_idx]]
        if algo_runnable_state == "1" and str(curr_match_operator).lower() == "and":
            and_operator_present = True
            return and_operator_present
        algo_curr_idx = algo_curr_idx + 1
    return and_operator_present



# created on 23-Jan-2021 01:45 PM #
def get_next_eval_groupID_and_match_operator(algo_curr_idx, algo_cnt, dt):
    next_eval_groupID = ""
    next_algo = ""
    next_algo_match_operator = ""
    eval_groupID_dict = config_utils_lib.get_algo_eval_groupID(dt)
    match_operator_dict = config_utils_lib.get_algo_match_operator(dt)
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)
    while ((algo_curr_idx + 1) < algo_cnt):
        next_algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_curr_idx+1]]
        if next_algo_runnable_state == "1":
            next_eval_groupID = eval_groupID_dict[algo_name_list_runnables[algo_curr_idx+1]]
            next_algo = algo_name_list_runnables[algo_curr_idx+1]
            next_algo_match_operator = match_operator_dict[next_algo]
            break
        algo_curr_idx = algo_curr_idx + 1
    return next_eval_groupID, next_algo_match_operator



# created on 11-Feb-2021 09:35 PM to 11:35 PM
def remove_leading_special_chars(failed_algos_string):
    if str(failed_algos_string).startswith(" && "): ##and len(failed_algos_string.split(" && ")) > 1:
        failed_algos_string =  failed_algos_string.strip()[3:]
        print("remove_leading_special_chars :: && stripped:"+failed_algos_string)
    return failed_algos_string


# created on 11-Feb-2021 10:20 PM to 11:25 PM
def get_text_with_base_algo(base_algo, failed_algos_string):
    if str(failed_algos_string).startswith(base_algo) or str(failed_algos_string).__contains__(base_algo):
        print("get_text_with_base_algo",failed_algos_string)
        return failed_algos_string
    else:
        print("get_text_with_base_algo",base_algo + " && " + remove_leading_special_chars(failed_algos_string))
        return base_algo + " && " + remove_leading_special_chars(failed_algos_string)


# created on 23-Jan-2021 01:15 PM to 05:30 PM #
# updates on 25-Jan-2021 04:35 PM #
def get_current_eval_groupID_and_match_operator(algo_curr_idx, algo_cnt, dt):
    curr_eval_groupID = ""
    algo_match_operator = ""
    match_operator_dict = config_utils_lib.get_algo_match_operator(dt)
    eval_groupID_dict = config_utils_lib.get_algo_eval_groupID(dt)
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    #runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)
    #while algo_curr_idx < algo_cnt:
    if algo_curr_idx < algo_cnt:
        #curr_algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_curr_idx]]
        #if curr_algo_runnable_state == "1":
        curr_eval_groupID = eval_groupID_dict[algo_name_list_runnables[algo_curr_idx]]
        algo_match_operator = match_operator_dict[algo_name_list_runnables[algo_curr_idx]]
            #if(len(curr_eval_groupID) > 0):
                #break
        #algo_curr_idx = algo_curr_idx + 1
    gen_utils.console_verbose_out("************************************************",dt)
    gen_utils.console_verbose_out("get_current_eval_groupID_and_match_operator()::::",dt)
    gen_utils.console_verbose_out("algo_curr_idx:{}".format(algo_curr_idx),dt)
    gen_utils.console_verbose_out("algo_cnt:{}".format(algo_cnt),dt)
    gen_utils.console_verbose_out("algo:{}".format(algo_name_list_runnables[algo_curr_idx]),dt)
    gen_utils.console_verbose_out('curr_eval_groupID:{}'.format(curr_eval_groupID),dt)
    gen_utils.console_verbose_out('algo_match_operator:{}'.format(algo_match_operator),dt)
    gen_utils.console_verbose_out("************************************************",dt)
    return curr_eval_groupID, algo_match_operator


# created on 07-Feb-2021 01:40 AM #
def get_current_group_eval_operator(algo_curr_idx, algo_cnt, dt):
    current_group_eval_operator = ""
    group_eval_operator_dict = config_utils_lib.get_algo_group_eval_operator(dt)
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    #runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)
    #while algo_curr_idx < algo_cnt:
    if algo_curr_idx < algo_cnt:
        current_group_eval_operator = group_eval_operator_dict[algo_name_list_runnables[algo_curr_idx]]
    return current_group_eval_operator



# created on 07-Feb-2021 03:00 PM
# updates on 08-Feb-2021 02:30 AM, 11-Feb-2021 09:35 AM to 11:55 PM, 12-Feb-2021 12:30 AM, 03-Apr-2021 09:30 AM to 11:55 PM. 04-Apr-2021 12:50 AM, 16-Jul-2021 11:50 PM, 17-Jul-2021 03:00 AM, 18-Jul-2021 01:20 AM,19-Jul-2021 01:15 AM, 20-Jul-2021 01:15 AM
def eval_result_in_all_resultsets(results_collection_dict, base_image, base_result, base_rec_idx, algo_name_list, dt, match_operator, prev_algo_eval_groupID, prev_algo_match_operator, prev_algo_eval_group_operator ):
    n = 1 # look up the image in all resultsets other than th first one, as it's the base reference for the look up
    rec_idx = 0
    prev_eval_groupID = ""
    image_found = False
    curr_algo_result = False
    net_img_found_result = {}
    net_algo_eval_result = {}
    failed_algos_images = {}
    failed_algos_string = ""
    image = ""
    net_mandatory_result = False
    net_mandatory_result_no_update = False
    #algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_ind_group_result = base_result
    #if(prev_algo_match_operator == "or" or prev_algo_eval_group_operator == "or" ):
    #    algo_ind_group_result = False
    init_assignment_ind_group = None
    ind_group_result_dict = {}
    
    #algo_runnable_details_dict= config_utils_lib.get_algo_runnable_details(dt)
    #groupID_dict = config_utils_lib.get_algo_eval_groupID(dt)
    ##cross_group_eval_operator_dict = config_utils_lib.get_algo_group_eval_operator(dt)
    #shared_group_eval_operator_dict = config_utils_lib.get_algo_match_operator(dt)

    #prev_algo_groupID = groupID_dict[algo_runnable_details_dict[n-1]]
       
    while(len(results_collection_dict) > 0 and n < len(results_collection_dict)):
        #result_dict = results_collection_dict[n][algo_name_list[n]]
        result_dict = results_collection_dict[algo_name_list[n]]
        if(len(result_dict) <= 0):
            print("No result records found. Algo:"+algo_name_list[n])
        
        curr_algo_eval_groupID, match_operator = get_current_eval_groupID_and_match_operator(n, len(algo_name_list), dt)
        curr_group_eval_operator = get_current_group_eval_operator(n, len(algo_name_list), dt)
        print("Curr algo group ID, match_operator::",curr_algo_eval_groupID, match_operator)
        if(prev_algo_eval_groupID  == ""):
            prev_algo_eval_groupID = curr_algo_eval_groupID
        #_is_group_transitioned = check_eval_group_transitioned(n, len(algo_name_list), curr_eval_groupID, dt)
        if(prev_algo_eval_groupID != curr_algo_eval_groupID):
            _is_group_transitioned = True
            prev_algo_eval_groupID = curr_algo_eval_groupID
        else:
            _is_group_transitioned = False
        
        if(prev_algo_eval_group_operator != curr_group_eval_operator):
            pass # implement the logic in later verions based on new requirements
        
        #curr_algo_groupID, curr_algo_shared_group_eval_operator = get_current_eval_groupID_and_match_operator(n, len(algo_name_list), dt)
        #curr_algo_cross_group_eval_operator = get_current_group_eval_operator(n, len(algo_name_list), dt)

        rec_idx = 0
        image_found = False
        curr_algo_result = False
        add_base_algo = False
        while rec_idx < len(result_dict):   # iterate through the result collection until the desired image is located
            image = result_dict[rec_idx]["image"]
            if image == base_image: #and rec_idx == base_rec_idx:
                image_found = True
                curr_algo_result = bool(result_dict[rec_idx]["result"])
                #print("!!base result!!:",base_result)
                #print("!!curr_algo_result!!:",curr_algo_result)
                if(init_assignment_ind_group == None):  # only for initalizing the algo_ind_group_result field. If not, the default bool value will affect the overall net result
                    init_assignment_ind_group = "Done"   # change th default value so that this block won't be execuetd again
                    #algo_ind_group_result = curr_algo_result

                if base_result == False and curr_algo_result == False:
                    #failed_algos_images[image] = algo_name_list[0] + " && " + algo_name_list[n]
                    failed_algos_string = remove_leading_special_chars(failed_algos_string + " && "+ algo_name_list[n])
                    add_base_algo = True     # flag for concatenating the base algorithm in the return value : failed_algos_images
                elif base_result == False and curr_algo_result == True:
                    #failed_algos_images[image] = algo_name_list[0]
                    add_base_algo = True
                elif base_result == True and curr_algo_result == False:
                    failed_algos_string = remove_leading_special_chars(failed_algos_string + " && "+  algo_name_list[n])

                break # break the current loop as the intended image was located and the flags have been updated too
            rec_idx = rec_idx + 1

        net_img_found_result[base_image] = image_found # assign the image_found flag to the net result dictionary that will be returned
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("image:",image)
        if(not _is_group_transitioned):
            if(match_operator == "and"):
                algo_ind_group_result = bool(algo_ind_group_result and curr_algo_result)
                if(not net_mandatory_result and base_result and not curr_algo_result): # needed when the order is : ((SSI = true AND p-hash = false) OR BF = false). Coz, net_mandatory_result = true stmt alters the result
                    net_mandatory_result_no_update = True    
            elif(match_operator == "or"):
                algo_ind_group_result = bool(algo_ind_group_result or curr_algo_result)
            print("same group-match-operator-result:",algo_ind_group_result)
            #time.sleep(3)
        else:
            #init_assignment_ind_group = None # reset needed to run the if block above to re-initialize the algo_ind_group_result field
            #ind_gro'up_result_dict[prev_algo_groupID] = algo_ind_group_result # since the next groupID has already been reached, prev_algo_groupID being used
            if(prev_algo_eval_group_operator == "and"):
                algo_ind_group_result = bool(algo_ind_group_result and curr_algo_result)
            elif(prev_algo_eval_group_operator == "or"):
                algo_ind_group_result = bool(algo_ind_group_result or curr_algo_result)
                if(base_result and not net_mandatory_result_no_update):
                    net_mandatory_result = True
            print("diff group-match-operator-result:",algo_ind_group_result)
            #time.sleep(3)


        #if(not _is_group_transitioned):
        #    if(prev_algo_group_eval_operator == "and"):
        #        algo_ind_group_result = bool(algo_ind_group_result and curr_algo_result)
        #    elif(prev_algo_group_eval_operator == "or"):
        #        algo_ind_group_result = bool(algo_ind_group_result or curr_algo_result)
        #else:
        #    init_assignment_ind_group = None # reset needed to run the if block above to re-initialize the algo_ind_group_result field
        #    ind_group_result_dict[prev_algo_groupID] = algo_ind_group_result # since the next groupID has already been reached, prev_algo_groupID being used

        
        #logging.info(image+": Found ?:"+net_img_found_result+" net algo eval result:"+net_algo_eval_result)
        if add_base_algo == True:
            add_base_algo = False
            failed_algos_string = get_text_with_base_algo(algo_name_list[0], failed_algos_string)
        n = n + 1
    
    if(net_mandatory_result == True):
        algo_ind_group_result = net_mandatory_result
    net_mandatory_result = False
    net_mandatory_result_no_update = False
    net_algo_eval_result[base_image] = algo_ind_group_result
    failed_algos_images[base_image] = remove_leading_special_chars(failed_algos_string)
    #print("Check net result-------------::::::",net_img_found_result, net_algo_eval_result, failed_algos_images)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return net_img_found_result[base_image], net_algo_eval_result[base_image], failed_algos_images[base_image]
    #if(len(ind_group_result_dict) <= 0):
    #    return False, False, {} # return if the individual group result collection is empty

    #net_algo_eval_result_flag = ind_group_result_dict[list(ind_group_result_dict.keys())[0]] # initialize the flag with the first boolean value from the dictionary
    #runnable_group_eval_operator_dict = config_utils_lib.get_runnable_group_eval_operator_against_groupID(dt)
    #for i in ind_group_result_dict:  # iterate through each individual group result dictionary
    #    curr_group_operator = runnable_group_eval_operator_dict[i] # get the active group eval operator corresponding to the group ID i.e. i = group ID
    #    if(curr_group_eval_operator == "and"):
    #        net_algo_eval_result_flag = bool(net_algo_eval_result_flag and ind_group_result_dict[i]) # net eval result "and"ified with the indidividual group result
    #    if(curr_group_eval_operator == "or"):
    #        net_algo_eval_result_flag = bool(net_algo_eval_result_flag or ind_group_result_dict[i])  # net eval result "or"ified with the indidividual group result

    #net_algo_eval_result[base_image] = net_algo_eval_result_flag
    #failed_algos_images[base_image] = remove_leading_special_chars(failed_algos_string)
    #print("Check net result-------------::::::",net_img_found_result, net_algo_eval_result, failed_algos_images)
    #return net_img_found_result, net_algo_eval_result, failed_algos_images


# created on 07-Feb-2021 02:30 PM
# updates on 08-Feb-2021 02:10 AM, 12-Feb-2021 12:35 AM,  02:10 AM, 04-Apr-2021 01:50 AM, 16-Jul-2021 11:50 PM, 17-Jul-2021 03:00 AM, 18-Jul-2021 01:20 AM,19-Jul-2021 01:15 AM, 20-Jul-2021 01:15 AM
def read_result(results_collection_dict, match_operator, dt, eval_group_result_coll_start_idx):
    net_eval_result = {}
    rec_idx = 0
    net_img_found_result = {}
    aggregated_failed_algos_images = {}
    failed_algos_images = {}
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    if(len(results_collection_dict) <= 0):
        return False, False, aggregated_failed_algos_images

    n=0
        
    base_curr_eval_groupID, base_match_operator =  get_current_eval_groupID_and_match_operator(n, len(algo_name_list), dt)
    base_curr_group_eval_operator = get_current_group_eval_operator(n, len(algo_name_list), dt)
    print("base_curr_eval_groupID, base_match_operator, base_curr_group_eval_operator:::::",base_curr_eval_groupID, base_match_operator,base_curr_group_eval_operator)
    #_is_group_transitioned = check_eval_group_transitioned(n, len(algo_name_list), curr_eval_groupID, dt)
        
    #curr_algo_groupID, curr_algo_shared_group_eval_operator = get_current_eval_groupID_and_match_operator(n, len(algo_name_list), dt)
    #curr_algo_cross_group_eval_operator = get_current_group_eval_operator(n, len(algo_name_list), dt)

    rec_idx = 0
    curr_algo_result = False
    add_base_algo = False
    
    #not sure about the use case of the below line. Commented for now
    #net_img_found_result, net_eval_result, aggregated_failed_algos_images = eval_OR_operator_resultsets(results_collection_dict, eval_group_result_coll_start_idx, eval_group_result_coll_end_idx)

    #result_dict = results_collection_dict[eval_]group_result_coll_start_idx][algo_name_list[eval_group_result_coll_start_idx]]
    result_dict = results_collection_dict[algo_name_list[eval_group_result_coll_start_idx]]
    while rec_idx < len(result_dict):
        base_image = result_dict[rec_idx]["image"]
        # 07-Feb-2021 11:45 PM 
        # the below call to find_image_in_all_resultsets can be commented for now and uncommented and used later, because, the results sets are expected to be same in terms of image name and order
        # merged find_image_in_all_resultsets with eval_result_in_all_resultsets
        #img_found_result = bool(img_found_result and find_image_in_all_resultsets(results_collection_dict, image, rec_idx, algo_name_list))
        base_result = bool(result_dict[rec_idx]["result"])
        if(len(results_collection_dict) > 1):
            #net_img_found_result[base_image], net_eval_result[base_image], failed_algos_images = eval_result_in_all_resultsets(results_collection_dict, base_image, base_result,  rec_idx, algo_name_list, dt, match_operator, base_curr_eval_groupID, base_match_operator, base_curr_group_eval_operator)
            net_img_found_result[base_image], net_eval_result[base_image], failed_algos_images[base_image] = eval_result_in_all_resultsets(results_collection_dict, base_image, base_result,  rec_idx, algo_name_list, dt, match_operator, base_curr_eval_groupID, base_match_operator, base_curr_group_eval_operator)
            aggregated_failed_algos_images[base_image] = failed_algos_images[base_image]
            #print("net result::::::",net_img_found_result[image], " -- ", net_eval_result[image], " -- ", failed_algos_images)
            #print("aggregated_failed_algos_images[image]",aggregated_failed_algos_images[image])
        else:
            net_img_found_result[base_image] = True 
            net_eval_result[base_image] = base_result
            if base_result == False:
                aggregated_failed_algos_images[base_image] = algo_name_list[eval_group_result_coll_start_idx]

        #Delete recs when:
        #match_operator == or and group_operator == or
        #match_operator == AND and group_operator == or

        
        print("================================================================================================")
        print("image :"+base_image)
        print("Net Result - find image, algo eval result, failed_algos :"+str(net_img_found_result[base_image]), " -- ", str(net_eval_result[base_image]), " -- ", str(failed_algos_images[base_image]), " -- ", str(aggregated_failed_algos_images[base_image]))
        print("===============================================================================================")
        print("")
        rec_idx = rec_idx + 1
    return net_img_found_result, net_eval_result, aggregated_failed_algos_images



# created on 05-Feb-2021 11:35 PM #
# updates on 03-Apr-2021 09:30 AM #
def compare_results(results_collection_dict, match_operator, curr_group_eval_operator, dt, coll_start_idx = 0):
    n = 0
    operations_res = True
    failed_algos_images = {}
    if len(results_collection_dict) <= 0:
        print("Error: Zero count result collection")
        return False,False,failed_algos_images,"error"
         
    #result_dict1 = results_collection_dict[0][res_obj_json[0]["algo"]]
    #result_dict2 = results_collection_dict[1][res_obj_json[0]["algo"]]

    #if match_operator == "and":
    print("curr_group_eval_operator:",curr_group_eval_operator)
    net_img_found_result, net_eval_result, failed_algos_images = read_result(results_collection_dict, match_operator, dt, coll_start_idx)
    
    #if curr_group_eval_operator == "and":
    #    net_eval_result = bool(net_eval_result and )
    

    return net_img_found_result,net_eval_result,failed_algos_images





# created on 21-Jul-2021 05:15 PM, 22-Jul-2021 01:40 AM
def generate_net_analysis_report(results_for_eval_dict,match_operator, curr_group_eval_operator, dt):
    #if len(results_for_eval_dict) >= 2:
    net_img_found_result_dict,net_eval_result_dict,failed_algos_images_dict = compare_results(results_for_eval_dict, match_operator, curr_group_eval_operator, dt)
    #operation_net_result, failures_with_algos, passed_imgs_with_or_operator_algo =  analyze_net_result(dt,comp_result_data,operation_net_result)

    net_details = {}
    result_pattern_dict = {}
    img_idx = 0
    print("********************ImageVision v6 operation summary**********************")
    print("net result                              : ",net_eval_result_dict)
    print("failures with algos                     : ",failed_algos_images_dict) 
    print("image located                           : ",net_img_found_result_dict)
    print("**************************************************************************")
    #while(len(results_for_eval_dict) > 0 and result_dict_idx < len(results_for_eval_dict)):
        #result_dict = results_collection_dict[n][algo_name_list[n]]
    #result_dict = results_for_eval_dict[algo_name_list[result_dict_idx]]
    while(img_idx < len(net_eval_result_dict)):
        #image = net_eval_result_dict["image"]
        image= list(net_eval_result_dict.keys())[img_idx]
        net_details["image"] = image
        net_details["net_result"] = net_eval_result_dict[image]
        net_details["image_located"] = net_img_found_result_dict[image]
        net_details["failed_algos"] = failed_algos_images_dict[image]
        print("is it right::::::",image,net_eval_result_dict[image])
        net_analysis_report.net_analysis_details_list.append(net_analysis_report(image, net_eval_result_dict[image], net_img_found_result_dict[image], failed_algos_images_dict[image]))
        result_pattern_dict[image] = net_eval_result_dict[image]
        img_idx = img_idx + 1

    #k = len(net_analysis_report.net_analysis_details_list) - 1
    resJson = json.dumps([o.dump() for o in net_analysis_report.net_analysis_details_list])
    res_obj_json = json.loads(resJson) 
    return res_obj_json, result_pattern_dict
