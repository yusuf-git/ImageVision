#/############################################################
# Author : Yusuf
# Date & Time : 08-Sep-2021 09:45 AM
# Updates on  : 09-Sep-2021 01:00 AM, 10-Sep-2021 10:00 AM to 11:50 PM, 11-Sep-2021 01:30 AM, 10:30 AM to 02:00 PM, 11:50 PM, 12-Sep-2021 01:30 AM, 11:50 PM 13-Sep-2021 01:45 AM,  14-Sep-2021 03:00 AM, 15-Sep-2021 12:35 AM, 16-Sep-2021 02:30 AM, 16-Nov-2021 2:30 AM, 17-Nov-2021 01:30 AM. 18-Nov-2021 09:30 PM,22-Nov-2021 02:30 AM, 23-Nov-2021 03:00 AM, 24-Nov-2021 02:30 AM, 25-Nov-2021 02:30 AM , 26-Nov-2021 02:00 AM, 27-Nov-2021 10:00 AM to 11:50 PM, 28-Nov-2021 02:00 AM, 05:30 PM to 11:55 PM, 29-Nov-2021 01:30 AM, 08:45 AM to 11:15 AM, 11:50 PM, 30-Nov-2021 01:25 AM, 01-Dec-2021 08:00 PM to 11:15 PM, 02-Dec-2021 03:15 AM, 
###############################################################
# import the necessary pages
#from _typeshed import OpenBinaryModeUpdating
from platform import uname
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import cv2
import sys
import imutils
import glob
import pyautogui
import time
import os
from PIL import ImageGrab
from PIL import Image
from pyscreeze import center
import region_locator
import win32api
from win32con import *


def get_uiobj_coords(dt):
    x = str(dt["visual_actions"]["x"])
    y = str(dt["visual_actions"]["y"])
    x = int(float(x))
    y = int(float(y))
    print("template_img_coords:",x,y)
    return x,y


def get_dragTo_coords(dt):
    x=""
    y=""
    if(len(str(dt["visual_actions"]["mouse_drag_to_coords"])) <= 0):
        print("a")
        return "",""

    coords_list = str(dt["visual_actions"]["mouse_drag_to_coords"]).split(",")
    if(len(coords_list) < 2):
        print("b")
        return "",""
    if(coords_list[0] == "" and coords_list[1] != ""):
        print("Empty x")
        x,_ = get_uiobj_coords(dt)
        y = coords_list[1]
    if(coords_list[1] == "" and coords_list[0] != ""):
        print("Empty y")
        _,y = get_uiobj_coords(dt)
        x = coords_list[0]
    if(coords_list[0] != "" and coords_list[1] != ""):
        x = coords_list[0]
        y = coords_list[1]

    #x = str(dt["visual_actions"]["mouse_drag_to_coords"]).split(",")[0]
    #y = str(dt["visual_actions"]["mouse_drag_to_coords"]).split(",")[1]
    #x = int(float(x))
    #y = int(float(y))
    #fprint("template_img_coords:",x,y)
    #time.sleep(10)
    return x,y


def check_coords_integrity(x,y,dt=None):
    if(x is None) or (y is None):
        return False
    return True


def moveMouseRelWithDelay(dt):
    print("******************************")
    print("[action]:[moveMouseRelWithDelay]")  
    try:
        x_step_target = str(dt["visual_actions"]["rel_x"])
        y_step_target = str(dt["visual_actions"]["rel_y"])
        delay = str(dt["visual_actions"]["delay"])
        print("x_step_target:",x_step_target)
        print("y_step_target:",y_step_target)
        #time.sleep(7)
        #x_step_target = int(float(x_step_target))
        #y_step_target = int(float(y_step_target))
        #print("x_step_target:",x_step_target)
        #print("y_step_target:",y_step_target)
        if len(str(delay)) <= 0:
            delay = "0.5"
        delay = float(delay)
        x_coord = 0
        y_coord = 0
        x_coord_neg = 0
        y_coord_neg = 0
        neg_coord_x = False
        neg_coord_y = False
        (curr_x, curr_y) = pyautogui.position()
        tmp_x = 0
        tmp_y = 0
        x_unspecified_coord = False
        y_unspecified_coord = False
        if(x_step_target == "" and y_step_target == ""):
            return False
        if(x_step_target == ""):
            #x_step_target = str(dt["visual_actions"]["x1"])
            #tmp_x = str(dt["visual_actions"]["x1"])
            x_step_target = "0"
            #tmp_x = "0"
            x_unspecified_coord = True
        if(y_step_target == ""):
            #y_step_target = str(dt["visual_actions"]["y1"])
            #tmp_y = str(dt["visual_actions"]["y1"])
            y_step_target = "0"
            #tmp_y = "0"
            y_unspecified_coord = True

        x_step_target = int(float(x_step_target))
        y_step_target = int(float(y_step_target))
        print("rel. x :",x_step_target)
        print("rel. y :",y_step_target)

        while(True):
            if(x_coord < int(x_step_target) and not x_unspecified_coord):
                x_coord += 1
                tmp_x = x_coord
            elif(x_coord_neg > int(x_step_target) and not x_unspecified_coord):
                x_coord_neg += -1
                tmp_x = x_coord_neg
                neg_coord_x = True
            if(y_coord < int(y_step_target) and not y_unspecified_coord):
                y_coord += 1
                tmp_y = y_coord
            elif(y_coord_neg > int(y_step_target) and not y_unspecified_coord):
                y_coord_neg += -1
                tmp_y = y_coord_neg
                neg_coord_y = True
            
            
            if((x_coord >= x_step_target or x_unspecified_coord) and (y_coord >= y_step_target or y_unspecified_coord) and not neg_coord_x and not neg_coord_y):
                break
            elif((x_coord_neg <= x_step_target or x_unspecified_coord) and (y_coord_neg <= y_step_target or y_unspecified_coord ) and neg_coord_x and neg_coord_y):
                break
            elif((x_coord_neg <= x_step_target or x_unspecified_coord) and (y_coord >= y_step_target or y_unspecified_coord) and neg_coord_x and not neg_coord_y):
                break
            elif((x_coord >= x_step_target or x_unspecified_coord) and (y_coord_neg <= y_step_target or y_unspecified_coord) and not neg_coord_x and  neg_coord_y):
                break
            pyautogui.moveRel(tmp_x,tmp_y)
            time.sleep(int(delay))
            tmp_x = 0
            tmp_y = 0
            #if(x_unspecified_coord):
                #tmp_x = str(dt["visual_actions"]["x1"])
            #    tmp_x = "0"
            #if(y_unspecified_coord):
                #tmp_y = str(dt["visual_actions"]["y1"])
            #    tmp_y = "0"
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "MouseMoveRelWithDelay failed"



def moveMouseRel(dt):
    print("******************************")
    print("[action]:[moveMouseRel]")  
    try:
        x_step_target = str(dt["visual_actions"]["rel_x"])
        y_step_target = str(dt["visual_actions"]["rel_y"])
        x_coord = 0
        y_coord = 0
        x_coord_neg = 0
        y_coord_neg = 0
        neg_coord_x = False
        neg_coord_y = False
        (curr_x, curr_y) = pyautogui.position()
        tmp_x = 0
        tmp_y = 0
        x_unspecified_coord = False
        y_unspecified_coord = False
        if(x_step_target == "" and y_step_target == ""):
            return False
        if(x_step_target == ""):
            #x_step_target = str(dt["visual_actions"]["x1"])
            #tmp_x = str(dt["visual_actions"]["x1"])
            x_step_target = "0"
            #tmp_x = "0"
            x_unspecified_coord = True
        if(y_step_target == ""):
            #y_step_target = str(dt["visual_actions"]["y1"])
            #tmp_y = str(dt["visual_actions"]["y1"])
            y_step_target = "0"
            #tmp_y = "0"
            y_unspecified_coord = True

        x_step_target = int(float(x_step_target))
        y_step_target = int(float(y_step_target))
        print("rel. x :",x_step_target)
        print("rel. y :",y_step_target)

        while(True):
            if(x_coord < int(x_step_target) and not x_unspecified_coord):
                x_coord += 1
                tmp_x = x_coord
            elif(x_coord_neg > int(x_step_target) and not x_unspecified_coord):
                x_coord_neg += -1
                tmp_x = x_coord_neg
                neg_coord_x = True
            if(y_coord < int(y_step_target) and not y_unspecified_coord):
                y_coord += 1
                tmp_y = y_coord
            elif(y_coord_neg > int(y_step_target) and not y_unspecified_coord):
                y_coord_neg += -1
                tmp_y = y_coord_neg
                neg_coord_y = True
            
            
            if((x_coord >= x_step_target or x_unspecified_coord) and (y_coord >= y_step_target or y_unspecified_coord) and not neg_coord_x and not neg_coord_y):
                break
            elif((x_coord_neg <= x_step_target or x_unspecified_coord) and (y_coord_neg <= y_step_target or y_unspecified_coord ) and neg_coord_x and neg_coord_y):
                break
            elif((x_coord_neg <= x_step_target or x_unspecified_coord) and (y_coord >= y_step_target or y_unspecified_coord) and neg_coord_x and not neg_coord_y):
                break
            elif((x_coord >= x_step_target or x_unspecified_coord) and (y_coord_neg <= y_step_target or y_unspecified_coord) and not neg_coord_x and  neg_coord_y):
                break
            
            pyautogui.moveRel(tmp_x,tmp_y)
            tmp_x = 0
            tmp_y = 0
            #if(x_unspecified_coord):
                #tmp_x = str(dt["visual_actions"]["x1"])
            #    tmp_x = "0"
            #if(y_unspecified_coord):
                #tmp_y = str(dt["visual_actions"]["y1"])
            #    tmp_y = "0"
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "MouseMoveRel failed"


def moveMouse(dt):
    print("******************************")
    print("[action]:[moveMouse]")  
    x,y = get_uiobj_coords(dt)
    if(not check_coords_integrity(x,y)):
        return False
    try:
        pyautogui.moveTo(x,y)
        tmp_x = str(x)
        tmp_y = str(y)
        dt["visual_actions"]["x"] = int(float(tmp_x))
        dt["visual_actions"]["y"] = int(float(tmp_y))
        dt["visual_actions"]["prev_moveMouseRel"] = "false"
        print("******************************")
        return True, ""
    except:
        print(" exception-movemouse:"+str(sys.exc_info()))
        dt["visual_actions"]["prev_moveMouseRel"] = "false"
        print("******************************")
        return False, "moveMouse failed"
        

def mouseUp(dt):
    #x,y = get_uiobj_coords(dt)
    #if(not check_coords_integrity(x,y)):
    #    return False
    print("******************************")
    print("[action]:[mouseUp]")  
    try:
        pyautogui.mouseUp()
        print("******************************")
        return True, ""
    except:
        print(" exception-movemouse:"+str(sys.exc_info()))
        print("******************************")
        return False, "mouseUp failed"


def mouseDown(dt):
    print("******************************")
    print("[action]:[mouseDown]")  

    #if(not check_coords_integrity(x,y)):
    #    return False
    try:
        pyautogui.mouseDown(button="left")
        #pyautogui.mouseDown()
        #pyautogui.mouseDown()
        #pyautogui.mouseDown()
        #pyautogui.mouseDown()
        #tmp_x = str(x)
        #tmp_y = str(y)
        #dt["visual_actions"]["x"] = int(float(tmp_x))
        #dt["visual_actions"]["y"] = int(float(tmp_y))
        #dt["visual_actions"]["prev_moveMouseRel"] = "false"
        print("******************************")
        return True, ""
    except:
        print("exception-movemouse:"+str(sys.exc_info()))
        print("******************************")
        #dt["visual_actions"]["prev_moveMouseRel"] = "false"
        return False, "mouseDown failed"
    

def mouseDrag(dt):
    print("******************************")
    print("[action]:[mouseDrag](drag n drop)")  

    try:

        orig_template_img = dt["actionize_args"]["template_img"]

        if(str(dt["actionize_args"]["action_inputs"]["drop_target_img"]) == ""  and 
            str(dt["actionize_args"]["action_inputs"]["mouse_drag_to_coords"]) == ""):
            print("Empty drop_target_img and mouse_drag_to_coords")
            return False

        if(str(dt["actionize_args"]["action_inputs"]["drop_target_img"]) != "" ):
            print("drag N drop activated method : template image for the drop location ...")
            dt["actionize_args"]["template_img"] = str(dt["actionize_args"]["action_inputs"]["drop_target_img"])
            drop_img_coords, drop_img = region_locator.multi_template_match(dt)
            dt["visual_actions"]["drop_img_coords"] = drop_img_coords
            print("drop_img_coords:",drop_img_coords)
            dt["actionize_args"]["template_img"] = orig_template_img
            if(len(drop_img_coords)) <= 0:
                return False
            centerCoords = get_center_coord(drop_img_coords, dt)
            x = centerCoords[0]
            y = centerCoords[1]


        if(str(dt["actionize_args"]["action_inputs"]["mouse_drag_to_coords"]) != "" 
           and str(dt["actionize_args"]["action_inputs"]["drop_target_img"]) == "" ):
            print("drag N drop activated method : drag to the specified coordinates ...")
            x,y = get_dragTo_coords(dt)
            print("mouse_drag_to_coords:",x,y)
         
        pyautogui.moveTo(int(x),int(y),1)
        print("******************************")
        return True, ""
    except:
        print("exception-movemouse:"+str(sys.exc_info()))
        print("******************************")
        return False, "mouseDrag failed"


def click(dt):
    print("******************************")
    print("[action]:[click]")    
    result = False
    x,y = get_uiobj_coords(dt)
    try:
        if(check_coords_integrity(x,y,dt)):
            #pyautogui.moveTo(x,y)
            pyautogui.click(x,y)
            print("clicked at:",x,y)
            result = True
        print("******************************")
        return result, ""
    except:
        print("******************************")
        return False, "click failed"


def relClick(dt):
    print("******************************")
    print("[action]:[relClick]")    
    x,y = get_uiobj_coords(dt)
    try:
        pyautogui.click()
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "relClick failed"



def mouseRightClick(dt):
    print("******************************")
    print("[action]:[mouseRightClick]")    
    result = False
    x,y = get_uiobj_coords(dt)
    try:
        if(check_coords_integrity(x,y)):
            pyautogui.rightClick(x,y)
            result = True
        print("******************************")
        return result, ""
    except:
        print("******************************")
        return False, "mouseRightClick failed"


def relMouseRightClick(dt):
    print("******************************")
    print("[action]:[relMouseRightClick]")    
    #x,y = get_uiobj_coords(dt)
    try:
        pyautogui.rightClick()
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "relMouseRightClick failed"


def doubleClick(dt):
    print("******************************")
    print("[action]:[doubleClick]")
    result = False
    x,y = get_uiobj_coords(dt)
    try:
        if(check_coords_integrity(x,y)):
            pyautogui.doubleClick(x,y)
            result = True
        print("******************************")
        return result, ""
    except:
        print("******************************")
        return False, "doubleClick failed"


def relDoubleClick(dt):
    print("******************************")
    print("[action]:[relDoubleClick]")
    x,y = get_uiobj_coords(dt)
    try:
        pyautogui.doubleClick()
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "relDoubleClick failed"


def scrollUp(dt):
    print("******************************")
    print("[action]:[scrollUp]")
    x,y = get_uiobj_coords(dt)
    scroll_up_units = int(str(dt["visual_actions"]["scroll_up_units"]))
    if(scroll_up_units is None or scroll_up_units == 0 ):
        return True
    idx = 1
    
    try:
        while idx <= scroll_up_units:
            #win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, 100000, 0)
            win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, scroll_up_units, 0)
            idx += 1
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "scrollUp failed"



def scrollDown(dt):
    print("******************************")
    print("[action]:[scrollDown]")
    x,y = get_uiobj_coords(dt)
    scroll_down_units = int(str(dt["visual_actions"]["scroll_down_units"]))
    usigned_scroll_down_units = 0
    if(str(scroll_down_units).startswith("-")):
        usigned_scroll_down_units = int(str(scroll_down_units).lstrip("-"))
    if(scroll_down_units is None or scroll_down_units == 0):
        return True
    idx = 1
    #scroll_down_units = scroll_down_units +(1 << 32)
    try:
        #pyautogui.moveTo(x,y)
        while idx <= usigned_scroll_down_units:
            #win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, -100000, 0)
            win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, scroll_down_units, 0)
            idx += 1
            #Scroll one to the right
            #win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, 1, 0)
            #Scroll one to the left
            #win32api.mouse_event(MOUSEEVENTF_HWHEEL, x, y, -1, 0)
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "scrollDown failed"


def type(dt):
    print("******************************")
    text = str(dt["visual_actions"]["type_text"])
    print("[action]:[type]")
    result = False
    x,y = get_uiobj_coords(dt)
    try:
        if(check_coords_integrity(x,y)):
            pyautogui.click(x,y)
            pyautogui.keyDown('ctrl')
            pyautogui.press('a')
            pyautogui.keyUp('ctrl')
            pyautogui.press('del')
            pyautogui.typewrite(text)
            result = True
        print("******************************")
        return result, ""
    except:
        print("******************************")
        return False, "type failed"


def relType(dt):
    print("******************************")
    text = str(dt["visual_actions"]["type_text"])
    print("[action]:[relType]")
    try:
        
        #pyautogui.write("Hello world.....")
        pyautogui.click()
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.press('del')
        pyautogui.typewrite(text)
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "relType failed"



def get_root_coords(dt):
    try:
        print("******************************")
        dt["visual_actions"]["x"] = int(float(dt["visual_actions"]["orig_x"]))
        dt["visual_actions"]["y"] = int(float(dt["visual_actions"]["orig_y"]))
        print("[action]:[get_root_coords]")
        print("original root coordinates...",dt["visual_actions"]["x"],",",dt["visual_actions"]["y"])
        pyautogui.moveTo(dt["visual_actions"]["x"], dt["visual_actions"]["y"])
        print("[sub-action]:[moveMouse]")
        print("******************************")
        return True, "get_root_coords:"+dt["visual_actions"]["x"]+","+ dt["visual_actions"]["y"]
    except:
        print("******************************")
        return False, "FAILURE : get_root_coords failed"



def wait(dt):
    try:
        print("******************************")
        print("[action]:[wait]")
        if(str(dt["visual_actions"]["wait_seconds"]) == "") :
            dt["visual_actions"]["wait_seconds"] = "0"
        print("waiting...",dt["visual_actions"]["wait_seconds"]," second(s)")
        time.sleep(int(str(dt["visual_actions"]["wait_seconds"])))
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "wait failed"


def isVisible(dt):
    try:
        print("******************************")
        print("[action]:[isVisible]")
        if(str(dt["visual_actions"]["template_match_algo_variant"]) == "multi_template_match"):
            coords, drop_img = region_locator.multi_template_match(dt)
        elif (str(dt["visual_actions"]["template_match_algo_variant"]) == "multi_template_match_multi_base"):
            coords, drop_img = region_locator.multi_template_match_multi_base(dt)

        if(len(coords) <= 0):
            print("visual info is not found...")
            print("******************************")
            return False, "isVisible failed"
        #print("[INFO] visual info coords:",coords)
        print("******************************")
        return True, ""
    except:
        print("******************************")
        return False, "isVisible failed"




def get_center_coord(coords,dt):
    instance = 0
    matched_instance_selection = str(dt["actionize_args"]["action_inputs"]["matched_instance"])
    centerCoord = []
    for coord in coords:
        if(instance == 0 and matched_instance_selection == "first"):
            centerCoord = (coord[0]+coord[2])/2, (coord[1]+coord[3])/2
            break

        if(instance == len(coords)-1 and matched_instance_selection == "last"):
            centerCoord = (coord[0]+coord[2])/2, (coord[1]+coord[3])/2
            break
        instance += 1

    print("drop - centeroid:",centerCoord)
    return centerCoord
    



####################UNUSED - MAY BE USEFUL LATER 26-Nov-2021 11:45 PM #########################################

def scrollUp_alt(dt):
    x,y = get_uiobj_coords(dt)
    scroll_up_units = int(str(dt["visual_actions"]["scroll_up_units"]))
    if(scroll_up_units is None or scroll_up_units == "" ):
        return True

    try:
        idx = 1
        pyautogui.moveTo(x,y)
        while idx <= scroll_up_units:
           #pyautogui.mouseDown()
           #pyautogui.dragTo(x, y+1)
           #pyautogui.click(x, y)
           #idx += 1
        #pyautogui.mouseDown(x,y)
        #pyautogui.dragTo(x, y-50)
        #pyautogui.mouseDown(x,y)
        #pyautogui.dragTo(x, y-50)
           pyautogui.scroll(scroll_up_units)
           idx += 1
        return True
    except:
        return False



def scrollDown_alt(dt):
    x,y = get_uiobj_coords(dt)
    scroll_down_units = int(str(dt["visual_actions"]["scroll_down_units"]))
    if(scroll_down_units is None or scroll_down_units == ""):
        return True

    try:
        idx = 1
        pyautogui.moveTo(x,y)
        while idx <= scroll_down_units:
           pyautogui.scroll(scroll_down_units)
           idx += 1
        return True
    except:
        return False


# Not functioning at all #
def mouseScroll2(dt):
    x,y = get_uiobj_coords(dt)
    scroll_times = str(dt["visual_actions"]["scroll_times"])
    if(scroll_times is None or scroll_times == ""):
        scroll_times = "1"
    scroll_times = int(scroll_times)
    print(scroll_times)
    try:
        if(check_coords_integrity(x,y)):
            pyautogui.scroll(int(scroll_times),x,y)
        else:
            pyautogui.scroll(int(scroll_times))
        return True
    except:
        return False
