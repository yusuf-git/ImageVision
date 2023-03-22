#/############################################################
# Author : Yusuf
# Date & Time : 19-Apr-2020 12:00 AM To 06:30 AM, 21-Apr-2020 03:10 AM, 01-May-2020 05:00 AM to 8:00 AM, 04-Sep-2021 09:00 PM, 05:Sep-2021 11:5 PM. 06-Sep-2021 03:15 AM, 08-Sep-2021 12:10 AM, 09-Sep-2021 01:00 AM, 10-Sep-2021 10:00 AM to 11:50 PM, 11-Sep-2021 01:30 AM, 10:30 AM to 02:00 PM, 11:50 PM, 12-Sep-2021 01:30 AM, 11:50 PM 13-Sep-2021 01:45 AM, 14-Sep-2021 03:00 AM, 15-Sep-2021 12:35 AM, 16-Sep-2021 02:30 AM, 04-Dec-2021 03:15 AM, 05-Dec-2021 02:45 AM, 10-Dec-2021 11:25 AM, 14-Dec-2021 05:55 AM, 15-Dec-2021 02:30 AM
###############################################################
# import the necessary pages
from tkinter import Scrollbar
from imutils.object_detection import non_max_suppression
import sys
import os
sys.path.insert(0, os.path.realpath(os.path.pardir))
import numpy as np
import argparse
import cv2

import imutils
import glob
import pyautogui
import time
import datetime
import json
from PIL import ImageGrab
from PIL import Image
import region_locator
import screen_actions
from cv_img_libs import gen_utils
from cv_img_libs import config_utils_lib
from cv_img_libs import BRISK_FLANN_baseline_utils_lib
from cv_img_libs import algo_artifacts_handler
from cv_img_libs import img_comp_utils
from data_models.sliced_image_checker_negative_cond import sliced_image_checker_negative_cond
from data_models.sliding_window_negative_cond_summary import sliding_window_negative_cond_summary
from data_models.sliced_image_checker_positive_cond import sliced_image_checker_positive_cond
from data_models.sliding_window_positive_cond_summary import sliding_window_positive_cond_summary
from data_models.imageops_data_model import imageops
from data_models.BF_baseline_data_model import BF_base_data_model
from data_models.BF_basetobase_comp_data_model import BF_basetobase_comp_data_model
from data_models.net_analysis_report_data_model import net_analysis_report




#Created on 08-Sep-2021 05:45 PM, 04-Dec-2021 02:10 AM
def retrieveConfigs(args):
    dt = img_comp_utils.readJson(args["json"], "actionize_args")
    reports_path = str(dt["actionize_args"]["reports_path"])
    if(not reports_path.endswith("/")):
        reports_path = reports_path + "/"

    net_result_path = str(dt["actionize_args"]["net_result_path"])
    if(not net_result_path.endswith("/")):
        net_result_path = net_result_path + "/"
    
    screen_snaps_path = str(os.path.join(reports_path,"screen_snaps/"))
    dt["actionize_args"]["screen_snaps_path"] = screen_snaps_path
    should_purge_oldlog = str(dt["actionize_args"]["purge_old_artifacts"])

    #if(not output_tmp_imgs_path.endswith("/")):
    #    output_tmp_imgs_path = output_tmp_imgs_path + "/"
    if(str(dt["actionize_args"]["action_inputs"]["matched_instance"])).lower() == "":
        dt["actionize_args"]["action_inputs"]["matched_instance"] = "first"
    return dt, reports_path, net_result_path, screen_snaps_path, should_purge_oldlog



def get_actions(dt):
    actions_list = []
    acts = str(dt["actionize_args"]["actions"])
    if(len(acts) <= 0):
        return actions_list
    actions_list = str(dt["actionize_args"]["actions"]).split("/")
    print(actions_list)
    #time.sleep(5)
    return actions_list


def map_data_to_actions(actions_list,dt):
    rel_xy = str(dt["actionize_args"]["action_inputs"]["rel_x_y"])
    for act in actions_list:
        if (str(act).lower() == "type" or str(act).lower() == "reltype"):
            dt["visual_actions"]["type_text"] = str(dt["actionize_args"]["action_inputs"]["type_text"])

        if(str(act).lower() == "scrollup"):
            dt["visual_actions"]["scroll_up_units"] = str(dt["actionize_args"]["action_inputs"]["scroll_up_units"])

        if(str(act).lower() == "scrolldown"):
            dt["visual_actions"]["scroll_down_units"] = str(dt["actionize_args"]["action_inputs"]["scroll_down_units"])

        #if(str(act).lower() == "clickat"):
        #    dt["visual_actions"]["clickAt"] = str(dt["actionize_args"]["action_inputs"]["clickat"])

        if(str(act).lower() == "wait"):
            dt["visual_actions"]["wait_seconds"] = str(dt["actionize_args"]["action_inputs"]["wait_seconds"])
        
        if(str(act).lower() == "mousedrag"):
            dt["visual_actions"]["mouse_drag_to_coords"] = str(dt["actionize_args"]["action_inputs"]["mouse_drag_to_coords"])

        if(len(rel_xy) > 0 and (str(act).lower() == "movemouserel" or str(act).lower() == "movemouserelwithdelay")):
            dt["visual_actions"]["rel_x"] = rel_xy.split(",")[0]
            dt["visual_actions"]["rel_y"] = rel_xy.split(",")[1]
            dt["visual_actions"]["delay"] = str(dt["actionize_args"]["action_inputs"]["mouse_move_delay"])
    return dt


def get_visual_actions_mapper():
    return {
    "type":screen_actions.type,
    "reltype":screen_actions.relType,
    "click":screen_actions.click,
    "relclick":screen_actions.relClick,
    "movemouserelwithdelay":screen_actions.moveMouseRelWithDelay,
    "movemouserel":screen_actions.moveMouseRel,
    "movemouse":screen_actions.moveMouse,
    "mouserightclick":screen_actions.mouseRightClick,
    "relmouserightclick":screen_actions.relMouseRightClick,
    "doubleclick":screen_actions.doubleClick,
    "reldoubleclick":screen_actions.relDoubleClick,
    "scrollup":screen_actions.scrollUp,
    "scrolldown":screen_actions.scrollDown,
    "get_root_coords":screen_actions.get_root_coords,
    "mouseup":screen_actions.mouseUp,
    "mousedown":screen_actions.mouseDown,
    "mousedrag":screen_actions.mouseDrag,
    "wait":screen_actions.wait,
    "isvisible":screen_actions.isVisible
    }


 # updates on 21-Nov-2020 04:15 PM #
def call_action(dt, action):
    tmp_res = []
    actions_mapper = get_visual_actions_mapper()
    #actions_list = get_actions(dt)
    func_result, msg = actions_mapper[str(action).lower()](dt)
    if(callable(func_result)):
        #tmp_res = func()
        return func_result, msg
    else:
        return func_result, msg


def writeResult(result, msg, dt, file_ext):
    imgfile = str(dt["actionize_args"]["template_img"])
    result_path = str(dt["actionize_args"]["net_result_path"])
    actions = str(dt["actionize_args"]["actions"])
    continue_on_failure = str(dt["actionize_args"]["continue_on_failure"])
    standard_res_file = os.path.join(result_path, "actionize_result.json")
    del_file(standard_res_file)

    resFile = get_output_artefact_name(imgfile, result_path, file_ext)
    resultStr = {"template_img":imgfile, "actions":actions, "continue_on_failure":continue_on_failure, "result":result, "message":msg }
    
    # write to a result file with the name of the template image
    write_to_json(resultStr, resFile)
    # write to the standard result file
    write_to_json(resultStr, standard_res_file)


def get_output_artefact_name(imgfile, artifact_path, file_ext):
    artifact_fixed_filename = os.path.join(artifact_path, str(os.path.basename(imgfile)).split('.')[0]+file_ext)
    artifact_file = artifact_fixed_filename
    dt_part = get_datetime_part()

    if(os.path.exists(artifact_file)):
        artifact_file = str(artifact_file).split(".")[0]
        artifact_file = os.path.join(str(artifact_file) + "_" + dt_part + file_ext)

    artFile = os.path.join(artifact_path, os.path.basename(artifact_file))
    if (os.path.isfile(artFile) or os.path.islink(artFile)):
        os.unlink(artFile)
        if(os.path.exists(artFile)):
            os.unlink(artFile)
    if(os.path.exists(artFile)):
        dt_part = get_datetime_part()
        artifact_file = os.path.join(artifact_path, str(os.path.basename(imgfile)).split('.')[0])
        artFile = os.path.join(artifact_file + "_" + dt_part + file_ext)

    return artFile


def get_datetime_part():
    x = datetime.datetime.now()
    dt_part = "{0}-{1}-{2}_{3}-{4}-{5}".format(x.day,x.month,str(x.year)[2:],x.hour,x.minute,x.second)
    return dt_part


def write_to_json(resultStr, resFile):
    resJson = json.dumps(resultStr, indent=4)
    with open(resFile,"w") as json_out:
        json_out.write(resJson)


def del_file(file):
    if(os.path.exists(file)):
        os.unlink(file)
    if(os.path.exists(file)):
        os.unlink(file)

def print_error(error_flag, found_match, message, dt):
    if(not error_flag and found_match):
        return False

    writeResult("false", message, dt, ".json")
    print("[INFO] completed the visual info search")
    print("************************")
    print("")
    print("==================================================================")
    print("[ImageVision v6 - Actionize] ==> operation completed (",( not error_flag and found_match),")")
    print("==================================================================")
    return True


def determine_template_match_algo_variant(dt):
    if(str(dt["actionize_args"]["search_methods"][0]["method1"]) == "multi_template_match"):
        dt["visual_actions"]["template_match_algo_variant"] = "multi_template_match"
        return dt
    
    if(str(dt["actionize_args"]["search_methods"][0]["method1"]) == "multi_template_match_multi_base"):
        dt["visual_actions"]["template_match_algo_variant"] = "multi_template_match_multi_base"
        return dt


# Created on 14-Dec-2021 08:30 AM
def format_paths(dt):
    RT_pos_path = str(dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"])
    RT_neg_path = str(dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"])
    RT_runtime_imgs_path = str(dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"])
    if not str(dt["actionize_args"]["imgArchivesPath"]).endswith("/") and len(str(dt["actionize_args"]["imgArchivesPath"])) > 0 :
        dt["actionize_args"]["imgArchivesPath"] = dt["actionize_args"]["imgArchivesPath"] + "/"
    if not str(dt["actionize_args"]["reports_path"]).endswith("/") and len(str(dt["actionize_args"]["reports_path"])) > 0 :
        dt["actionize_args"]["reports_path"] = dt["actionize_args"]["reports_path"] + "/"
    if not str(dt["actionize_args"]["net_result_path"]).endswith("/") and len(str(dt["actionize_args"]["net_result_path"])) > 0:
        dt["actionize_args"]["net_result_path"] = dt["actionize_args"]["net_result_path"] + "/"
    if not RT_pos_path.endswith("/") and len(RT_pos_path) > 0:
        dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"] = dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"] + "/"
    if not RT_neg_path.endswith("/") and len(RT_neg_path) > 0:
        dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"] = dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"] + "/"
    if not RT_runtime_imgs_path.endswith("/") and len(RT_runtime_imgs_path) > 0:
        dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"] = dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"] + "/"

    return dt


def generate_RT_result(res_obj_json_persist, original_report_path, report_file):
    res_obj_json_persist = gen_utils.convert_serializable(res_obj_json_persist)
    data_gap_detection_report = os.path.join(original_report_path, report_file)
    img_comp_utils.writeJson(data_gap_detection_report,res_obj_json_persist,True)
    return res_obj_json_persist

def print_session_end_msg(net_action_result):
    print("=================================================================")
    print("[ImageVision v6 - Actionize] ==> operation....completed (",(net_action_result),")")
    print("=================================================================")

def write_json(resultStr,resFile) :
    resJson = json.dumps(resultStr, indent=4)
    with open(resFile,"w") as json_out:
        json_out.write(resJson)

def trigger_RT_run(dt):
    is_RT_run = False
    json_result_set = None
    res_file = ""
    if(str(dt["actionize_args"]["realtime_mode"]).lower() != "true"):
        return is_RT_run, False
    
    is_RT_run = True
    format_paths(dt)
    rt_pos_path = dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"]
    rt_neg_path = dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"]
    rt_result_path = dt["actionize_args"]["RT_anomaly_detection"]["net_result_path"]
    runtime_imgs_path = dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"]

    if((len(rt_pos_path) <= 0 and len(rt_neg_path) <= 0) or len(runtime_imgs_path) <= 0):
        print("empty positive or negative or runtime_imgs path for RT...")
        print('exiting...')
        sys.exit(1)
    RT_net_result, json_result_set_neg, json_result_set_pos = region_locator.RT_multi_template_match_multi_base(dt)
    if(len(json_result_set_neg) > 0):
        json_result_set = json_result_set_neg
        res_file = "RT_data_gap_neg_result.json"
    elif(len(json_result_set_pos) > 0):
        json_result_set = json_result_set_pos
        res_file = "RT_data_gap_pos_result.json"
    net_res_json={"net_result":RT_net_result}
    generate_RT_result(json_result_set, rt_result_path, res_file )
    write_json(net_res_json, rt_result_path+"\\RT_data_gap_net_result.json" )

    return is_RT_run, RT_net_result


############################### Actionizer - driver program #######################################
print("===============ImageVision - Actionize=================")
preprocessing_needed = True
preprocessing_finished = False
coords = ()
centerCoord = ()
message = ""
start_time = time.time()                    
args = gen_utils.parse_args()
dt, reports_path, net_result_path, screen_snaps_path, should_purge_oldartifacts = retrieveConfigs(args)
algo_artifacts_handler.handle_report_result_paths(reports_path, net_result_path, should_purge_oldartifacts, screen_snaps_path)
dt["visual_actions"] = {}
dt["visual_actions"]["curr_scr_snap"] = get_output_artefact_name(str(dt["actionize_args"]["template_img"]), screen_snaps_path, ".png")
continue_on_failure = str(dt["actionize_args"]["continue_on_failure"])
matched_instance_selection = str(dt["actionize_args"]["action_inputs"]["matched_instance"])
error_flag = False
found_match = False
should_exit = False


#================================RT run==========================================
is_this_RT_run, RT_net_result = trigger_RT_run(dt)
if(is_this_RT_run):
    print_session_end_msg(RT_net_result)
    sys.exit(1)
#================================end of RT run block===================================================


#=====================================Actionize Run===================================
try:
    if(not os.path.exists(str(dt["actionize_args"]["template_img"]))):
        error_flag = True
        message = "template img file is not found"
        print(message)
        print_error(error_flag, found_match, message, dt)
        should_exit = True
        sys.exit(1)
        
    dt = determine_template_match_algo_variant(dt)
    
    if(str(dt["visual_actions"]["template_match_algo_variant"]) == "multi_template_match"):
        coords, orig_img = region_locator.multi_template_match(dt)
    elif (str(dt["visual_actions"]["template_match_algo_variant"]) == "multi_template_match_multi_base"):
        coords, orig_img = region_locator.multi_template_match_multi_base(dt)


    #coords, orig_img = region_locator.multi_template_match(dt)
    #coords, orig_img = region_locator.multi_template_match_multi_base(dt)
    #coords, orig_img = region_locator.multi_template_match_multi_base_multi_scale(dt)

    if(len(coords) <= 0):
        found_match = False
        message = "no match found for the template img on the current screen"
    else:
        found_match = True
except:
    error_flag = True
    message=str(sys.exc_info())
    print("[ERROR] - visual info search operation:")
    print(message)


if(should_exit):
    sys.exit(1)

if(error_flag or not found_match):
    message = "no match found for the template img or error while performing the match"
    print("[FAILURE] no match found for the template img or error while performing the match")
    
should_exit = print_error(error_flag, found_match, message, dt)
if(should_exit):
    print('exiting Actionize....')
    sys.exit(1)

curr_scr_file =  os.path.join( screen_snaps_path,"curr_screen.png")
img = cv2.imread(curr_scr_file)

if(str(dt["actionize_args"]["intermediate_output"])).lower() == "true":
    cv2.imshow("Final NMS",img)
    time.sleep(1)

instance = 0 # neural network(AI/ML) : postive images , negative - writing articles, presentations - consistency, taking up challenges, showcasing talent : softskills & communication & presentation
for coord in coords:
    if(instance == 0 and matched_instance_selection == "first"):
        centerCoord = (coord[0]+coord[2])/2, (coord[1]+coord[3])/2
        dt["visual_actions"]["x1"] = coord[0]
        dt["visual_actions"]["y1"] = coord[1]
        break

    if(instance == len(coords)-1 and matched_instance_selection == "last"):
        centerCoord = (coord[0]+coord[2])/2, (coord[1]+coord[3])/2
        dt["visual_actions"]["x1"] = coord[0]
        dt["visual_actions"]["y1"] = coord[1]
        break
    instance += 1

#print('dt["visual_actions"]["x1"]:',dt["visual_actions"]["x1"])
#print('dt["visual_actions"]["y1"]:',dt["visual_actions"]["y1"])

print("[INFO] centeroid:",centerCoord)
dt["visual_actions"]["x"] = int(float(centerCoord[0]))
dt["visual_actions"]["y"] = int(float(centerCoord[1]))
dt["visual_actions"]["orig_x"] = int(float(centerCoord[0]))
dt["visual_actions"]["orig_y"] = int(float(centerCoord[1]))
print("[INFO] completed the visual info search")
print("************************")

try:
    print("parsing action list...")
    actions_list = get_actions(dt)
    dt = map_data_to_actions(actions_list, dt)
    action_result = True
    net_action_result = True

    for action in actions_list:
         action_result, message = call_action(dt,action)
         if(not bool(action_result)):
             print("[FAILURE] - Action " + action +" failed")
             message = "[FAILURE] - Action " + action +" failed"
             if(str(continue_on_failure).lower() != "true"):
                 net_action_result = False
                 print("[FAILURE] - continue_on_failure : false. Terminating the operation...")
                 break
             else:
                 net_action_result = False
                 print("[INFO] - continue_on_failure : true. Continuing with the operation...")
                 continue
except:
    action_result = False
    net_action_result = False
    message=str(sys.exc_info())
    print("[ERROR] - visual actions:")
    print(message)

finally:
    print("[ImageVision - Actionize] [INFO] ==> net result :",net_action_result)
    if(net_action_result):
        writeResult("true", message, dt, ".json")
    else:
        writeResult("false", message, dt, ".json")

    print("=================================================================")
    print("[ImageVision v6 - Actionize] ==> operation....completed (",(net_action_result),")")
    print("=================================================================")























#-----------------UNUSED CODE - FOR LATER REFERENCE---------------------------

'''
for coord in coords:
    #centerCoord = (int((coord[0]+coord[2])/2), int((coord[1]+coord[3])/2))
    print("coord:",coord)
    centerCoord = (coord[0]+coord[2])/2, (coord[1]+coord[3])/2
    print(centerCoord)
    time.sleep(0.5)
    #print("Centroid:",centerCoord[0]," ",centerCoord[1])
    screen_actions.moveMouse(centerCoord[0],centerCoord[1])
    time.sleep(0.5)
    screen_actions.moveMouse(coord[0],coord[1])
    time.sleep(0.5)
'''
'''
#try:
if(error_flag or not found_match):
   #coords, _ = region_locator.multi_scale_template_match()
    coords, _ = region_locator.multi_scale_multi_template_match()
    coords, _ = region_locator.sliding_window_match(dt)

img_file =  "D:\Explore\AI\CV\Exercises\sdv\pyimagesearch\images\curr_screen.png"
img = cv2.imread(img_file)
#cv2.imshow("Final NMS",img)
#time.sleep(1)
'''

