#/############################################################
# Author : Yusuf
# Created : 01-Oct-2020 08:30 PM
# Updates : 02-Oct-2020 10:40 AM, 11-Oct-2020 02:30 PM to 11:50 PM, 12-Oct-2020 02:00 AM, 13-Oct-2020 04:00 AM, 14-Oct-2020 04:10 AM, 15-Oct-2020 03:20 AM, 16-Oct-2020 02:45 AM, 17-Oct-2020 03:10 AM, 18-Oct-2020 04:10 AM, 21-Nov-2020 02:20 AM, 09:45 PM, 25-Nov-2020 11:50 PM, 26-Nov-2020 12:45 AM, 27-Nov-2020 02:45 AM, 28-Nov-2020 11:55 PM, 29-Nov-2020 12:45 AM, 18-Jan-2021 11:50 PM, 19-Jan-2021 12:35 AM, 20-Jan-2021 11:50 PM, 21-Jan-2021 03:15 AM, 31-Jan-2021 03:30 AM, 06-Feb-2021 01:05 AM, 02-Apr-2021 08:30 AM to 11:50 PM, 03-Apr-2021 12:45 AM, 16-Jul-2021 11:50 PM, 17-Jul-2021 03:00 AM, 18-Jul-2021 01:20 AM,19-Jul-2021 01:15 AM, 20-Jul-2021 01:15 AM, 21-Jul-2021 01:25 AM, 22-Jul-2021 02:45 AM, 02-Aug-2021 02:30 AM, 07-Aug-2021 11:55 PM, 23-Oct-2021 11:30 PM, 24-Oct-2021 02:50 AM
###############################################################
# create a thumbnail of an image
import sys
import os

#from py.cv_img_libs.result_pattern_analyzer import console_verbose_out
#sys.path.insert(0, 'path/to/your/py_file')
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
from cv_img_libs import results_processor
from cv_img_libs import algo_artifacts_handler
from cv_img_libs import gen_utils
from cv_img_libs import special_config_keys
from algos_namelist import comp_algos
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.net_analysis_report_data_model import net_analysis_report
from  cv_img_libs import logical_gate_evaluator
from  cv_img_libs import result_pattern_analyzer
import cv2
import imutils
import imagehash
import jsonpickle
import img_comparator


# added on 28-Nov-2020 02:30 AM #
def del_prev_artifacts(workspace_path,should_purge_oldlog):
    try:
        prev_logpath = os.path.join(workspace_path,"image_ops/logs")
        prev_diffpath = os.path.join(workspace_path,"image_ops/diffs")
        if(should_purge_oldlog.lower() == "true" and os.path.exists(prev_logpath) is True):
            shutil.rmtree(prev_logpath)
        if(should_purge_oldlog.lower() == "true" and os.path.exists(prev_diffpath) is True):
            shutil.rmtree(prev_diffpath)
    except:
        print("error :: deleting prev. artifacts....Not OK")


# added on 28-Nov-2020 02:30 AM #
def createartifactspaths(dt):
    import datetime
    workspace_path = str(dt["compare_args"]["workspace_path"])
    should_purge_oldlog = str(dt["compare_args"]["purge_old_artifacts"])
    x = datetime.datetime.now()
    dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
    del_prev_artifacts(workspace_path, should_purge_oldlog)
    curr_logpath = os.path.join(workspace_path,"image_ops/logs",dt_part)
    curr_diffpath = os.path.join(workspace_path,"image_ops/diffs",dt_part)
    os.makedirs(curr_logpath)
    os.makedirs(curr_diffpath)
    return curr_logpath, curr_diffpath


def create_special_keys(dt):
    dt["compare_args"]["sliding_window_active"] = "false"
    dt["compare_args"]["hang_issue_reports_path"] = ""
    dt["compare_args"]["hang_issue_checker"] = {}
    dt["compare_args"]["hang_issue_checker"]["check_frequency_min"] = ""
    return dt



 # updates on 21-Nov-2020 04:15 PM #
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


# created on 18-Jan-2021 10:40 PM #
def keep_first_result_rec_img_paths(curr_algo_log, comp_result_data, _is_img_path_update_needed=True):
    n=0
    #comp_result_data.extend(tmp_match_data)
    while(len(comp_result_data) > 0 and n < len(comp_result_data) and _is_img_path_update_needed == True):
        if(n > 0):
            comp_result_data[n]["base_img_path"] = ""
            comp_result_data[n]["runtime_img_path"] = ""
        n = n + 1
    return comp_result_data



# created on 11:15 PM #
def get_img_file_cnt(filepath):
    cnt = 0
    for path, subdirs, files in os.walk(filepath):
        for name in files:
            cnt = cnt + 1
    return cnt

def format_paths(dt):
    if not str(dt["compare_args"]["img_ops_session_rootpath"]).endswith("/"):
        dt["compare_args"]["img_ops_session_rootpath"] = dt["compare_args"]["img_ops_session_rootpath"] + "/"
    if not str(dt["compare_args"]["comp_reports_path"]).endswith("/"):
        dt["compare_args"]["comp_reports_path"] = dt["compare_args"]["comp_reports_path"] + "/"
    if not str(dt["compare_args"]["net_result_path"]).endswith("/"):
        dt["compare_args"]["net_result_path"] = dt["compare_args"]["net_result_path"] + "/"
    return dt


# added on 21-Nov-2020 09:35 PM #
def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", "--json", required=True, help="json arg file name")
    args = vars(ap.parse_args())
    return args



#global imgfile_g
#global message
#global result
start_time = time.time()
args = parse_args()
dt = img_comp_utils.readJson(args["json"], "compare_args")
dt = create_special_keys(dt)
dt = format_paths(dt)
reports_path = str(dt["compare_args"]["comp_reports_path"])
net_result_path = str(dt["compare_args"]["net_result_path"])
should_purge_oldlog = str(dt["compare_args"]["purge_old_artifacts"])
algo_artifacts_handler.handle_report_result_paths(reports_path, net_result_path, should_purge_oldlog)
#reports_path  = algo_artifacts_handler.createartifactspaths(dt)
vision_tdk_logfile = str(os.path.join(reports_path,'ImageComp.log')).replace('\\','/')
logging.basicConfig(filename=vision_tdk_logfile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

_is_BF_active_algo = False
_should_generate_BF_baseline_file = False
algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)
runnable_state_labels = {}
runnable_state_labels["0"] = "off"
runnable_state_labels["1"] = "on"
dt["compare_args"]["missing_imgs"] = {}
preprocessing_needed = True
preprocessing_finished = False
#dt["compare_args"]["workspace_base"] = workspace_base
#dt["compare_args"]["workspace_runtime"] = workspace_runtime

operation_net_result = False
algo_name_list = []
comp_result_data = []
tmp_match_data = []
match_ops_details=[]
res_obj_json = []
result_file_list = []
algo_cnt = len(config_utils_lib.get_algo_mapper())
algo_idx = 0
b_tmp_path = ""
r_tmp_path = ""
algo_op_report = ""
match_operator_dict = config_utils_lib.get_algo_match_operator(dt)
eval_groupID_dict = config_utils_lib.get_algo_eval_groupID(dt)
prev_eval_groupID = ""
curr_eval_groupID = ""
curr_group_eval_operator = ""
next_algo_groupID = ""
next_algo_operator = ""
_is_curr_group_set_AND_operation = False
next_algo_runnable_state = ""
next_algo = ""

del_passed_result_records = False
results_for_eval_dict = {}
tmp_full_result_data_for_group_AND_eval = []

while(algo_idx < algo_cnt):

    print("******+******+******+******+*****")
    algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_idx]]
    print("algo                           : "+algo_name_list_runnables[algo_idx])
    print("runnable state                 : "+runnable_state_labels[algo_runnable_state])
    print("intra-group algo eval operator : "+match_operator_dict[algo_name_list_runnables[algo_idx]])
    print("algo groupID                   : "+eval_groupID_dict[algo_name_list_runnables[algo_idx]])
    #print("inter-group eval operator      :"+curr_group_eval_operator[algo_name_list_runnables[algo_idx]])
    print("******+******+******+******+*****")
    logging.info("algo           : "+algo_name_list_runnables[algo_idx])
    logging.info("runnable state : "+runnable_state_labels[algo_runnable_state])

    if(algo_runnable_state=="0"):
        algo_idx = algo_idx + 1
        continue
    
    _is_curr_group_set_AND_operation = logical_gate_evaluator.check_AND_operator_in_curr_eval_group(algo_idx, algo_cnt, dt)
    curr_eval_groupID, match_operator = logical_gate_evaluator.get_current_eval_groupID_and_match_operator(algo_idx, algo_cnt, dt)
    curr_group_eval_operator = logical_gate_evaluator.get_current_group_eval_operator(algo_idx, algo_cnt, dt)
    if prev_eval_groupID == "":# or prev_algo_groupID != curr_algo_groupID:
        prev_eval_groupID = curr_eval_groupID
    _is_group_transitioned = logical_gate_evaluator.check_eval_group_transitioned(algo_idx, algo_cnt, prev_eval_groupID, dt)
    

    BF_algo_prereq = BRISK_FLANN_baseline_utils_lib.check_BF_algo_ops_prereq(algo_idx, dt)
    if BF_algo_prereq == 0 or BF_algo_prereq == 1:
        _is_BF_active_algo = True
    else:
        _is_BF_active_algo = False
        BF_algo_prereq = 999
        BF_base_data_model.newimgs_baseline_buffer = []
        BF_basetobase_comp_data_model.basetobase_kp_update_list = []
    if BF_algo_prereq == 0 and _is_BF_active_algo == True:
        _should_generate_BF_baseline_file = True
    else:
        _should_generate_BF_baseline_file = False
    # end of parametric baseline check

    print("******+*********+*********")
    if(preprocessing_finished == True):
        preprocessing_needed = False
    
    print("preprocessing finished ?",preprocessing_finished)
    print("preprocessing needed   ?",preprocessing_needed)
    print("******+*********+*********")

    ############################# INVOKE THE LISTED ALGORITHMS AS PER INDEX #################################################
    algo_name_list, tmp_match_data = call_func(dt,algo_idx,res_obj_json )
    preprocessing_finished = True # PRE-PROCESSING NOT NEEDED AFTER INVOKING THE FIRST ALGO
    algo_op_report = os.path.join(reports_path, str(algo_name_list[algo_idx]).lower()+"_report.json")
    result_file_list.append(algo_op_report) # add the current result json to the result file list for building consolidated result file later
    
    match_ops_rec_cnt = len(tmp_match_data)
    #print( algo_name_list[algo_idx], " : image match operational records -->",match_ops_rec_cnt)
    #print("******+*********+*********")
    #print(comp_result_data.count())

    #json_file_data = img_comp_utils.readJson_plain("ssi_comp_result.json") #working fine, but without IO ops, the object creation is done below - 14-Oct-2020 03:15 AM
    #res_obj = json_file_data
    m = 0
    k = len(tmp_match_data) - 1
    resJson = json.dumps([o.dump() for o in tmp_match_data])
    res_obj_json = json.loads(resJson) 

    gen_utils.console_verbose_out("*********************************************************",dt)
    gen_utils.console_verbose_out("just before comp_result_data.extent():{}".format(res_obj_json),dt)
    comp_result_data.extend(res_obj_json) #add the result set object to the end of the list
    gen_utils.console_verbose_out("comp_result_data afte being extended:".format(comp_result_data),dt)
    gen_utils.console_verbose_out("*********************************************************",dt)

    if len(tmp_full_result_data_for_group_AND_eval) <= 0: # needed for group AND operation, as the original list undergoes changes with the removal of passed records - 07-Feb-2021 12:50 AM
        tmp_full_result_data_for_group_AND_eval = res_obj_json
    algo_artifacts_handler.WriteJsonlog(algo_op_report,res_obj_json) #write the result log to the json file

    #check the number of passed entries to delete them and retain the failed ones for the next algo operation
    while(len(tmp_match_data) >= 0 and m < match_ops_rec_cnt):
        #print("len(comp_result_data) ====",len(comp_result_data))
        #print("len(tmp_match_data) ====",len(tmp_match_data))
        match_ops_details = imageops(res_obj_json[k]["image"], res_obj_json[k]["base_img_path"], res_obj_json[k]["runtime_img_path"], res_obj_json[k]["algo"],res_obj_json[k]["expscore"],res_obj_json[k]["original_score"],res_obj_json[k]["result"],res_obj_json[k]["msg"])
        gen_utils.console_verbose_out("res_obj_json.result:{}".format(match_ops_details.result),dt)
        # check if the two vara are empty, then assign the base and runtime image paths to the vars for storing only one in the comparison output json file
        if(b_tmp_path=="" or r_tmp_path==""):
            b_tmp_path = match_ops_details.base_img_path
            r_tmp_path = match_ops_details.runtime_img_path
        #if(match_ops_details.result == True or str(match_ops_details.msg).lower().startswith("missing") is True):
        if((_is_curr_group_set_AND_operation == False) and match_operator == "or"  and (match_ops_details.result == True or str(match_ops_details.msg).lower().startswith("missing") is True)):
            #comp_result_data.pop(k)
            del res_obj_json[k]
        
        # the below statements may no longer be required, and hence commented. This is because the BF algo result details have undergone major changes from BenchImage
        #if(algo_name_list[algo_idx] == "BRISK-FLANN" and (str(match_ops_details.msg).lower().startswith("goodpoints") is True or str(match_ops_details.msg).lower().startswith("goodpoints_percent"))):
        #    del res_obj_json[k]
        k = k - 1
        m = m + 1


    BRISK_FLANN_baseline_utils_lib.add_new_BF_baseline_entry(_is_BF_active_algo, dt) # add new baseline images to the existing BF baseline json
    BRISK_FLANN_baseline_utils_lib.generate_BF_baseline_from_dataobject(_should_generate_BF_baseline_file,dt) # create BF baseline json from the data model for the first time

    ########create, read and process BF algo baseline json - create the baseline json for the first time from data object###############
    if(len(BF_basetobase_comp_data_model.basetobase_kp_update_list) > 0):
        BF_basetobase_resjson = json.dumps([o.dump() for o in BF_basetobase_comp_data_model.basetobase_kp_update_list])
        BF_basetobase_res_obj_json = json.loads(BF_basetobase_resjson) 
        tmp_b2b_comp_list = BF_basetobase_comp_data_model.basetobase_kp_update_list
        print("tmp_b2b_comp_list:",tmp_b2b_comp_list)
        #time.sleep()
        
        #for x in tmp_b2b_comp_list:
        for x in BF_basetobase_res_obj_json:
            img = x["image"]
            comp_res = x["comp_result"]
            latest_kp = x["basetobase_latest_kp"]
            print(img)
            print(comp_res)
            print(latest_kp)
            print("**********basetobase_comp_data*********")
    
    if(len(res_obj_json) > 0):
        gen_utils.console_verbose_out("input list for next algo compute :{}".format(res_obj_json),dt)
        gen_utils.console_verbose_out("**********",dt)
        # add the results to the results_for_eval_dict for comparison of results of various algorithms for net result
        #results_for_eval_dict[algo_idx][res_obj_json[0]["algo"]] = res_obj_json
        results_for_eval_dict[algo_name_list_runnables[algo_idx]] = res_obj_json
       
           
        algo_idx = algo_idx + 1
        res_obj_json[0]["base_img_path"] = b_tmp_path
        res_obj_json[0]["runtime_img_path"] = r_tmp_path
        #operation_net_result, failures_with_algos, passed_imgs_with_or_operator_algo =  analyze_net_result(dt,comp_result_data,operation_net_result)
        tmp_match_data = []
        imageops.image_match_outcome_list = []
    else:
        print("**********")
        print("match operation fully successful")
        operation_net_result = True
        print(res_obj_json)
        break



############################# result consolidation #########################
cons_result_file = os.path.join(reports_path, "consolidated_algo_result.json")
consolidated_result_list, consolidation_result = results_processor.consolidate_result(result_file_list, dt)
results_processor.write_consolidated_result(cons_result_file, consolidated_result_list, True)
############################### end of result consolidation ###################

res_obj_json, result_pattern_dict = logical_gate_evaluator.generate_net_analysis_report(results_for_eval_dict,match_operator,curr_group_eval_operator,dt)
result_pattern_analysis_dict = result_pattern_analyzer.analyze_result_pattern(result_pattern_dict, dt)
    
# write the logical gate analysis to a json file
logical_gate_report = os.path.join(reports_path,"logical_gate_analysis.json")
img_comp_utils.writeJson(logical_gate_report,res_obj_json,True)

# write the result pattern analysis to a json file
result_pattern_end_report = os.path.join(net_result_path,"result_pattern_analysis.json")
img_comp_utils.writeJson(result_pattern_end_report,result_pattern_analysis_dict,True) 


 # Logical Gate Evaluator -  DONE - 95 %
        
        # BF = false     OR     SSI = true  AND p-hash = false ==> False
        # BF = true      OR     SSI = true AND p-hash = false ==> true
        # BF = true      OR     SSI = false AND p-hash = false ==> false(True)
        # BF = false OR SSI = false AND p-hash = true ==> false
        # BF = false OR SSI = true AND p-hash = true ==> true
        # BF = false OR SSI = false AND p-hash = false ==> false
        # BF = true OR SSI = true AND p-hash = true ==> true
        # BF = true OR SSI = false AND p-hash = true ==> true
        # BF = true OR SSI = false AND p-hash = true ==> true


        # SSI = true AND p-hash = false      OR      BF = false ==> false
        
        
        
        # SSI = true AND p-hash = false      OR      BF = false ==> false
        # SSI = true AND p-hash = false      OR      BF = false ==> false
        # SSI = true AND p-hash = false      OR      BF = false ==> false



#------------------------------------------------------------------

# Result Pattern Analyzer - DONE - 90 %
    ## 1. different BF score for different builds
     # 2. Score largely vary - 100 to 500 - White patch check vs. non-white patch check 
    #  3. How to differentiate genuine issues from the false positives when the scores largey vary







     # Need more testing Areas :

     # Problem-1 :  White patch check vs. non-white patch check 
                      
                       # White-patch present scenarios:
                       #-------------------------------
                           # 1. Try to baseline solid BF score - white patch present - small
                           # 2. Try to baseline solid BF score - white patch present - medium
                           # 3. Try to baseline solid BF score - white patch present - large
                           # 4. Try to baseline solid SSI and P-Hash score - white patch present - small
                           # 5. Try to baseline solid SSI and P-Hash score - white patch present - medium
                           # 6. Try to baseline solid SSI and P-Hash score - white patch present - large

                      # White-patch not present scenarios:
                       #-----------------------------------
                           # 1. Try to baseline solid BF score - white patch not present
                           # 4. Try to baseline solid SSI and P-Hash score - white patch not present


    # assummptions :
    # 1. baseline1 : SSI : 0.75, p-hash - 6, BF - 250
    # 2. baseline1 : SSI : 0.70, p-hash - 5, BF - 150

    # 3. Even not a single algo group performing well, what next ?
               # take the score that repeats most number of times across builds for SSI, P-Hash, BF

    # what next ? :
          # test all the image sets aginst baseline1 image set
          # there will be 7 runs minimum ==> you will arrive at benchmarking score for all three algos

    # v3 : 
            # in v2, only Result Pattern Analyzer is available for white-patch checking
            # In v3 something more : whie patch - BF variance : exp = 350, act = 550 ==> potentially could be a white patch

    
        









     # 2.   (i) White patch check :
                  # - Baseline SSI and P-hash
    #       (ii) no white patch 

     # 3. False means - dig deeper and explore more, True means - finish the workflow ::: OPEM AREA


# Hung Issue Checker     -  DONE - 80 %


