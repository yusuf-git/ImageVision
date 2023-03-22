#/############################################################
# Author : Yusuf
# Date & Time : 19-Apr-2020 12:00 AM To 06:30 AM, 21-Apr-2020 03:10 AM, 01-May-2020 05:00 AM to 8:00 AM, 11-Sep-2021 01:30 AM, 12-Sep-2021 01:30 AM, 11:50 PM 13-Sep-2021 01:45 AM, 14-Sep-2021 03:00 AM, 15-Sep-2021 12:35 AM, 03-Dec-2021 03:00 AM, 04-Dec-2021 03:15 AM, 05-Dec-2021 03:10 AM, 12-Dec-2021 04:15 PM to 11:55 PM, 13-Dec-2021 01:15 AM, 14-Dec-2021 12:30 AM, 05:55 AM to 11:30 AM, 15-Dec-2021 02:30 AM
###############################################################
# import the necessary pages
#from posix import times_result
import PIL
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
import datetime
from PIL import ImageGrab
from PIL import Image
from data_models.RT_negative_cond_result import RT_negative_cond_result
from data_models.RT_positive_cond_result import RT_positive_cond_result


def select_matched_instance(cnt, pick, PIL_img, dt, startX,startY,endX,endY):
    filename_indicator = ""
    if(cnt != 0 and cnt != len(pick)-1):
        return False
    matched_instance_selection = str(dt["actionize_args"]["action_inputs"]["matched_instance"]).lower()
    print("[INFO] selected_match_instance:",matched_instance_selection)
    if(cnt == 0 and matched_instance_selection == "first"):
        filename_indicator = "f"
    elif(cnt == len(pick)-1 and matched_instance_selection == "last"):
        filename_indicator = "l"
    
    if((cnt == 0 and matched_instance_selection == "first") or (cnt == len(pick)-1 and matched_instance_selection == "last")):
        dttime = datetime.datetime.now()
        dt_time_part = "{0}-{1}-{2}_{3}-{4}-{5}".format(dttime.day,dttime.month,str(dttime.year)[2:],dttime.hour,dttime.minute,dttime.second)
        screen_snaps_path = dt["actionize_args"]["screen_snaps_path"]
        template_img_name = str(os.path.basename(dt["actionize_args"]["template_img"])).split(".")[0]
        img_cropped = PIL_img.crop((startX,startY,endX,endY))
        img_cropped.save(os.path.join(screen_snaps_path,  template_img_name +"_" + filename_indicator +"_"+ dt_time_part +".png"))
        return True
    return False


def bg_mask(img_path):
    # opencv loads the image in BGR, convert it to RGB
    img_file1 = 'C:\py\demo\RTFilterImages\CPPTooltip_top_A.png'
    img_file2 = 'C:\py\demo\RTFilterImages\RPPDataGap_top.png'

    for img_file in glob.glob(os.path.join(str(img_path) + "/*.png")):
        maksed_filename = os.path.join(img_file, str(os.path.basename(img_file)).split('.')[0]+"-bgmasked" +".png")
        masked_filename = os.path.join(os.path.dirname(img_file), os.path.basename(img_file).split('.')[0]+"-bgmasked" +".png")
        print("masked filename:",maksed_filename)
        img = cv2.cvtColor(cv2.imread(img_file2), cv2.COLOR_BGR2RGB)
        lower_white = np.array([220, 220, 220], dtype=np.uint8)
        upper_white = np.array([255, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(img, lower_white, upper_white)  # could also use threshold
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # "erase" the small white points in the resulting mask
        mask = cv2.bitwise_not(mask)  # invert mask

        # load background (could be an image too)
        bk = np.full(img.shape, 255, dtype=np.uint8)  # white bk

        # get masked foreground
        fg_masked = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("fg_masked", fg_masked)
        cv2.waitKey(0)
 
        # get masked background, mask must be inverted 
        mask = cv2.bitwise_not(mask)
        bk_masked = cv2.bitwise_and(bk, bk, mask=mask)
        cv2.imwrite(maksed_filename,bk_masked)
        cv2.imshow("bk_masked", bk_masked)
        cv2.waitKey(0)

        # combine masked foreground and masked background 
        final = cv2.bitwise_or(fg_masked, bk_masked)
        mask = cv2.bitwise_not(mask)  # revert mask to original
        cv2.imshow("final", mask)
        cv2.waitKey(0)
    


def multi_template_match(dt):
    print("[INFO] object detection algo variant : MULTI TEMPLATE MATCH")
    print("[INFO] beginning the visual info search....")
    curr_scr_file = dt["visual_actions"]["curr_scr_snap"]
    rects = []
    threshold = str(dt["actionize_args"]["search_methods"][0]["m1_threshold"])
    screen_snaps_path = str(os.path.join(dt["actionize_args"]["screen_snaps_path"]))
    threshold = float(threshold)
    cnt = 0
    instance_selection_result_from_coll = False

    # load the input image and template image from disk, then grab the
    # template image spatial dimensions
    print("[INFO] grabbing the current screen...")
    dyn_img = ImageGrab.grab()
    dyn_img.save(curr_scr_file)
    time.sleep(0.2)

    image = cv2.imread(curr_scr_file)
    PIL_img = Image.open(curr_scr_file)
    orig_img = image
    print("[INFO] loading the input image...")
    template = cv2.imread(dt["actionize_args"]["template_img"])
    (tH, tW) = template.shape[:2]
    
    # display the  image and template to our screen
    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
        cv2.imshow("Input Image", image)
        cv2.imshow("Template", template)

    # convert both the image and template to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # perform template matching
    print("[INFO] performing the matching operation...")
    result = cv2.matchTemplate(imageGray, templateGray,
	    cv2.TM_CCOEFF_NORMED)

    # find all locations in the result map where the matched value is
    # greater than the threshold, then clone the original image so we
    # can draw on it
    (yCoords, xCoords) = np.where(result >= threshold)
    clone = image.copy()
    print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
    # loop over our starting (x, y)-coordinates
    for (x, y) in zip(xCoords, yCoords):
	    # draw the bounding box on the image
	    cv2.rectangle(image, (x, y), (x + tW, y + tH), (0,0, 255), 2)

    # show our output image *before* applying non-maxima suppression
    #if args.get("visualize", False):
    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
        cv2.imshow("Before NMS", clone)
        cv2.waitKey(0)

    # loop over the starting (x, y)-coordinates again
    for (x, y) in zip(xCoords, yCoords):
    #for (x, y) in zip(*(xCoords, yCoords)[::-1]):
    	    # update the list of rectangles
	    rects.append((x, y, x + tW, y + tH))
    
    # apply non-maxima suppression to the rectangles
    pick = non_max_suppression(np.array(rects))
    print("[INFO] {} matched locations *after* NMS".format(len(pick)))
    
    # loop over the final bounding boxes
    for (startX, startY, endX, endY) in pick:
	    # draw the bounding box on the image
	    cv2.rectangle(image, (startX, startY), (endX, endY),
		    (0, 0, 255), 2)
	    if(len(screen_snaps_path) > 0 and not instance_selection_result_from_coll) :
	        instance_selection_result_from_coll = select_matched_instance(cnt,pick,PIL_img,dt,startX, startY,endX, endY)
	        print("[INFO] matched instance selection result:",instance_selection_result_from_coll)
	        cnt += 1
	        print("[INFO] Selected match count :",cnt)

            
    # show the output image6
    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
        cv2.imshow("After NMS", image)
        cv2.waitKey(0)

    print("[INFO] visual info coords:",pick)
    cv2.imwrite(curr_scr_file, image)
    return pick, orig_img




def multi_template_match_multi_base(dt):
    print("[INFO] object detection algo variant : MULTI TEMPLATE MATCH-MULTI BASE")
    print("[INFO] beginning the visual info search....")
    curr_scr_file = dt["visual_actions"]["curr_scr_snap"]
    rects = []
    threshold = str(dt["actionize_args"]["search_methods"][0]["m1_threshold"])
    screen_snaps_path = str(os.path.join(dt["actionize_args"]["screen_snaps_path"]))
    threshold = float(threshold)
    cnt = 0
    instance_selection_result_from_coll = False

    # load the input image and template image from disk, then grab the
    # template image spatial dimensions
    print("[INFO] grabbing the current screen...")
    dyn_img = ImageGrab.grab()
    dyn_img.save(curr_scr_file)
    time.sleep(0.2)

    image = cv2.imread(curr_scr_file)
    PIL_img = Image.open(curr_scr_file)
    orig_img = image
    print("[INFO] loading the input image...")

    for template_file in glob.glob(str(os.path.dirname(dt["actionize_args"]["template_img"]) + "/*.png")):
        print("template :",template_file)
        #if(os.path.isfile(str(dt["actionize_args"]["template_img"])) and template_file.lower().endswith(".png")):
        #    tmp_fname = template_file.split('.')
        #    fname_ = tmp_fname[0] + "_" + str(idx_) + "." + tmp_fname[1]

        template = cv2.imread(template_file)
        (tH, tW) = template.shape[:2]
    
        # display the  image and template to our screen
        if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
            cv2.imshow("Input Image", image)
            cv2.imshow("Template", template)

        # convert both the image and template to grayscale
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # perform template matching
        print("[INFO] performing the matching operation...")
        result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)

        # find all locations in the result map where the matched value is
        # greater than the threshold, then clone the original image so we
        # can draw on it
        (yCoords, xCoords) = np.where(result >= threshold)
        clone = image.copy()
        print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
        # loop over our starting (x, y)-coordinates
        for (x, y) in zip(xCoords, yCoords):
	        # draw the bounding box on the image
	        cv2.rectangle(image, (x, y), (x + tW, y + tH), (0,0, 255), 2)

        # show our output image *before* applying non-maxima suppression
        if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
            cv2.imshow("Before NMS", clone)
            cv2.waitKey(0)

        # loop over the starting (x, y)-coordinates again
        for (x, y) in zip(xCoords, yCoords):
        #for (x, y) in zip(*(xCoords, yCoords)[::-1]):
    	    # update the list of rectangles
	        rects.append((x, y, x + tW, y + tH))
    
        # apply non-maxima suppression to the rectangles
        pick = non_max_suppression(np.array(rects))
        print("[INFO] {} matched locations *after* NMS".format(len(pick)))
        #if(len(pick) <= 0):
        #    continue
    
        # loop over the final bounding boxes
        for (startX, startY, endX, endY) in pick:
	        # draw the bounding box on the image
	        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	        if(len(screen_snaps_path) > 0 and not instance_selection_result_from_coll) :
	            instance_selection_result_from_coll = select_matched_instance(cnt,pick,PIL_img,dt,startX, startY,endX, endY)
	            print("[INFO] matched instance selection result:",instance_selection_result_from_coll)
	            cnt += 1
	            print("[INFO] Selected match count :",cnt)
            
        # show the output image6
        if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
            cv2.imshow("After NMS", image)
            cv2.waitKey(0)
        
        if(len(pick) > 0):
            print("[INFO] visual info coords:",pick)
        if(len(pick) > 0):
            break
 
    cv2.imwrite(curr_scr_file, image)
    return pick, orig_img




def RT_multi_template_match_multi_base( dt):
    print("[INFO] object detection algo variant : MULTI TEMPLATE MATCH-MULTI BASE")
    #print("[INFO] beginning the bakground masking....")
    rt_pos_path = dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"]
    rt_neg_path = dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"]
    runtime_imgs_path = dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"]
    neg_condition_check_mode = str(dt["actionize_args"]["RT_anomaly_detection"]["neg_condition_check_mode"])
    curr_base_imgs_path = ""
    if(str(neg_condition_check_mode).lower() == "true"):
        curr_base_imgs_path = rt_neg_path
    else:
        curr_base_imgs_path = rt_pos_path
    
    #bg_mask(glob.glob(os.path.join(curr_base_imgs_path + "/*.png")))
    #bg_mask(glob.glob(os.path.join(runtime_imgs_path + "/*.png")))
    
    curr_scr_file = dt["visual_actions"]["curr_scr_snap"]
    reports_path = str(dt["actionize_args"]["RT_anomaly_detection"]["reports_path"])
    #net_result_path = str(dt["actionize_args"]["net_result_path"])
    rects = []
    threshold = str(dt["actionize_args"]["search_methods"][0]["m1_threshold"])
    screen_snaps_path = str(os.path.join(dt["actionize_args"]["screen_snaps_path"]))
    threshold = float(threshold)
    cnt = 0
    instance_selection_result_from_coll = False
    net_result = True
    rt_result = False
    
    print("curr_base_imgs_path:",curr_base_imgs_path)
    #time.sleep(5)

    # load the input image and template image from disk, then grab the
    # template image spatial dimensions
    #print("[INFO] grabbing the current screen...")
    #dyn_img = ImageGrab.grab()
    #dyn_img.save(curr_scr_file)
    #time.sleep(0.2)
 
   # runtime img : r1
   # baseline    : gap1 --> gap1 found in r1 ? yes --> pick r2

    for runtime_img in glob.glob(os.path.join(runtime_imgs_path + "/*.png")):
        rt_result = False
        print("----------------------------------------------------------")
        print("[INFO] runtime image:",runtime_img)
        curr_report_file_passed = os.path.join(reports_path, "passed/", os.path.basename(runtime_img))
        curr_report_file_failed = os.path.join(reports_path, "failed/", os.path.basename(runtime_img))
        
        if(not os.path.exists(os.path.dirname(curr_report_file_passed))):
            os.makedirs(os.path.dirname(curr_report_file_passed))
        if(not os.path.exists(os.path.dirname(curr_report_file_failed))):
            os.makedirs(os.path.dirname(curr_report_file_failed))

        image = cv2.imread(runtime_img)
        PIL_img = Image.open(runtime_img)
        orig_img = image
        pick = []
        rects = []

        #print('glob.glob(os.path.join(curr_base_imgs_path + "/*.png")):',len(glob.glob(os.path.join(curr_base_imgs_path + "/*.png"))))
        #time.sleep(6)
        #time.sleep(1)
        for template_file in glob.glob(os.path.join(curr_base_imgs_path + "/*.png")):
            pick = []
            rects = []
            print("[INFO] baseline image :",template_file)
            #time.sleep(2)
            template = cv2.imread(template_file)
            (tH, tW) = template.shape[:2]
    
            # display the  image and template to our screen
            if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
                cv2.imshow("Runtime image", image)
                cv2.imshow("Baseline Image", template)

            # convert both the image and template to grayscale
            imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # perform template matching
            print("[INFO] performing the matching operation...")
            result = cv2.matchTemplate(imageGray, templateGray, cv2.TM_CCOEFF_NORMED)

            # find all locations in the result map where the matched value is
            # greater than the threshold, then clone the original image so we
            # can draw on it
            (yCoords, xCoords) = np.where(result >= threshold)
            clone = image.copy()
            print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
            # loop over our starting (x, y)-coordinates
            for (x, y) in zip(xCoords, yCoords):
	            # draw the bounding box on the image
	            cv2.rectangle(image, (x, y), (x + tW, y + tH), (0,0, 255), 2)

            # show our output image *before* applying non-maxima suppression
            if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
                cv2.imshow("Before NMS", clone)
                cv2.waitKey(0)

            # loop over the starting (x, y)-coordinates again
            for (x, y) in zip(xCoords, yCoords):
            #for (x, y) in zip(*(xCoords, yCoords)[::-1]):
    	        # update the list of rectangles
	            rects.append((x, y, x + tW, y + tH))
    
            # apply non-maxima suppression to the rectangles
            pick = non_max_suppression(np.array(rects))
            print("[INFO] {} matched locations *after* NMS".format(len(pick)))
            print("[INFO] visual info coords:",pick)
            #if(len(pick) <= 0):
            #    continue
    
            # loop over the final bounding boxes
            for (startX, startY, endX, endY) in pick:
	            # draw the bounding box on the image
	            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	            if(len(screen_snaps_path) > 0 and not instance_selection_result_from_coll) :
	                instance_selection_result_from_coll = select_matched_instance(cnt,pick,PIL_img,dt,startX, startY,endX, endY)
	                print("[INFO] matched instance selection result:",instance_selection_result_from_coll)
	                cnt += 1
	                print("[INFO] Selected match count :",cnt)
            
            # show the output image6
            if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
                cv2.imshow("After NMS", image)
                cv2.waitKey(0)
        
            #if(len(pick) > 0):
            
            print("----------------------------------------------------------")
            
            if(len(pick) > 0):
                print("pick:",pick)
                if(str(neg_condition_check_mode).lower() == "true"):
                    rt_result = False
                    break
                else:
                    rt_result = True
                    break
            elif (len(pick) <= 0):
                if(str(neg_condition_check_mode).lower() == "true"):
                    rt_result = True
                    continue
                else:
                    rt_result = False
                    continue

        
        if(rt_result):
            cv2.imwrite(curr_report_file_passed, image)
            print("result : true")
            if(str(neg_condition_check_mode).lower() == "true"):
                RT_negative_cond_result.result_list.append(RT_negative_cond_result(runtime_img, str(rt_result)))
            else:
                RT_positive_cond_result.result_list.append(RT_positive_cond_result(runtime_img, str(rt_result)))
            #RT_negative_cond_result.result_list.append(RT_negative_cond_result(runtime_img, str(rt_result)))
        else:
            net_result = False
            cv2.imwrite(curr_report_file_failed, image)
            print("result : false")
            if(str(neg_condition_check_mode).lower() == "true"):
                RT_negative_cond_result.result_list.append(RT_negative_cond_result(runtime_img, str(rt_result)))
            else:
                RT_positive_cond_result.result_list.append(RT_positive_cond_result(runtime_img, str(rt_result)))
        
    print("net result:",net_result)
    return net_result, RT_negative_cond_result.result_list, RT_positive_cond_result.result_list





# Updates on 23-Sep-2021 01:00 AM, 24-Sep-2021 02:35 AM
def multi_template_match_multi_base_multi_scale(dt):
    print("multi-template-multi-base")
    screen_snaps_path = str(os.path.join(dt["actionize_args"]["screen_snaps_path"]))
    #temp_out_path = str(os.path.join(str(dt["actionize_args"]["output_imgs_path"]),"screen_snaps"))
    curr_scr_file = str(os.path.join(screen_snaps_path,"curr_screen.png"))
    # initialize our list of rectangles
    rects = []
    pick = []
    threshold = 0.9
    cnt = 0
    instance_selection_result_from_coll = False
    #img_out_path = os.path.join(dt["actionize_args"]["output_imgs_path"])

    # load the input image and template image from disk, then grab the
    # template image spatial dimensions
    print("[INFO] grabbing the current screen...")
    dyn_img = ImageGrab.grab()
    dyn_img.save(curr_scr_file)
    time.sleep(0.2) 
    #image = cv2.imread(args["image"])
    curr_scr_image = cv2.imread(curr_scr_file)
    curr_scr_Gray = cv2.cvtColor(curr_scr_image, cv2.COLOR_BGR2GRAY)
    PIL_img = Image.open(curr_scr_file)
    orig_img = curr_scr_image
    nms_idx = 1
    #template = cv2.imread(args["template"])
    print("[INFO] loading the template image...")

    for template_file in glob.glob(str(dt["actionize_args"]["template_img_path"] + "/*.png")):
	    # load the image, convert it to grayscale, and initialize the
	    # bookkeeping variable to keep track of the matched region
	    rects = []
        
	    template_image = cv2.imread(template_file)
	    templateGray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
	    #time.sleep(0.5)
	    found = None
        #template = cv2.imread(dt["actionize_args"]["template_img"])
	    (tH, tW) = template_image.shape[:2]
	    #(tH, tW) = curr_scr_image.shape[:2]
    
        # display the  image and template to our screen
	    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
	        cv2.imshow("Input Image", curr_scr_image)
	        cv2.imshow("Template", template_image)
	        cv2.waitKey(0)

        # convert both the image and template to grayscale
	    print("template image:",template_file)
	    for scale in np.linspace(0.2, 2.0, 60)[::-1]:
            # resize the image according to the scale, and keep track
		    # of the ratio of the resizing
	        #resized = imutils.resize(curr_scr_Gray, width = int(curr_scr_Gray.shape[1] * scale))
	        resized = imutils.resize(templateGray, width = int(templateGray.shape[1] * scale))
	        #r = curr_scr_Gray.shape[1] / float(resized.shape[1])
	        r = templateGray.shape[1] / float(resized.shape[1])
		    # if the resized image is smaller than the template, then break
		    # from the loop
	        if resized.shape[0] < tH or resized.shape[1] < tW:
	            print("breaking.....from linspace")
	            break
            # detect edges in the resized, grayscale image and apply template
		    # matching to find the template in the image
            #edged = cv2.Canny(resized, 50, 200)
            #result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            #print("result------AAAA:",result)
     #      (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # perform template matching
	        print("[INFO] performing template matching...")
	        #result = cv2.matchTemplate(curr_scr_Gray, resized,cv2.TM_CCOEFF_NORMED)
	        #result = cv2.matchTemplate(resized, templateGray, cv2.TM_CCOEFF_NORMED)
	        result = cv2.matchTemplate(curr_scr_Gray, resized, cv2.TM_CCOEFF_NORMED)

            # find all locations in the result map where the matched value is
            # greater than the threshold, then clone the original image so we
            # can draw on it
	        (yCoords, xCoords) = np.where(result >= threshold)
	        if(len(yCoords) > 0 and len(xCoords) > 0):
	            print("************************************")
	            print("match found for the ratio:",r)
	            print("************************************")
	            #time.sleep(1)
	        else:
	            continue
	            #continue
	            
	        clone = curr_scr_Gray.copy()
       
	        print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
            # loop over our starting (x, y)-coordinates
	        for (x, y) in zip(xCoords, yCoords):
	            # draw the bounding box on the image
	            bef_NMS_img = cv2.rectangle(clone, (x, y), (x + tW, y + tH),
		            (255, 0, 0), 3)
                
                # show our output image *before* applying non-maxima suppression
                #if args.get("visualize", False):
	            if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
	                cv2.imshow("Before NMS", bef_NMS_img)
	                cv2.waitKey(0)

	        rects = []
            # loop over the starting (x, y)-coordinates again
	        for (x, y) in zip(xCoords, yCoords):
	            # update the list of rectangles
	            rects.append((x, y, x + tW, y + tH))
            
   
            # apply non-maxima suppression to the rectangles
	        pick = []
	        pick = non_max_suppression(np.array(rects))
	        print("[INFO] {} matched locations *after* NMS".format(len(pick)))
	        print("[INFO] rects :", rects)
	        print("[INFO] - pick:",pick)
	        #time.sleep(1)
    
            # loop over the final bounding boxes
	        for (startX, startY, endX, endY) in pick:
	        # draw the bounding box on the image
	            tmp_img = cv2.rectangle(curr_scr_image, (startX, startY), (endX, endY),
		            (255, 0, 0), 3)
	            after_NMS_img = os.path.join(screen_snaps_path, "aft_NMS_img_"+str(nms_idx)+".png")
	            print(after_NMS_img)
	            #time.sleep(3)
	            cv2.imwrite(after_NMS_img, tmp_img)
	            nms_idx += 1
	            #cv2.imshow("final matched image:",tmp_img)
	            #cv2.waitKey(0)

	            #if(len(img_out_path) > 0 and not instance_selection_result_from_coll) :
	            #    instance_selection_result_from_coll = select_matched_instance(cnt,pick,PIL_img,dt,startX, startY,endX, endY)
	            #    print("matched instance selection result:",instance_selection_result_from_coll)
	            #    cnt += 1
	            #    print("cnt:",cnt)

            
        # show the output image
        #if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
        #    cv2.imshow("After NMS", curr_scr_image)
        #    cv2.waitKey(0)

    print("final result:",pick)
    return pick, orig_img


def multi_template_match_multi_base_prev(dt):
    print("multi-template-multi-base")
    #temp_out_path = str(os.path.join(str(dt["actionize_args"]["output_imgs_path"]),"screen_snaps"))
    screen_snaps_path = str(os.path.join(dt["actionize_args"]["screen_snaps_path"]))
    curr_scr_file = str(os.path.join(screen_snaps_path,"curr_screen.png"))
    
    # initialize our list of rectangles
    rects = []
    threshold = 0.8
    cnt = 0
    instance_selection_result_from_coll = False
    #img_out_path = os.path.join(dt["actionize_args"]["output_imgs_path"])

    # load the input image and template image from disk, then grab the
    # template image spatial dimensions
    print("[INFO] grabbing the current screen...")
    dyn_img = ImageGrab.grab()
    dyn_img.save(curr_scr_file)
    time.sleep(0.2) 
    #image = cv2.imread(args["image"])
    curr_scr_image = cv2.imread(curr_scr_file)
    #PIL_img = Image.open(curr_scr_file)
    cv2.namedWindow('curr_scr', cv2.WINDOW_NORMAL)
    cv2.imshow("curr_scr",curr_scr_image)
    cv2.waitKey(0)
    orig_img = curr_scr_image
    #template = cv2.imread(args["template"])
    # convert both the image and template to grayscale
    curr_scr_Gray = cv2.cvtColor(curr_scr_image, cv2.COLOR_BGR2GRAY)
    print("np.linspace:",np.linspace(0.2, 1.0, 20)[::-1])    
    time.sleep(10)

    for template_file in glob.glob(str(dt["actionize_args"]["template_img_path"] + "/*.png")):
	    # load the image, convert it to grayscale, and initialize the
	    # bookkeeping variable to keep track of the matched region
	    print("[INFO] loading the template image :",template_file)
	    template_image = cv2.imread(template_file)
	    if(str(dt["actionize_args"]["intermediate_output"]) == "false"):
	        cv2.imshow("Original tempate Image", template_image)
	        cv2.waitKey(0)
	    #time.sleep(0.5)
	    #template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
	    found = None

        #template = cv2.imread(dt["actionize_args"]["template_img"])
	    (tH, tW) = template_image.shape[:2]
    
        # display the  image and template to our screen
	    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
	        cv2.imshow("Input Image", curr_scr_image)
	        cv2.imshow("Template", template_image)

    

	    templateGray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
	    print("template image:",template_file)
	    result = cv2.matchTemplate(curr_scr_Gray, templateGray,
	        cv2.TM_CCOEFF_NORMED)

            # find all locations in the result map where the matched value is
            # greater than the threshold, then clone the original image so we
        # can draw on it
	    (yCoords, xCoords) = np.where(result >= threshold)
	    clone = curr_scr_Gray.copy()
	    print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
        # loop over our starting (x, y)-coordinates
	    for (x, y) in zip(xCoords, yCoords):
            # draw the bounding box on the image
	        cv2.rectangle(clone, (x, y), (x + tW, y + tH),
		            (255, 0, 0), 3)

            # show our output image *before* applying non-maxima suppression
            #if args.get("visualize", False):
	    if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
	        cv2.imshow("Before NMS", clone)
	        cv2.waitKey(0)


            # loop over the starting (x, y)-coordinates again
	    for (x, y) in zip(xCoords, yCoords):
	        # update the list of rectangles
	        rects.append((x, y, x + tW, y + tH))
    
            # apply non-maxima suppression to the rectangles
	    pick = non_max_suppression(np.array(rects))
	    print("[INFO] {} matched locations *after* NMS".format(len(pick)))
    
        # loop over the final bounding boxes
	    for (startX, startY, endX, endY) in pick:
	        # draw the bounding box on the image
	        rect_img = cv2.rectangle(curr_scr_image, (startX, startY), (endX, endY),
		        (255, 0, 0), 3)
	        cv2.imshow("curr_sr_image",rect_img)
	        cv2.waitKey(0)

        
	    if(len(pick) > 0):
	        break
	            #if(len(img_out_path) > 0 and not instance_selection_result_from_coll) :
	             #    instance_selection_result_from_coll = select_matched_instance(cnt,pick,PIL_img,dt,startX, startY,endX, endY)
	            #    print("matched instance selection result:",instance_selection_result_from_coll)
	            #    cnt += 1
	            #    print("cnt:",cnt)

            
        # show the output image
        #if str(dt["actionize_args"]["intermediate_output"]).lower() == "true":
        #    cv2.imshow("After NMS", curr_scr_image)
        #    cv2.waitKey(0)

    print("final result:",pick)
    return pick, orig_img



def multi_scale_template_match():
    print("multi_scale")
    coord_list = []
    #time.sleep(1)
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--template", required=True, help="Path to template image")
    ap.add_argument("-c", "--images", required=True,
	    help="Path to images where template will be matched")
    ap.add_argument("-b", "--threshold", type=float, default=0.8,
	    help="threshold for multi-template matching")
    ap.add_argument("-v", "--visualize",
	    help="Flag indicating whether or not to visualize each iteration")
    args = vars(ap.parse_args())
    # load the image image, convert it to grayscale, and detect edges
    template = cv2.imread(args["template"])
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    if args.get("visualize", False):
        cv2.imshow("Template", template)
        cv2.waitKey(0)

    # loop over the images to find the template in
    for imagePath in glob.glob(args["images"] + "/*.png"):
	    # load the image, convert it to grayscale, and initialize the
	    # bookkeeping variable to keep track of the matched region
	    image = cv2.imread(imagePath)
	    if args.get("visualize", False):
	        cv2.imshow("Visualize", image)
	        cv2.waitKey(0)
	    #time.sleep(0.5)
	    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	    found = None
	    # loop over the scales of the image
	    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		    # resize the image according to the scale, and keep track
		    # of the ratio of the resizing
		    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		    r = gray.shape[1] / float(resized.shape[1])
		    # if the resized image is smaller than the template, then break
		    # from the loop
		    if resized.shape[0] < tH or resized.shape[1] < tW:
			    break
            		# detect edges in the resized, grayscale image and apply template
		    # matching to find the template in the image
		    edged = cv2.Canny(resized, 50, 200)
		    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
		    print("result------AAAA:",result)
		    (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		    if args.get("visualize", False):
			    clone = np.dstack([edged, edged, edged])
			    cv2.rectangle(clone, (maxLoc[0], maxLoc[1]),
				    (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
			    cv2.imshow("Visualize", clone)
			    cv2.waitKey(0)

		    if found is None or maxVal > found[0]:
			    found = (maxVal, maxLoc, r)

	    if(found is not None):
	        print("Not none:",found)
	        time.sleep(10)
	    (_, maxLoc, r) = found
	    (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
	    (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

	    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
	    print("maxVal:",maxVal)   
	    time.sleep(8)

      
	    if args.get("visualize", False):
	        cv2.imshow("Image", image)
	        cv2.waitKey(0)
	    coord_list.append(startX)
	    coord_list.append(startY)
	    coord_list.append(endX)
	    coord_list.append(endY)

	    #print("ABC-X:",(startX+endX)/2," ABC-Y:",(startY+endY)/2)
	    #return ((startX+endX)/2,(startY+endY)/2)
    return (startX,endX,startY,endY), image 



def multi_scale_multi_template_match(screenCapture=False):
    print("multi_scale multi template")
    time.sleep(3)
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--template", required=True, help="Path to template image")
    ap.add_argument("-c", "--images", required=True,
	    help="Path to images where template will be matched")
    ap.add_argument("-b", "--threshold", type=float, default=0.8,
	    help="threshold for multi-template matching")
    ap.add_argument("-v", "--visualize",
	    help="Flag indicating whether or not to visualize each iteration")
    args = vars(ap.parse_args())

    print("[INFO] loading images...")
    if(screenCapture):
        time.sleep(6)
        dyn_img = ImageGrab.grab()  # X1,Y1,X2,Y2)
        #dyn_img.save("D:\Explore\AI\CV\Exercises\sdv\pyimagesearch\images\curr_screen.png")
        dyn_img.save(str(os.path.join(args["images"], "curr_screen.png")))
        
        time.sleep(0.7)
        #image = cv2.imread(args["image"])
        #image = cv2.imread(str(os.path.join(args["images"], "curr_screen.png")))
        #orig_img = image

    # load the image image, convert it to grayscale, and detect edges
    template = cv2.imread(args["template"])
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    cv2.imshow("Template", template)
    cv2.waitKey(0)



    # loop over the images to find the template in
    for imagePath in glob.glob(args["images"] + "/*.png"):
	    # load the image, convert it to grayscale, and initialize the
	    # bookkeeping variable to keep track of the matched region
	    image = cv2.imread(imagePath)
	    orig_img = image
	    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	    found = None
	    # loop over the scales of the image
	    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		    # resize the image according to the scale, and keep track
		    # of the ratio of the resizing
		    resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		    r = gray.shape[1] / float(resized.shape[1])
		    # if the resized image is smaller than the template, then break
		    # from the loop
		    if resized.shape[0] < tH or resized.shape[1] < tW:
			    break
            		# detect edges in the resized, grayscale image and apply template
		    # matching to find the template in the image
		    edged = cv2.Canny(resized, 50, 200)
		    result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)




		    (yCoords, xCoords) = np.where(result >= args["threshold"])
		    clone = image.copy()
		    print("[INFO] {} matched locations *before* NMS".format(len(yCoords)))
            # loop over our starting (x, y)-coordinates
		    for (x, y) in zip(xCoords, yCoords):
	            # draw the bounding box on the image
		        cv2.rectangle(clone, (x, y), (x + tW, y + tH),
		            (255, 0, 0), 3)
                # show our output image *before* applying non-maxima suppression
		        cv2.imshow("Before NMS", clone)
		        cv2.waitKey(0)

                # initialize our list of rectangles
		        rects = []
                # loop over the starting (x, y)-coordinates again

		    for (x, y) in zip(xCoords, yCoords):
	            # update our list of rectangles
		        rects.append((x, y, x + tW, y + tH))
                # apply non-maxima suppression to the rectangles
		        pick = non_max_suppression(np.array(rects))
		        print("[INFO] {} matched locations *after* NMS".format(len(pick)))
                    # loop over the final bounding boxes
		    for (startX, startY, endX, endY) in pick:
	            # draw the bounding box on the image
		        cv2.rectangle(image, (startX, startY), (endX, endY),
		            (255, 0, 0), 3)
                # show the output image
		        cv2.imshow("After NMS", image)
		        cv2.waitKey(0)
                #cv2.destroyAllWindows()
		    time.sleep(9)
    #print("final result:",pick)
    return pick,orig_img




