#/############################################################
# Author : Yusuf
# Created : 24-Jul-2021 10:30 AM
# Updates : 25-Jul-2021 10:30 AM to 11:50 PM, 26-Jul-2021 01:15 AM, 27-Jul-2021 02:00 AM, 28-Jul-2021 01:45 AM, 29-Jul-2021 02:15 AM, 30-Jul-2021 03:00 AM. 31-Jul-2021 01:30 AM, 01-Aug-2021 01:20 AM. 02-Aug-2021 02:30 AM, 02-Aug-2021 11:45 PM, 03-Aug-2021 11:55 PM, 04-Aug-2021 01:30 AM, 07-Aug-2021 11:55 PM
###############################################################

#from logging import log
import logging
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
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
from data_models.hang_issue_checker_data_model import hang_issue_checker_data_model
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.net_analysis_report_data_model import net_analysis_report



#Created on 07-Aug-2021 05:45 PM
def retriveConfigs(args):
    dt = img_comp_utils.readJson(args["json"], "compare_args")
    reports_path = str(dt["compare_args"]["hang_issue_reports_path"])
    
    net_result_path = str(dt["compare_args"]["net_result_path"])
    should_purge_oldlog = str(dt["compare_args"]["purge_old_reports"])
    if(not reports_path.endswith("/")):
        reports_path = reports_path + "/"
    if(not net_result_path.endswith("/")):
        net_result_path = net_result_path + "/"
    return dt, reports_path,net_result_path,should_purge_oldlog


def create_special_keys(dt):
    dt["compare_args"]["sliding_window_active"] = "false"
    #dt["compare_args"]["hang_issue_reports_path"] = ""
    #dt["compare_args"]["hang_issue_checker"] = ""
    #dt["compare_args"]["hang_issue_checker"]["check_frequency_min"] = ""
    return dt


def set_run_mode_to_historical(dt):
    if str(dt["compare_args"]["realtime"]).lower() == "true":
        dt["compare_args"]["realtime"] = "false"
    return dt



def write_net_result(result, dt):
    runtime_path = str(dt["compare_args"]["runtime_img_path"])
    result_path = str(dt["compare_args"]["net_result_path"])
    hang_issue_reports_path = str(dt["compare_args"]["hang_issue_reports_path"])
    fname = "hang_issue_result"
    resFile = os.path.join(result_path, str(fname)+ ".json")
    if(os.path.exists(resFile)):
        x = datetime.datetime.now()
        dt_part = "{0}{1}{2}_{3}{4}{5}".format(x.day,x.month,x.year,x.hour,x.minute,x.second)
        resFile = str(os.path.join(result_path, str(fname) + dt_part + ".json"))
    resultStr = {"result":result, "runtime_path":str(os.path.dirname(runtime_path)), "report_path":hang_issue_reports_path }
    resJson = json.dumps(resultStr, indent=4)
    with open(resFile,"w") as json_out:
        json_out.write(resJson)



# updates on 21-Nov-2020 04:15 PM #
def call_func(dt, algo_idx, tmp_match_data, special_state):
    algo_name_list = config_utils_lib.get_algo_name_list(dt)
    algo_mapper = config_utils_lib.get_algo_mapper()
    _,result_set = algo_mapper[algo_name_list[algo_idx]](dt,tmp_match_data,special_state)
    if(callable(result_set)):
        return algo_name_list, result_set
    else:
        return algo_name_list, result_set



def get_files(path):
    img_list = []
    if not os.path.exists(path):
        return img_list
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            img_list.append(os.path.join(dirname, filename))
    img_list = gen_utils.sort(img_list)
    return img_list



def compare(img_list, dt, original_reports_path):
    result = True
    res_obj_json = []
    res_obj_json_persist = []
    try:
        algo_name_list = config_utils_lib.get_algo_name_list(dt)
        algo_cnt  = 2
        algo_idx = 0
        res_obj_json = []
        while(algo_idx < algo_cnt):
            if(algo_name_list[algo_idx] != "SSI"): #and algo_name_list[algo_idx] != "perceptual_hashing"): # uncomment the preceding commented statement to activate p-hash
                algo_idx = algo_idx + 1
                continue
        
            res_obj_json, res_obj_json_persist, result = compare_images(img_list, algo_idx, dt)
            algo_idx = algo_idx + 1
        res_obj_json_persist = gen_utils.convert_serializable(res_obj_json_persist)
        hang_issue_checker_report = os.path.join(original_reports_path,"hang_issue_report.json")
        img_comp_utils.writeJson(hang_issue_checker_report,res_obj_json_persist,True)    
        return res_obj_json_persist, result
    except:
        return res_obj_json_persist, False




def compare_images(img_list, algo_idx,  dt):
        i = 0
        result = True
        tmp_match_data = []
        res_obj_json = []
        comp_result_data = []
        special_state = True
        print("img list",img_list)
        print("total images:",len(img_list))
        while i < len(img_list):
            dt["compare_args"]["baselineImage"] = img_list[i]
            dt["compare_args"]["runtime_img_path"] = img_list[i+1]
            hang_issue_checker_data_model.tmp_img_match_result_list = []
            algo_name_list, tmp_match_data = call_func(dt,algo_idx,res_obj_json, special_state)
            resJson = json.dumps([o.dump() for o in tmp_match_data])
            res_obj_json = json.loads(resJson) 
            if(res_obj_json[0]["result"] == False):
                result = False
            comp_result_data.extend(res_obj_json) #add the result set object to the end of the list
            hang_issue_checker_data_model.tmp_img_match_result_list.append(hang_issue_checker_data_model(str(os.path.basename(dt["compare_args"]["baselineImage"])), str(os.path.basename(dt["compare_args"]["runtime_img_path"])), res_obj_json[0]["img_path"], res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"],res_obj_json[0]["result"],res_obj_json[0]["msg"]))
            hang_issue_checker_data_model.hang_issue_checker_result_list.append(hang_issue_checker_data_model(str(os.path.basename(dt["compare_args"]["baselineImage"])), str(os.path.basename(dt["compare_args"]["runtime_img_path"])), res_obj_json[0]["img_path"], res_obj_json[0]["algo"],res_obj_json[0]["expscore"],res_obj_json[0]["original_score"],res_obj_json[0]["result"],res_obj_json[0]["msg"]))
            i = i + 1
            if( i == len(img_list)-1):
                break
        return hang_issue_checker_data_model.tmp_img_match_result_list, hang_issue_checker_data_model.hang_issue_checker_result_list, result

            

# Created at 07-Aug-2021 08:30 PM
def format_paths(dt):
    if not str(dt["compare_args"]["runtime_img_path"]).endswith("/"):
        dt["compare_args"]["runtime_img_path"] = dt["compare_args"]["runtime_img_path"] + "/"
    if not str(dt["compare_args"]["hang_issue_reports_path"]).endswith("/"):
        dt["compare_args"]["hang_issue_reports_path"] = dt["compare_args"]["hang_issue_reports_path"] + "/"
    if not str(dt["compare_args"]["net_result_path"]).endswith("/"):
        dt["compare_args"]["net_result_path"] = dt["compare_args"]["net_result_path"] + "/"
    return dt
    

    

def check_hang_issue(dt):
    hang_issue_issue_check_interval = int(dt["compare_args"]["hang_issue_checker"]["check_frequency_min"])
    next_img_counter = 0
    img_hop_idx = hang_issue_issue_check_interval * 60
    img_cnt = 0
    next_img_cnt_calculated = False
    baseline_img = ""
    runtime_img = ""
    img_list = []
    dt = format_paths(dt)
    dt = set_run_mode_to_historical(dt)
    original_reports_path = dt["compare_args"]["hang_issue_reports_path"] 
    dt["compare_args"]["hang_issue_reports_path"] = str(os.path.join(original_reports_path, "diffs"))
    all_runtime_imgs_list = get_files(str(os.path.dirname(dt["compare_args"]["runtime_img_path"])))
    if(len(all_runtime_imgs_list) <= 0):
        print("no such path or no image files found in the path:",str(os.path.dirname(dt["compare_args"]["runtime_img_path"])))
        return [],False
    all_runtime_imgs_list = gen_utils.sort(all_runtime_imgs_list)

    # Read from a speficifc path - all images - make sure good number of images
    # data_folder = Path("C:/Users/apthal/Desktop/imageReport")
    #fileDir = os.listdir("C:/SDVAutomation/src/test-inputs/imagevision/log-widget/realtime/py")
    #all_runtime_imgs_list = os.listdir(str(os.path.join(str(os.path.dirname(dt["compare_args"]["runtime_img"])), str(os.path.dirname(dt["compare_args"]["runtime_img"]))))
    #print("all_runtime_imgs_list:",str(os.path.dirname(dt["compare_args"]["runtime_img"])))
    #time.sleep(8)

    #sorted(fileDir)
    #fileDir.sort(key=lambda f:int(filter(str.isdigit,f)))
    #all_runtime_imgs_list.sort(key=lambda f:int(re.sub("\D","",f)))
    #sorted_files = sorted([os.path.basename(f) for f in all_runtime_imgs_list], key=lambda x: os.path.splitext(x)[0])
    #print(sorted_files)

    total_images= len(all_runtime_imgs_list)
    while img_cnt < total_images:
        if img_cnt == 0:
            baseline_img=all_runtime_imgs_list[img_cnt]
            img_list.append(baseline_img)
            next_img_counter = img_hop_idx
            runtime_img=all_runtime_imgs_list[next_img_counter]
            img_list.append(runtime_img)
        if next_img_counter == 0:
            pass
        elif not next_img_cnt_calculated:
            next_img_counter = next_img_counter + img_hop_idx
            next_img_cnt_calculated = True
        if img_cnt == next_img_counter or img_cnt == len(all_runtime_imgs_list)-1:
            if(img_cnt > len(all_runtime_imgs_list)):
                img_cnt = len(all_runtime_imgs_list) - 1
            runtime_img=all_runtime_imgs_list[img_cnt]
            img_list.append(runtime_img)
            next_img_cnt_calculated = False
        img_cnt=img_cnt+1

    result_set, result = compare(img_list,dt, original_reports_path)
    return result_set, result
   
    #compare(baseline and RT) then set baseline=RT

################################## PROGRAM ENTRY POINT ###########################
try:
    start_time = time.time()
    args = gen_utils.parse_args()
    dt, reports_path, net_result_path, should_purge_oldlog = retriveConfigs(args)
    dt = create_special_keys(dt)
    logfile = str(os.path.join(reports_path,'hang_issue_checker.log')).replace('\\','/')
    algo_artifacts_handler.handle_report_result_paths(reports_path, net_result_path, should_purge_oldlog)
    logging.basicConfig(filename=logfile, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    result_set, result = check_hang_issue(dt)
    print(result_set)
except:
    result = False
    message=str(sys.exc_info())
    logging.error(message)
finally:
    print("*******************************************************")
    print("imagevision v2 : Hang Issue Checker")
    if(result == True):
        write_net_result("true", dt)
        print("operation result:true")
    else:
        write_net_result("false", dt)
        print("operation result:false")
    print("*******************************************************")









'''###################DEVELOPED BUT UNUSED CODE - MAY BE USEFUL LATER##################

def compare(baseline_img, runtime_img, dt):
    runnable_algos_dict = config_utils_lib.get_algo_runnable_details(dt)
    algo_name_list_runnables = config_utils_lib.get_algo_name_list(dt)
    algo_cnt = len(config_utils_lib.get_algo_mapper())
    algo_idx = 0
    while(algo_idx < algo_cnt):
        algo_runnable_state = runnable_algos_dict[algo_name_list_runnables[algo_idx]]
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

'''