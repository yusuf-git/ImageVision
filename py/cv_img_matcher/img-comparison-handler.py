#/############################################################
# Author : Yusuf
# Created : 01-Oct-2020 08:30 PM
# Updates : 02-Oct-2020 10:40 AM, 11-Oct-2020 02:30 PM to 11:50 PM, 12-Oct-2020 02:00 AM, 13-Oct-2020 04:00 AM, 14-Oct-2020 04:10 AM, 15-Oct-2020 03:20 AM, 16-Oct-2020 02:45 AM, 17-Oct-2020 03:10 AM, 18-Oct-2020 04:10 AM, 21-Nov-2020 02:20 AM, 09:45 PM, 25-Nov-2020 11:50 PM, 26-Nov-2020 12:45 AM, 27-Nov-2020 02:45 AM, 28-Nov-2020 11:55 PM, 29-Nov-2020 12:45 AM
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
from cv_img_libs import results_processor
from cv_img_libs import algo_artifacts_handler
from algos_namelist import comp_algos
from data_models.imageops_data_model import imageops
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
import cv2
import imutils
import imagehash
import jsonpickle
#from di_container import di_container
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


 # updates on 21-Nov-2020 04:15 PM #
def call_func(dt, algo_idx, tmp_match_data):
    tmp_res = []
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_mapper = config_utils_lib.get_algo_mapper()
    print("algo active index | algo :",algo_idx, "|", algo_name_list[algo_idx])
    #print("**********")
    ##print("********************tmp_match_data****************")
    ##print(tmp_match_data)
    #print("**********")
    #print("********************Length of tmp_match_data****************")
    #print(len(tmp_match_data))
    #print("**********")
    if(len(tmp_match_data) > 0):
        #print("********************tmp_match_data - tmp_paths ****************")
        #print(":::",tmp_match_data[0]["base_img_path"])
        #print(":::",tmp_match_data[0]["runtime_img_path"])
        #print("**********")
        pass
    func = algo_mapper[algo_name_list[algo_idx]](dt,tmp_match_data)
    if(callable(func)):
        #tmp_res = func()
        return algo_name_list, func
    else:
        return algo_name_list, func

def find_passed_imgs_with_or_operator(n, curr_algo, operator, comp_result_data):
    passed_algos_imgs_with_or_operator = {}
    passed_imgs_with_or_operator = []
    if(comp_result_data[n]["result"] == True and operator.lower() == "or"):
        passed_imgs_with_or_operator.append(comp_result_data[n]["image"])
        passed_algos_imgs_with_or_operator[curr_algo] = passed_imgs_with_or_operator
    return passed_algos_imgs_with_or_operator


 # created on 17-Oct-2020 05:30 PM #
 # updates on 18-Oct-2020 12:25 AM, 03:15 AM #
def analyze_net_result(dt, comp_result_data, op_net_result):
    #if(op_net_result == True):
    #    return True, "", passed_imgs_with_or_operator_algo
    curr_algo=""
    match_operator = config_utils_lib.get_algo_match_operator(dt)
    operations_res = True
    comp_res_obj  = iter(comp_result_data)
    n = 0
    passed_imgs_with_or_operator_algo = {}
    #passed_imgs_with_or_operator = []
    tmp_failures_with_algos = ""
    failures_with_algos = ""
    while(len(comp_result_data) > 0 and n < len(comp_result_data)):
        operator = match_operator[comp_result_data[n]["algo"]]
        curr_algo = comp_result_data[n]["algo"]
        #curr_algo = next(comp_res_obj)
        while(comp_result_data[n]["algo"] == curr_algo and n < len(comp_result_data)):
            if(comp_result_data[n]["result"] == False and operator.lower() == "and"):
                operations_res = False
                tmp_failures_with_algos = curr_algo
            passed_imgs_with_or_operator_algo =  find_passed_imgs_with_or_operator(n, curr_algo, operator, comp_result_data)
            n = n + 1
            if(n >= len(comp_result_data)):
                break
        # concatenate algos with comma until before the last algo
        if(n < len(comp_result_data)):
            failures_with_algos = failures_with_algos + tmp_failures_with_algos + ", "
        elif(n > len(comp_result_data)):
            failures_with_algos = failures_with_algos + tmp_failures_with_algos  # concatenate algo without comma for the last algo
        tmp_failures_with_algos = ""
    # in case the algos that have failed ends with comma, remove it
    if(failures_with_algos.strip().endswith(",") == True):
        failures_with_algos = failures_with_algos.strip()[:-1]
    
    if(op_net_result == False):
        return operations_res, failures_with_algos, passed_imgs_with_or_operator_algo
    else:
        return True, failures_with_algos, passed_imgs_with_or_operator_algo # in case the net result is already True(i.e.Pass), return the passed images list with "OR" operator algo with net result being True

        
def WriteJsonlog(curr_algo_log, comp_result_data, _is_img_path_update_needed=True):
    n=0
    #comp_result_data.extend(tmp_match_data)
    while(len(comp_result_data) > 0 and n < len(comp_result_data) and _is_img_path_update_needed == True):
        if(n > 0):
            comp_result_data[n]["base_img_path"] = ""
            comp_result_data[n]["runtime_img_path"] = ""
        n = n + 1
    if(os.path.exists(curr_algo_log)):
        os.unlink(curr_algo_log)    
    img_comp_utils.writeJson(curr_algo_log,comp_result_data,True)
    #img_comp_utils.writeJson("match_op_log.json",comp_result_data, True)        

# created on 11:15 PM #
def get_img_file_cnt(filepath):
    cnt = 0
    for path, subdirs, files in os.walk(filepath):
        for name in files:
            cnt = cnt + 1
    return cnt

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
reports_path  = algo_artifacts_handler.createartifactspaths(dt)
vision_tdk_logfile = str(os.path.join(reports_path,'vision_tdk.log')).replace('\\','/')
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

operation_net_result = False
algo_name_list = []
comp_result_data = []
tmp_match_data = []
match_ops_details=[]
res_obj_json = []
result_file_list = []
algo_cnt = len(config_utils_lib.get_algo_mapper())
#print("algo_cnt",algo_cnt)
#print("First print:",dt)
algo_idx = 0
b_tmp_path = ""
r_tmp_path = ""
algo_op_report = ""
#while(algo_idx < len(algo_mapper)):
while(algo_idx < algo_cnt):

    print("******+******+******+******+*****")
    algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_idx]]
    print("algo           : "+algo_name_list_runnables[algo_idx])
    print("runnable state :",runnable_state_labels[algo_runnable_state])
    print("******+******+******+******+*****")
    logging.info("algo           : "+algo_name_list_runnables[algo_idx])
    logging.info("runnable state :"+runnable_state_labels[algo_runnable_state])
    if(algo_runnable_state=="0"):
        algo_idx = algo_idx + 1
        continue

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
    algo_name_list, tmp_match_data = call_func(dt,algo_idx,res_obj_json)
    algo_op_report = os.path.join(reports_path, str(algo_name_list[algo_idx]).lower()+"_report.json")
    result_file_list.append(algo_op_report) # add the current result json to the result file list for building consolidated result file later
    
    match_ops_rec_cnt = len(tmp_match_data)
    print( algo_name_list[algo_idx], " : image match operational records -->",match_ops_rec_cnt)
    print("******+*********+*********")
    #print(comp_result_data.count())

    #json_file_data = img_comp_utils.readJson_plain("ssi_comp_result.json") #working fine, but without IO ops, the object creation is done below - 14-Oct-2020 03:15 AM
    #res_obj = json_file_data
    m = 0
    k = len(tmp_match_data) - 1
    resJson = json.dumps([o.dump() for o in tmp_match_data])
    res_obj_json = json.loads(resJson) 
    comp_result_data.extend(res_obj_json)
    #check the number of passed entries to delete them and retain the failed ones for the next algo operation
    while(len(tmp_match_data) >= 0 and m < match_ops_rec_cnt):
        print("len(comp_result_data) ====",len(comp_result_data))
        print("len(tmp_match_data) ====",len(tmp_match_data))
        match_ops_details = imageops(res_obj_json[k]["image"], res_obj_json[k]["base_img_path"], res_obj_json[k]["runtime_img_path"], res_obj_json[k]["algo"],res_obj_json[k]["expscore"],res_obj_json[k]["original_score"],res_obj_json[k]["result"],res_obj_json[k]["msg"])
        print("res_obj_json.result:",match_ops_details.result)
        # check if the two vara are empty, then assign the base and runtime image paths to the vars for storing only one in the comparison output json file
        if(b_tmp_path=="" or r_tmp_path==""):
            b_tmp_path = match_ops_details.base_img_path
            r_tmp_path = match_ops_details.runtime_img_path
        if(match_ops_details.result == True or str(match_ops_details.msg).lower().startswith("missing") is True):
            #comp_result_data.pop(k)
            del res_obj_json[k]
        
        # the below statements may no longer be required, and hence commented. This is because the BF algo result details have undergone major changes from BenchImage
        #if(algo_name_list[algo_idx] == "BRISK-FLANN" and (str(match_ops_details.msg).lower().startswith("goodpoints") is True or str(match_ops_details.msg).lower().startswith("goodpoints_percent"))):
        #    del res_obj_json[k]
        k = k - 1
        m = m + 1

    BRISK_FLANN_baseline_utils_lib.add_new_BF_baseline_entry(_is_BF_active_algo, dt)
    BRISK_FLANN_baseline_utils_lib.generate_BF_baseline_from_dataobject(_should_generate_BF_baseline_file,dt)

    ########create, read and process BF algo baseline json - create the baseline json for the first time from data object###############
    if(len(BF_basetobase_comp_data_model.basetobase_kp_update_list) > 0):
        tmp_b2b_comp_list = BF_basetobase_comp_data_model.basetobase_kp_update_list
        for x in tmp_b2b_comp_list:
            img = x["image"]
            comp_res = x["comp_result"]
            latest_kp = x["basetobase_latest_kp"]
            print("**********basetobase_comp_data*********")
            print(img)
            print(comp_res)
            print(latest_kp)
    
    if(len(res_obj_json) > 0):
        print("input list for next algo compute :",res_obj_json)
        print("**********")
        algo_idx = algo_idx + 1
        res_obj_json[0]["base_img_path"] = b_tmp_path
        res_obj_json[0]["runtime_img_path"] = r_tmp_path
        tmp_match_data = []
        imageops.image_match_outcome_list = []
    else:
        print("**********")
        print("match operation fully successful")
        operation_net_result = True
        print(res_obj_json)
        break

WriteJsonlog(algo_op_report,comp_result_data)

############################# result consolidation #########################
cons_result_file = os.path.join(reports_path, "consolidated_result.json")
consolidated_result_list, consolidation_result = results_processor.consolidate_result(result_file_list)
results_processor.write_consolidated_result(cons_result_file, consolidated_result_list, True)
############################### end of result consolidation ###################


operation_net_result, failures_with_algos, passed_imgs_with_or_operator_algo =  analyze_net_result(dt,comp_result_data,operation_net_result)


print("*************************************************************************")
print("                    match op summary -->         ")
print("net result                              : ",operation_net_result)
print("failures with algos                     : ",failures_with_algos)
print("passed matches with 'OR' operator algo  : ",passed_imgs_with_or_operator_algo)
print("**************************************************************************")
            




#ob = imageops(res_obj[0]["image"],res_obj[0]["algo"],res_obj[0]["expscore"],res_obj[0]["original_score"],res_obj[0]["result"],res_obj[0]["msg"])




#a = [{"image":"1.png","score":1.0,"outcome":False},{"image":"2.png","score":0.96,"outcome":True}]




'''

while(k < res_length):
        ob = imageops(res_obj[k]["image"], res_obj[k]["base_img_path"], res_obj[k]["runtime_img_path"], res_obj[k]["algo"],res_obj[k]["expscore"],res_obj[k]["original_score"],res_obj[k]["result"],res_obj[k]["msg"])
        #print(ob)
        #print("##############################")
        #if(ob.result is False and str(ob.msg).lower().startswith("missing") is False):
        print("ob.result = ",ob.result)
        if(ob.result == True):
            print("##############################")
            print("deleting item:",ob)
            comp_result_data.pop(k)
            print("##############################")
        k = k + 1


for r in comp_result_data:
    print([r])
    print("#######JSON string#######################")
    json_rec = jsonpickle.encode(r)
    print(json_rec)
    print("#######END - JSON string#######################")
    

print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#res_obj = jsonpickle.decode(json_file_data)
'''