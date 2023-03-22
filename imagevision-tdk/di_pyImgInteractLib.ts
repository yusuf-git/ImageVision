/******************** 
* Author : Yusuf
* Authored on : 30-Jul-2020 10:30 PM
* Updates on   : 31-Jul-2020 01:00 AM, 06:45 AM, 06:17 PM, 05-Aug-2020 2:55 AM, 06-Dec-2021 03:00 AM, 19-Dec-2021 11:30 AM to 03:00 PM, 20-Dec-2021 06:47 PM
* Depdendency Injection for py CV image library
*
*********************/

import * as fse from 'fs-extra'
import { browser, by, protractor, ExpectedConditions } from "protractor"
import * as path from "path"
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework"
import * as cp from 'child_process'
//import {PythonShell} from 'python-shell'
import * as fs from 'fs'
import { fs_helper as fsh, fs_helper } from "./../helpers/fs_helper"
import { async } from 'q'
import { AppFeatures_CV } from "./appfeatures_cv"
import { pathRefs } from './pathRefs'


export class di_pyImgInteractLib {

    constructor() {
        this.setDefault()
    }
    

    setDefault() {
        this.appFeatures_CV = ""
        this.template_img = ""
        this.reports_path = ""
        this.net_result_path = ""
        this.actions = ""
        this.browserDependent = "false"
        this.intermediate_output = "false"
        this.purge_old_artifacts = "false"
        this.continue_on_failure = "false"
        this.imgArchivesPath = ""
        this.action_inputs.type_text = ""
        this.action_inputs.scroll_up_units = "600"
        this.action_inputs.scroll_down_units = "-600"
        this.action_inputs.rel_x_y = "",
        this.action_inputs.mouse_move_delay = "1"
        this.action_inputs.mouse_drag_to_coords = ""
        this.action_inputs.drop_target_img = ""
        this.action_inputs.wait_seconds = "0"
        this.action_inputs.matched_instance = "first" //other supported option : "last"
        this.search_methods.method1 = "template_matching"
        this.search_methods.m1_threshold = "0.8"
        this.realtime_mode = "false"
        this.RT_anomaly_detection.neg_condition_check_mode = "true"
        this.RT_anomaly_detection.reports_path = ""
        this.RT_anomaly_detection.net_result_path = ""
        this.RT_anomaly_detection.runtime_imgs_path = ""
        this.RT_anomaly_detection.positive_conditions.baseline_path = ""
        this.RT_anomaly_detection.negative_conditions.baseline_path = ""
        //pathRefs.runTimeImgPath = ""
        //pathRefs.baselineImgPath = ""
        //pathRefs.reportsPath = ""
        //pathRefs.resultPath = ""
    }

    public getCurrentConfigs():IpyActionizeLib{
        let search_methods : Array<search_methods> = []
        let di_py = {
            appFeatures_CV : this.dt["actionize_args"]["appFeatures_CV"],
            template_img : this.dt["actionize_args"]["template_img"],
            actions : this.dt["actionize_args"]["actions"],
            reports_path : this.dt["actionize_args"]["reports_path"],
            net_result_path : this.dt["actionize_args"]["net_result_path"],
            imgArchivesPath : this.dt["actionize_args"]["imgArchivesPath"],
            continue_on_failure : this.dt["actionize_args"]["continue_on_failure"],
            browserDependent : this.dt["actionize_args"]["browserDependent"],
            intermediate_output : this.dt["actionize_args"]["intermediate_output"],
            purge_old_artifacts : this.dt["actionize_args"]["purge_old_artifacts"],

            act_inputs_type_text : this.dt["actionize_args"]["action_inputs"]["type_text"],
            act_inputs_scroll_up_units : this.dt["actionize_args"]["action_inputs"]["scroll_up_units"],
            act_inputs_scroll_down_units : this.dt["actionize_args"]["action_inputs"]["scroll_down_units"],
            act_inputs_rel_x_y : this.dt["actionize_args"]["action_inputs"]["rel_x_y"],
            act_inputs_mouse_move_delay : this.dt["actionize_args"]["action_inputs"]["mouse_move_delay"],
            act_inputs_mouse_drag_to_coords : this.dt["actionize_args"]["action_inputs"]["mouse_drag_to_coords"],
            act_inputs_drop_target_img : this.dt["actionize_args"]["action_inputs"]["drop_target_img"],
            act_inputs_wait_seconds : this.dt["actionize_args"]["action_inputs"]["wait_seconds"],
            act_inputs_matched_instance : this.dt["actionize_args"]["action_inputs"]["matched_instance"],
            
            method1 : this.dt["actionize_args"]["search_methods"][0]["method1"],
            m1_threshold : this.dt["actionize_args"]["search_methods"][0]["m1_score"],

            realtime_mode : this.dt["actionize_args"]["realtime_mode"],
            RT_anodet_neg_condition_check_mode : this.dt["actionize_args"]["RT_anomaly_detection"]["neg_condition_check_mode"],
            RT_anodet_reports_path : this.dt["actionize_args"]["RT_anomaly_detection"]["reports_path"],
            RT_anodet_net_result_path : this.dt["actionize_args"]["RT_anomaly_detection"]["net_result_path"],
            RT_anodet_pos_baseline_path : this.dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"],
            RT_anodet_neg_baseline_path : this.dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"],
            RT_anodet_runtime_imgs_path : this.dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"],
        }
        
        this.action_inputs.type_text = di_py.act_inputs_type_text
        this.action_inputs.scroll_up_units = di_py.act_inputs_scroll_up_units
        this.action_inputs.scroll_down_units = di_py.act_inputs_scroll_down_units
        this.action_inputs.rel_x_y = di_py.act_inputs_rel_x_y
        this.action_inputs.mouse_move_delay = di_py.act_inputs_mouse_move_delay
        this.action_inputs.mouse_drag_to_coords = di_py.act_inputs_mouse_drag_to_coords
        this.action_inputs.drop_target_img = di_py.act_inputs_drop_target_img
        this.action_inputs.wait_seconds = di_py.act_inputs_wait_seconds
        this.action_inputs.matched_instance = di_py.act_inputs_matched_instance
        this.search_methods.method1 = di_py.method1
        this.search_methods.m1_threshold = di_py.m1_threshold
        this.RT_anomaly_detection.reports_path = di_py.RT_anodet_reports_path
        this.RT_anomaly_detection.net_result_path = di_py.RT_anodet_net_result_path
        this.RT_anomaly_detection.neg_condition_check_mode = di_py.RT_anodet_neg_condition_check_mode
        this.RT_anomaly_detection.runtime_imgs_path = di_py.RT_anodet_runtime_imgs_path
        this.RT_anomaly_detection.positive_conditions.baseline_path = di_py.RT_anodet_pos_baseline_path
        this.RT_anomaly_detection.negative_conditions.baseline_path = di_py.RT_anodet_neg_baseline_path
        return di_py

    }

    public get action_inputs():action_inputs{
        if(this._action_inputs == null || this._action_inputs == undefined){
            this._action_inputs = new action_inputs()
        }
        return this._action_inputs
    }


   /*  public get realtime():string{
       return this._realtime
   }
   public set realtime(paramValue:string){
       this._realtime = paramValue
   } */

    public get search_methods():search_methods{
        if(this._search_methods == null || this._search_methods == undefined){
            this._search_methods = new search_methods()
        }
        return this._search_methods
    }

    public get RT_anomaly_detection():RT_anomaly_detection {
        if(this._RT_anomaly_detection == null || this._RT_anomaly_detection == undefined){
            this._RT_anomaly_detection = new RT_anomaly_detection()
        }
        return this._RT_anomaly_detection
    }

    public get positive_conditions():positive_conditions{
        if(this._positive_conditions == null || this._positive_conditions == undefined){
            this._positive_conditions = new positive_conditions()
        }
        return this._positive_conditions
    }

    public get negative_conditions():negative_conditions{
        if(this._negative_conditions == null || this._negative_conditions == undefined){
            this._negative_conditions = new negative_conditions()
        }
        return this._negative_conditions
    }

    private argFile = path.join(browser.params.baseDir, '..', "py/cv-img-interact/actionize_configs.json")
    //private dt = require(this.argFile)
    private dt = JSON.parse(fs.readFileSync(this.argFile, 'utf-8'))
    private _appFeatures_CV = ""
    private _template_img = ""
    private _reports_path = ""
    private _net_result_path = ""
    private _actions = ""
    private _browserDependent = ""
    private _intermediate_output = ""
    private _purge_old_artifacts = ""
    private _continue_on_failure = ""
    private _realtime_mode = ""
    private _action_inputs:action_inputs = null
    private _search_methods:search_methods = null
    private _RT_anomaly_detection:RT_anomaly_detection = null
    private _positive_conditions:positive_conditions = null
    private _negative_conditions:negative_conditions = null
    
    appFeatures_CV = ""
    template_img = ""
    reports_path = ""
    imgArchivesPath = ""
    net_result_path = ""
    actions = ""
    browserDependent = ""
    intermediate_output = ""
    purge_old_artifacts = ""
    continue_on_failure = ""
    realtime_mode = ""

}



export interface IpyActionizeLib {
    appFeatures_CV : string
    template_img : string
    reports_path : string
    net_result_path : string
    imgArchivesPath : string
    actions : string
    browserDependent : string
    intermediate_output : string
    purge_old_artifacts : string
    continue_on_failure : string

    act_inputs_type_text : string
    act_inputs_scroll_up_units : string
    act_inputs_scroll_down_units : string
    act_inputs_rel_x_y : string
    act_inputs_mouse_move_delay : string
    act_inputs_mouse_drag_to_coords : string
    act_inputs_drop_target_img : string
    act_inputs_wait_seconds : string
    act_inputs_matched_instance : string
    method1 : string
    m1_threshold : string

    realtime_mode : string
    RT_anodet_neg_condition_check_mode : string
    RT_anodet_reports_path : string
    RT_anodet_net_result_path : string
    RT_anodet_pos_baseline_path : string
    RT_anodet_neg_baseline_path : string
    RT_anodet_runtime_imgs_path : string
}


export class action_inputs{
    public type_text:string
    public scroll_up_units:string
    public scroll_down_units:string
    public rel_x_y:string
    public mouse_move_delay:string
    public mouse_drag_to_coords:string
    public drop_target_img:string
    public wait_seconds:string
    public matched_instance:string
}

export class search_methods{
    method1 = ""
    m1_threshold = ""
}  

export class RT_anomaly_detection {
    neg_condition_check_mode = ""
    reports_path = ""
    net_result_path = ""
    runtime_imgs_path = ""
    _positive_conditions: positive_conditions = null

    _negative_conditions: negative_conditions = null 

    //positive_conditions:positive_conditions = null

    //negative_conditions:negative_conditions = null

    public get positive_conditions():positive_conditions{

        if(this._positive_conditions == null || this._positive_conditions == undefined){

            this._positive_conditions = new positive_conditions()

        }

        return this._positive_conditions

    }



    public get negative_conditions():negative_conditions{

        if(this._negative_conditions == null || this._negative_conditions == undefined){

            this._negative_conditions = new negative_conditions()

        }

        return this._negative_conditions

    }


}

export class positive_conditions{
    baseline_path = ""
}

export class negative_conditions{
    baseline_path = ""
}