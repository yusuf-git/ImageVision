/******************** 
* Author : Yusuf
* Authored on : 28-Jul-2020 12:35 AM
* Updates on  : 28-Jul-2020 04:00 AM, 30-Jul-2020 03:45 AM, 08:30 PM, 04-Aug-2020 10:20 PM, 09-Dec-2020 12:15 PM, 26-Dec-2020 01:40 AM
# v3 Updates  : 08-Oct-2021 to 10-Oct-2021 12:30 AM
* Depdendency Injection for py CV image comparison library
**************************************************/



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

export class di_pyImgCompLib {

    constructor() {
        this.setDefault()
    }
    

    setDefault() {
        this.appFeatures_CV = ""
        this.baselineImage = ""
        this.runtime_img = ""
        this.comp_reports_path = ""
        this.net_result_path = ""
        this.imgArchivesPath = ""
        this.browserDependent = "true"
        this.realtime = "false"
        this.uiObjSnap = "false"
        this.maskRegion = ""
        this.maskRegionExcluding = ""
        this.aspect_ratio_required = "true"
        this.intermediate_output = "false"
        this.purge_old_artifacts = "false"
        this.result_pattern_analyzer.failure_pattern_succession_density = "0"
        this.p_hash_parametric.hash_size = "8"
        this.d_hash_parametric.hash_size = "8"
        // this.hang_issue_ResultPath=this.hang_issue_ResultPath
	    // this.imgCompResultPath=this.imgCompResultPath
	    // this.imgInteractionResultPath=this.imgInteractionResultPath
        //this.hang_issue_checker_frequency=this.hang_issue_checker_frequency        
        this.BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = "false"
        this.BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = path.join(browser.params.baseDir,"./src/test-inputs/imagevision/data/baseline/briskflann_baseline.json")
        this.BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = "false"
        this.BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = "false"
        this.BRISK_FLANN_parametric.FLANNmatcher_accuracy = "0.5"

        this.similarity.method1 = "SSI"
        this.similarity.m1_score = "1"
        this.similarity.m1_match_operator = "and"
        this.similarity.m1_powered_on= "1"
        this.similarity.m1_eval_groupID = "1"
                
        this.similarity.method2 = "perceptual_hashing"
        this.similarity.m2_score = "0"
        this.similarity.m2_match_operator = "and"
        this.similarity.m2_powered_on= "1"
        this.similarity.m2_eval_groupID = "1"

        this.similarity.method3 = "BRISK-FLANN"
        this.similarity.m3_score = "0"
        this.similarity.m3_match_operator = "and"
        this.similarity.m3_powered_on= "1"
        this.similarity.m3_eval_groupID = "2"

        this.similarity.group_eval_operator = "or"

        pathRefs.runTimeImgPath = ""
        pathRefs.runtime_img = ""
        pathRefs.baselineImgPath = ""
        pathRefs.reportsPath = ""
        pathRefs.resultPath = ""
    }

    public getCurrentConfigs():IpyImgCompLib{
        let similarity_arr : Array<similarity> = []
        let di_py = {
        appFeatures_CV : this.dt["compare_args"]["appFeatures_CV"],
        baselineImage : this.dt["compare_args"]["baselineImage"],
        runtime_img : this.dt["compare_args"]["runtime_img"],
        comp_reports_path : this.dt["compare_args"]["comp_reports_path"],
        net_result_path : this.dt["compare_args"]["net_result_path"],
        imgArchivesPath : this.dt["compare_args"]["imgArchivesPath"],
        browserDependent : this.dt["compare_args"]["browserDependent"],
        realtime : this.dt["compare_args"]["realtime"],
        uiObjSnap : this.dt["compare_args"]["uiObjSnap"],
        maskRegion : this.dt["compare_args"]["maskRegion"],
        maskRegionExcluding : this.dt["compare_args"]["maskRegionExcluding"],
        aspect_ratio_required : this.dt["compare_args"]["aspect_ratio_required"],
        intermediate_output : this.dt["compare_args"]["intermediate_output"],
        purge_old_artifacts : this.dt["compare_args"]["purge_old_artifacts"],
        failure_pattern_succession_density : this.dt["compare_args"]["result_pattern_analyzer"]["failure_pattern_succession_density"],
        p_hash_size : this.dt["compare_args"]["p_hash_parametric"]["hash_size"],
        d_hash_size : this.dt["compare_args"]["d_hash_parametric"]["hash_size"],
        BRISK_FLANN_bl_confirmed_variance_auto_update_disabled : this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_bl_confirmed_variance_auto_update(disabled)"],
        BRISK_FLANN_parametric_baseline : this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"],
        BRISK_FLANN_baseline_metrics_auto_update_disabled : this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_baseline_metrics_auto_update(disabled)"],
        BRISK_FLANN_gp_gpp_check_enabled : this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"],
        FLANNmatcher_accuracy : this.dt["compare_args"]["BRISK_FLANN_parametric"]["FLANNmatcher_accuracy"],
        

        
        method1 : this.dt["compare_args"]["similarity"][0]["method1"],
        m1_score : this.dt["compare_args"]["similarity"][0]["m1_score"],
        m1_match_operator: this.dt["compare_args"]["similarity"][0]["m1_match_operator"],
        m1_powered_on : this.dt["compare_args"]["similarity"][0]["m1_powered_on"],
        m1_eval_groupID : this.dt["compare_args"]["similarity"][0]["m1_eval_groupID"],
        group_eval_operator : this.dt["compare_args"]["similarity"][0]["group_eval_operator"],
        method2 : this.dt["compare_args"]["similarity"][1]["method2"],
        m2_score : this.dt["compare_args"]["similarity"][1]["m2_score"],
        m2_match_operator : this.dt["compare_args"]["similarity"][1]["m2_match_operator"],
        m2_powered_on : this.dt["compare_args"]["similarity"][1]["m2_powered_on"],
        m2_eval_groupID : this.dt["compare_args"]["similarity"][1]["m2_eval_groupID"],
        method3 : this.dt["compare_args"]["similarity"][2]["method3"],
        m3_score : this.dt["compare_args"]["similarity"][2]["m3_score"],
        m3_match_operator : this.dt["compare_args"]["similarity"][2]["m3_match_operator"],
        m3_powered_on : this.dt["compare_args"]["similarity"][2]["m3_powered_on"],
        m3_eval_groupID : this.dt["compare_args"]["similarity"][2]["m3_eval_groupID"],


        // this.hang_issue_ResultPath=this.dt["compare_args"]["hang_issue_ResultPath"]
        // this.imgCompResultPath=this.dt["compare_args"]["imgCompResultPath"]
        // this.imgInteractionResultPath=this.dt["compare_args"]["imgInteractionResultPath"]            
        //this.hang_issue_checker_frequency=this.dt["compare_args"]["hang_issue_checker"]["check_frequency_min"]     
        }
        this.result_pattern_analyzer.failure_pattern_succession_density = di_py.failure_pattern_succession_density
        this.p_hash_parametric.hash_size = di_py.p_hash_size
        this.d_hash_parametric.hash_size = di_py.d_hash_size
        this.BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = di_py.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled
        this.BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = di_py.BRISK_FLANN_parametric_baseline
        this.BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = di_py.BRISK_FLANN_baseline_metrics_auto_update_disabled
        this.BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = di_py.BRISK_FLANN_gp_gpp_check_enabled
        this.BRISK_FLANN_parametric.FLANNmatcher_accuracy = di_py.FLANNmatcher_accuracy

        this.similarity.method1 = di_py.method1
        this.similarity.m1_score = di_py.m1_score
        this.similarity.m1_match_operator = di_py.m1_match_operator
        this.similarity.m1_powered_on = di_py.m1_powered_on
        this.similarity.m1_eval_groupID = di_py.m1_eval_groupID
        this.similarity.group_eval_operator = di_py.group_eval_operator
        
        this.similarity.method2 = di_py.method2
        this.similarity.m2_score = di_py.m2_score
        this.similarity.m2_match_operator = di_py.m2_match_operator
        this.similarity.m2_powered_on = di_py.m2_powered_on
        this.similarity.m2_eval_groupID = di_py.m2_eval_groupID

        this.similarity.method3 = di_py.method3
        this.similarity.m3_score = di_py.m3_score
        this.similarity.m3_match_operator = di_py.m3_match_operator
        this.similarity.m3_powered_on = di_py.m3_powered_on
        this.similarity.m3_eval_groupID = di_py.m3_eval_groupID
        return di_py

    }

    public get p_hash_parametric():p_hash_parametric{
        if(this._p_hash_parametric == null || this._p_hash_parametric == undefined){
            this._p_hash_parametric = new p_hash_parametric()
        }
        console.log("this._p_hash_parametric.hash_size:",this._p_hash_parametric.hash_size)
        return this._p_hash_parametric
    }

    public set p_hash_parametric(paramValue:p_hash_parametric){
        if(this._p_hash_parametric == null || this._p_hash_parametric == undefined){
            this._p_hash_parametric = new p_hash_parametric()
        }
        if(paramValue.hash_size.length > 0)
            this._p_hash_parametric.hash_size = paramValue.hash_size
        else
            this._p_hash_parametric.hash_size = "8"
        console.log("this._p_hash_parametric.hash_size:",this._p_hash_parametric.hash_size)
        //return this._p_hash_parametric
    }

    public get d_hash_parametric():d_hash_parametric{
        if(this._d_hash_parametric == null || this._d_hash_parametric == undefined){
            this._d_hash_parametric = new d_hash_parametric()
        }
        return this._d_hash_parametric
    }

    public set d_hash_parametric(paramValue:d_hash_parametric){
        if(this._d_hash_parametric == null || this._d_hash_parametric == undefined){
            this._d_hash_parametric = new d_hash_parametric()
        }
        if(paramValue.hash_size.length > 0)
            this._d_hash_parametric.hash_size = paramValue.hash_size
        else
            this._d_hash_parametric.hash_size = "8"
    }

    public get result_pattern_analyzer():result_pattern_analyzer{
        if(this._result_pattern_analyzer == null || this._result_pattern_analyzer == undefined){
            this._result_pattern_analyzer = new result_pattern_analyzer()
        }
        console.log("getter--this._result_pattern_analyzer.failure_pattern_succession_density:",this._result_pattern_analyzer.failure_pattern_succession_density)
        return this._result_pattern_analyzer
    }

    public set result_pattern_analyzer(paramValue:result_pattern_analyzer){
        if(this._result_pattern_analyzer == null || this._result_pattern_analyzer == undefined){
            this._result_pattern_analyzer = new result_pattern_analyzer()
        }
        if(paramValue.failure_pattern_succession_density.length > 0)
            this._result_pattern_analyzer.failure_pattern_succession_density = paramValue.failure_pattern_succession_density
        else
            this._result_pattern_analyzer.failure_pattern_succession_density = "0"
        console.log("setter---this._result_pattern_analyzer.failure_pattern_succession_density:",this._result_pattern_analyzer.failure_pattern_succession_density)
    }

    public get BRISK_FLANN_parametric():BRISK_FLANN_parametric{
        if(this._BRISK_FLANN_parametric == null || this._BRISK_FLANN_parametric == undefined){
            this._BRISK_FLANN_parametric =  new BRISK_FLANN_parametric()
        }
/*      this._BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = "true"
        this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = path.join(browser.params.baseDir,"./src/test-inputs/imagevision/data/baseline/briskflann_baseline.json")
        this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = "true"
        this._BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = "true"
        this._BRISK_FLANN_parametric.FLANNmatcher_accuracy = "0.5"*/
        console.log("this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline:",this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline)
        return this._BRISK_FLANN_parametric
    }

    public set BRISK_FLANN_parametric(paramValue:BRISK_FLANN_parametric){
        if(this._BRISK_FLANN_parametric == null || this._BRISK_FLANN_parametric == undefined){
            this._BRISK_FLANN_parametric =  new BRISK_FLANN_parametric()
        }
        if(paramValue.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled !== "")
            this._BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = paramValue.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled
        else
            this._BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = "false"
    
        if(paramValue.BRISK_FLANN_parametric_baseline !== "")
            this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = paramValue.BRISK_FLANN_parametric_baseline
        else
            this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = path.join(browser.params.baseDir,"./src/test-inputs/imagevision/data/baseline/briskflann_baseline.json")

        if(paramValue.BRISK_FLANN_baseline_metrics_auto_update_disabled !== "")
           this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = paramValue.BRISK_FLANN_baseline_metrics_auto_update_disabled
        else
           this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = "false"
        
        if(paramValue.BRISK_FLANN_gp_gpp_check_enabled !== "")
           this._BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = paramValue.BRISK_FLANN_gp_gpp_check_enabled
        else
           this._BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = "false"
        
        if(paramValue.FLANNmatcher_accuracy !== "")
           this._BRISK_FLANN_parametric.FLANNmatcher_accuracy = paramValue.FLANNmatcher_accuracy
        else
           this._BRISK_FLANN_parametric.FLANNmatcher_accuracy = "0.5"

        console.log("this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline:",this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline)
    }


 /*  public get realtime():string{
       return this._realtime
   }
   public set realtime(paramValue:string){
       this._realtime = paramValue
   } */

    public get similarity():similarity{
        if(this._similarity == null || this._similarity == undefined){
            this._similarity = new similarity()
        }
        return this._similarity
    }

    public set similarity(paramValue:similarity){
        if(this._similarity == null || this._similarity == undefined){
            this._similarity = new similarity()
        }
        if(paramValue.method1 != "")
            this._similarity.method1 = paramValue.method1
        else
            this._similarity.method1 = "SSI"
        
        if(paramValue.m1_score != "")
            this._similarity.m1_score = paramValue.m1_score
        else
            this._similarity.m1_score = "1"
        
        if(paramValue.m1_match_operator != "")
            this._similarity.m1_match_operator = paramValue.m1_match_operator
        else
            this._similarity.m1_match_operator = "and"

        if(paramValue.m1_powered_on != "")
            this._similarity.m1_powered_on = paramValue.m1_powered_on
        else
            this._similarity.m1_powered_on = "1"

        if(paramValue.m1_eval_groupID != "")
            this._similarity.m1_eval_groupID = paramValue.m1_eval_groupID
        else
            this._similarity.m1_eval_groupID = "1"

        if(paramValue.method2 != "")
            this._similarity.method2 = paramValue.method2
        else
            this._similarity.method2 = "perceptual_hashing"
        
        if(paramValue.m2_score != "")
            this._similarity.m2_score = paramValue.m2_score
        else 
            this._similarity.m2_score = "0"
        
        if(paramValue.m2_match_operator != "")
             this._similarity.m2_match_operator = paramValue.m2_match_operator
        else
            this._similarity.m2_match_operator = "and"

        if(paramValue.m2_powered_on != "")    
            this._similarity.m2_powered_on = paramValue.m2_powered_on
        else
            this._similarity.m2_powered_on = "1"
        
        if(paramValue.m2_eval_groupID != "")
            this._similarity.m2_eval_groupID = paramValue.m2_eval_groupID
        else
            this._similarity.m2_eval_groupID = "1"

        if(paramValue.method3 != "")
             this._similarity.method3 = paramValue.method3
        else
             this._similarity.method3 = "BRISK-FLANN"
        
        if(paramValue.m3_score != "")
             this._similarity.m3_score = paramValue.m3_score
        else
             this._similarity.m3_score = "0"
            
        if(paramValue.m3_match_operator != "")
             this._similarity.m3_match_operator = paramValue.m3_match_operator
        else 
             this._similarity.m3_match_operator = "and"
        
        if(paramValue.m3_powered_on != "")
             this._similarity.m3_powered_on = paramValue.m3_powered_on
        else
             this._similarity.m3_powered_on = "1"
        
        if(paramValue.m3_eval_groupID != "")
            this._similarity.m3_eval_groupID = paramValue.m3_eval_groupID
        else
            this._similarity.m3_eval_groupID = "2"

        if(paramValue.group_eval_operator != "")
            this._similarity.group_eval_operator = paramValue.group_eval_operator
        else
            this._similarity.group_eval_operator = "or"
    }


 
    private argFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/img-comp-args.json")
    //private dt = require(this.argFile)
    private dt = JSON.parse(fs.readFileSync(this.argFile, 'utf-8'))
    private _appFeatures_CV = ""
    private _baselineImage = ""
    private _runtime_img = ""
    //private _diff_img_path = ""
    private _comp_reports_path = ""
    private _net_result_path = ""
    private _imgArchivesPath = ""
    private _browserDependent = "true"
    private _realtime = ""
    private _uiObjSnap = ""
    private _maskRegion = ""
    private _maskRegionExcluding=""
    private _aspect_ratio_required=""
    private _intermediate_output=""
    private _purge_old_artifacts=""
    private _p_hash_parametric:p_hash_parametric = null
    private _d_hash_parametric:d_hash_parametric = null
    private _BRISK_FLANN_parametric:BRISK_FLANN_parametric = null
    private _result_pattern_analyzer:result_pattern_analyzer = null
    private _similarity:similarity = null
    
    appFeatures_CV = ""
    baselineImage = ""
    runtime_img = ""
    comp_reports_path = ""
    net_result_path = ""
    imgArchivesPath = ""
    uiObjSnap = ""
    browserDependent = ""
    realtime = ""
    maskRegion = ""
    maskRegionExcluding=""
    aspect_ratio_required=""
    intermediate_output=""
    purge_old_artifacts=""
}



export interface IpyImgCompLib {
    appFeatures_CV : string
    baselineImage : string
    runtime_img : string
    comp_reports_path : string
    net_result_path : string
    imgArchivesPath : string
    browserDependent : string
    realtime : string
    uiObjSnap : string
    maskRegion : string
    maskRegionExcluding : string
    aspect_ratio_required : string
    intermediate_output : string
    purge_old_artifacts : string
    p_hash_size : string
    d_hash_size : string
    failure_pattern_succession_density : string
    BRISK_FLANN_bl_confirmed_variance_auto_update_disabled : string
    BRISK_FLANN_parametric_baseline : string
    BRISK_FLANN_baseline_metrics_auto_update_disabled : string
    BRISK_FLANN_gp_gpp_check_enabled : string
    FLANNmatcher_accuracy : string
    method1 : string
    m1_score : string
    m1_match_operator : string
    m1_powered_on : string
    m1_eval_groupID : string
    method2 : string
    m2_score : string
    m2_match_operator : string
    m2_powered_on:string
    m2_eval_groupID : string
    method3 : string
    m3_score : string
    m3_match_operator : string
    m3_powered_on:string
    m3_eval_groupID : string
    group_eval_operator : string
}

export class p_hash_parametric{
    public hash_size:string
}

export class d_hash_parametric{
    public hash_size:string
}

export class result_pattern_analyzer{
    public failure_pattern_succession_density:string
}

export class BRISK_FLANN_parametric{
    public BRISK_FLANN_bl_confirmed_variance_auto_update_disabled:string
    public BRISK_FLANN_parametric_baseline:string
    public BRISK_FLANN_baseline_metrics_auto_update_disabled:string
    public BRISK_FLANN_gp_gpp_check_enabled:string
    public FLANNmatcher_accuracy:string
}

export class similarity{
    method1 = ""
    m1_score = ""
    m1_match_operator = ""
    m1_powered_on=""
    m1_eval_groupID = ""
    method2 = ""
    m2_score = ""
    m2_match_operator = ""
    m2_powered_on=""
    m2_eval_groupID = ""
    method3 = ""
    m3_score = ""
    m3_match_operator = ""
    m3_powered_on=""
    m3_eval_groupID = ""
    group_eval_operator = ""
}


    /* setDefault() {
        this.appFeatures_CV = this._appFeatures_CV
        this.baselineImage = this._baselineImage
        this.runtime_img = this._runtime_img
        this.comp_reports_path = this._comp_reports_path
        this.net_result_path = this._net_result_path
        this.imgArchivesPath = this._imgArchivesPath
        this.browserDependent = this._browserDependent
        this.realtime = this._realtime
        this.uiObjSnap = this._uiObjSnap
        this.maskRegion = this._maskRegion
        this.maskRegionExcluding = this._maskRegionExcluding
        this.aspect_ratio_required = this._aspect_ratio_required
        this.intermediate_output = this._intermediate_output
        this.purge_old_artifacts = this._purge_old_artifacts
        this.result_pattern_analyzer.failure_pattern_succession_density = this._result_pattern_analyzer.failure_pattern_succession_density
        this.p_hash_parametric.hash_size = this._p_hash_parametric.hash_size
        this.d_hash_parametric.hash_size = this._d_hash_parametric.hash_size
        // this.hang_issue_ResultPath=this.hang_issue_ResultPath
	    // this.imgCompResultPath=this.imgCompResultPath
	    // this.imgInteractionResultPath=this.imgInteractionResultPath
        //this.hang_issue_checker_frequency=this.hang_issue_checker_frequency        
        this.BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled = this._BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled
        this.BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline
        this.BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled
        this.BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = this._BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled
        this.BRISK_FLANN_parametric.FLANNmatcher_accuracy = this._BRISK_FLANN_parametric.FLANNmatcher_accuracy

        this.similarity.method1 = this._similarity.method1
        this.similarity.m1_score = this._similarity.m1_score
        this.similarity.m1_match_operator = this._similarity.m1_match_operator
        this.similarity.m1_powered_on=this._similarity.m1_powered_on
        this.similarity.m1_eval_groupID = this._similarity.m1_eval_groupID
        this.similarity.group_eval_operator = this._similarity.group_eval_operator
        
        this.similarity.method2 = this._similarity.method2
        this.similarity.m2_score = this._similarity.m2_score
        this.similarity.m2_match_operator = this._similarity.m2_match_operator
        this.similarity.m2_powered_on=this._similarity.m2_powered_on
        this.similarity.m2_eval_groupID = this._similarity.m2_eval_groupID

        this.similarity.method3 = this._similarity.method3
        this.similarity.m3_score = this._similarity.m3_score
        this.similarity.m3_match_operator = this._similarity.m3_match_operator
        this.similarity.m3_powered_on=this._similarity.m3_powered_on
        this.similarity.m3_eval_groupID = this._similarity.m3_eval_groupID
        pathRefs.runtimeImgPath = ""
        pathRefs.runtime_img = ""
        pathRefs.baselineImgPath = ""
        pathRefs.reportsPath = ""
        pathRefs.resultPath = ""
    } */

    /*getValues():IpyImgCompLib{
        let fname_arr = this.dt["args"][0]["imgFile"].split('/')
        let fname = fname_arr[fname_arr.length-1]
        let di_py = {
            appFeatures_CV: this.dt["args"][0]["appFeatures_CV"],
            imgFile: path.join(browser.params.imgArchivesPath, fname),
            
        }
        return di_py
    }*/



/******************Temporary-experimental code************************

    /*static get imgFile1():string {
        console.log("argList - JSON object:",this.dt)
        let fname = this.dt["args"][0]["imgFile"].split('/').last()
        console.log(path.join(browser.params.imgArchivesPath,fname))
        return path.join(browser.params.imgArchivesPath,fname)
    }

    static set imgFile2(abc:string) {
        console.log("argList - JSON object:",this.dt)
        let fname = this.dt["args"][0]["imgFile"].split('/').last()
        console.log(path.join(browser.params.imgArchivesPath,fname))
        //return path.join(browser.params.imgArchivesPath,fname)
    }

    get cycles():string {
        let cycles = this.dt["args"][0]["cycles"]
        console.log("cycles",cycles)
        return cycles
    }

    get realtimeImgGrabDurationMins():string {
        let duration = this.dt["args"][0]["realtimeImgGrabDurationMins"]
        console.log("cycles",duration)
        return duration
    }

    get interval():string {
        let cycles = this.dt["args"][0]["cycles"]
        console.log("cycles",cycles)
        return cycles
    }

    constructor(){
        if (this._baselineImage == "") {
            this._appFeatures_CV = this.dt["compare_args"]["appFeatures_CV"]
            this._baselineImage = this.dt["compare_args"]["baselineImage"]
            this._runtime_img = this.dt["compare_args"]["runtime_img"]
            this._comp_reports_path = this.dt["compare_args"]["comp_reports_path"]
            this._net_result_path = this.dt["compare_args"]["net_result_path"]
            this._img_ops_session_rootpath = this.dt["compare_args"]["img_ops_session_rootpath"]
            this._browserDependent = this.dt["compare_args"]["browserDependent"]
            this._realtime = this.dt["compare_args"]["realtime"]
            this._maskRegion = this.dt["compare_args"]["maskRegion"]
            this._maskRegionExcluding= this.dt["compare_args"]["maskRegionExcluding"]
            this._aspect_ratio_required=this.dt["compare_args"]["aspect_ratio_required"]
            this._intermediate_output=this.dt["compare_args"]["intermediate_output"]
            this._purge_old_artifacts=this.dt["compare_args"]["purge_old_artifacts"]
            this._result_pattern_analyzer.failure_pattern_succession_density = this.dt["compare_args"]["result_pattern_analyzer"]["failure_pattern_succession_density"]
            this._p_hash_parametric.hash_size = this.dt["compare_args"]["p_hash_parametric"]["hash_size"]
            this._d_hash_parametric.hash_size = this.dt["compare_args"]["d_hash_parametric"]["hash_size"]
            this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_bl_confirmed_variance_auto_update(disabled)"]
            this._BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline = this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"]
            this._BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled = this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_baseline_metrics_auto_update(disabled)"]
            this._BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled = this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"]
            this._BRISK_FLANN_parametric.FLANNmatcher_accuracy = this.dt["compare_args"]["BRISK_FLANN_parametric"]["FLANNmatcher_accuracy"]
    
           
            this._similarity.method1 = this.dt["compare_args"]["similarity"][0]["method1"]
            this._similarity.m1_score = this.dt["compare_args"]["similarity"][0]["m1_score"]
            this._similarity.m1_match_operator= this.dt["compare_args"]["similarity"][0]["m1_match_operator"]
            this._similarity.m1_powered_on=this.dt["compare_args"]["similarity"][0]["m1_powered_on"]
            this._similarity.m1_eval_groupID = this.dt["compare_args"]["similarity"][0]["m1_eval_groupID"]
            this._similarity.group_eval_operator = this.dt["compare_args"]["similarity"][0]["group_eval_operator"]
            this._similarity.method2 = this.dt["compare_args"]["similarity"][1]["method2"]
            this._similarity.m2_score = this.dt["compare_args"]["similarity"][1]["m2_score"]
            this._similarity.m2_match_operator= this.dt["compare_args"]["similarity"][1]["m2_match_operator"]
            this._similarity.m2_powered_on=this.dt["compare_args"]["similarity"][1]["m2_powered_on"]
            this._similarity.m2_eval_groupID = this.dt["compare_args"]["similarity"][1]["m2_eval_groupID"]
            this._similarity.method3 = this.dt["compare_args"]["similarity"][2]["method3"]
            this._similarity.m3_score = this.dt["compare_args"]["similarity"][2]["m3_score"]
            this._similarity.m3_match_operator= this.dt["compare_args"]["similarity"][2]["m3_match_operator"]
            this._similarity.m3_powered_on=this.dt["compare_args"]["similarity"][2]["m3_powered_on"]
            this._similarity.m3_eval_groupID = this.dt["compare_args"]["similarity"][2]["m3_eval_groupID"]
    
    
            this.appFeatures_CV = this.dt["compare_args"]["appFeatures_CV"]
            this.baselineImage = this.dt["compare_args"]["baselineImage"]
            this.runtime_img = this.dt["compare_args"]["runtime_img"]
            this.comp_reports_path = this.dt["compare_args"]["comp_reports_path"]
            this.net_result_path = this.dt["compare_args"]["net_result_path"]
            this.img_ops_session_rootpath = this.dt["compare_args"]["img_ops_session_rootpath"]
    
            //this.diff_img_path = this.dt["compare_args"]["diff_img_path"]
            this.browserDependent = this.dt["compare_args"]["browserDependent"]
            this.realtime = this.dt["compare_args"]["realtime"]
            this.maskRegion = this.dt["compare_args"]["maskRegion"]
            this.maskRegionExcluding= this.dt["compare_args"]["maskRegionExcluding"]
            this.aspect_ratio_required=this.dt["compare_args"]["aspect_ratio_required"]
            this.intermediate_output=this.dt["compare_args"]["intermediate_output"]
            this.purge_old_artifacts=this.dt["compare_args"]["purge_old_artifacts"]
            this.result_pattern_analyzer.failure_pattern_succession_density = this.dt["compare_args"]["result_pattern_analyzer"]["failure_pattern_succession_density"]
            this.p_hash_parametric.hash_size=this.dt["compare_args"]["p_hash_parametric"]["hash_size"]
            this.d_hash_parametric.hash_size=this.dt["compare_args"]["d_hash_parametric"]["hash_size"]
            // this.hang_issue_ResultPath=this.dt["compare_args"]["hang_issue_ResultPath"]
            // this.imgCompResultPath=this.dt["compare_args"]["imgCompResultPath"]
            // this.imgInteractionResultPath=this.dt["compare_args"]["imgInteractionResultPath"]            
            //this.hang_issue_checker_frequency=this.dt["compare_args"]["hang_issue_checker"]["check_frequency_min"]     
            this.BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled=this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_bl_confirmed_variance_auto_update(disabled)"]
            this.BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline=this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"]
            this.BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled=this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_baseline_metrics_auto_update(disabled)"]
            this.BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled=this.dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"]
            this.BRISK_FLANN_parametric.FLANNmatcher_accuracy=this.dt["compare_args"]["BRISK_FLANN_parametric"]["FLANNmatcher_accuracy)"]
            
            this.similarity.method1 = this.dt["compare_args"]["similarity"][0]["method1"]
            this.similarity.m1_score = this.dt["compare_args"]["similarity"][0]["m1_score"]
            this.similarity.m1_match_operator= this.dt["compare_args"]["similarity"][0]["m1_match_operator"]
            this.similarity.m1_powered_on=this.dt["compare_args"]["similarity"][0]["m1_powered_on"]
            this.similarity.m1_eval_groupID = this.dt["compare_args"]["similarity"][0]["m1_eval_groupID"]
            this.similarity.group_eval_operator= this.dt["compare_args"]["similarity"][0]["group_eval_operator"]
            this.similarity.method2 = this.dt["compare_args"]["similarity"][1]["method2"]
            this.similarity.m2_score = this.dt["compare_args"]["similarity"][1]["m2_score"]
            this.similarity.m2_match_operator= this.dt["compare_args"]["similarity"][1]["m2_match_operator"]
            this.similarity.m2_powered_on=this.dt["compare_args"]["similarity"][1]["m2_powered_on"]
            this.similarity.m2_eval_groupID = this.dt["compare_args"]["similarity"][1]["m2_eval_groupID"]
            this.similarity.method3 = this.dt["compare_args"]["similarity"][2]["method3"]
            this.similarity.m3_score = this.dt["compare_args"]["similarity"][2]["m3_score"]
            this.similarity.m3_match_operator= this.dt["compare_args"]["similarity"][2]["m3_match_operator"]
            this.similarity.m3_powered_on=this.dt["compare_args"]["similarity"][2]["m3_powered_on"]            
            this.similarity.m3_eval_groupID = this.dt["compare_args"]["similarity"][2]["m3_eval_groupID"]
    

         
            // this._hang_issue_ResultPath=this.dt["compare_args"]["hang_issue_ResultPath"]
            // this._imgCompResultPath=this.dt["compare_args"]["imgCompResultPath"]
            // this._imgInteractionResultPath=this.dt["compare_args"]["imgInteractionResultPath"]
           // this._hang_issue_checker_frequency=this.dt["compare_args"]["hang_issue_checker"]["check_frequency_min"]           

            this._method4 = this.dt["compare_args"]["similarity"][0]["method4"]
            this._m4_score = this.dt["compare_args"]["similarity"][0]["m4_score"]
            this._m4_match_operator= this.dt["compare_args"]["similarity"][0]["m4_match_operator"]
            this._m4_powered_on=this.dt["compare_args"]["similarity"][0]["m4_powered_on"]
            this._m4_eval_groupID = this.dt["compare_args"]["similarity"][0]["m4_eval_groupID"]
            this._method5 = this.dt["compare_args"]["similarity"][0]["method5"]
            this._m5_score = this.dt["compare_args"]["similarity"][0]["m5_score"]
            this._m5_match_operator= this.dt["compare_args"]["similarity"][0]["m5_match_operator"]
            this._m5_powered_on=this.dt["compare_args"]["similarity"][0]["m5_powered_on"]
            this._m5_eval_groupID = this.dt["compare_args"]["similarity"][0]["m5_eval_groupID"]
            this._method6 = this.dt["compare_args"]["similarity"][0]["method6"]
            this._m6_score = this.dt["compare_args"]["similarity"][0]["m6_score"]
            //private fname = this.dt["args"][0]["imgFile"].split('/').last()

            this.method4 = this.dt["compare_args"]["similarity"][0]["method4"]
            this.m4_score = this.dt["compare_args"]["similarity"][0]["m4_score"]
            this.m4_match_operator= this.dt["compare_args"]["similarity"][0]["m4_match_operator"]
            this.m4_powered_on=this.dt["compare_args"]["similarity"][0]["m4_powered_on"]
            this.m4_eval_groupID = this.dt["compare_args"]["similarity"][0]["m4_eval_groupID"]
            this.method5 = this.dt["compare_args"]["similarity"][0]["method5"]
            this.m5_score = this.dt["compare_args"]["similarity"][0]["m5_score"]
            this.m5_match_operator= this.dt["compare_args"]["similarity"][0]["m5_match_operator"]
            this.m5_powered_on=this.dt["compare_args"]["similarity"][0]["m5_powered_on"]
            this.m5_eval_groupID = this.dt["compare_args"]["similarity"][0]["m5_eval_groupID"]
            this.method6 = this.dt["compare_args"]["similarity"][0]["method6"]
            this.m6_score = this.dt["compare_args"]["similarity"][0]["m6_score"]



            //method1 = ""
    //m1_score = ""
    //m1_match_operator = ""
    //m1_powered_on=""
    //m1_eval_groupID = ""
    //group_eval_operator = ""
    
    //method2 = ""
    //m2_score = ""
    //m2_match_operator = ""
    //m2_powered_on=""
    //m2_eval_groupID = ""
    //method3 = ""
    //m3_score = ""
    //m3_match_operator = ""
    //m3_powered_on=""
    //m3_eval_groupID = ""
    /*method4 = ""
    m4_score = ""
    m4_match_operator = ""
    m4_powered_on=""
    m4_eval_groupID = ""
    method5 = ""
    m5_score = ""
    m5_match_operator = ""
    m5_powered_on=""
    m5_eval_groupID = ""
    method6 = ""
    m6_score = ""

        this.method4 = this._method4
        this.m4_score = this._m4_score
        this.m4_match_operator = this.m4_match_operator
        this.m4_powered_on=this.m4_powered_on
        this.m4_eval_groupID = this.m4_eval_groupID
        this.method5 = this._method5
        this.m5_score = this._m5_score
        this.m5_match_operator = this.m5_match_operator
        this.m5_powered_on=this.m5_powered_on
        this.m5_eval_groupID = this.m5_eval_groupID
        this.method6 = this._method6
        this.m6_score = this._m6_score


            //private _p_hash_size=""
    //private _d_hash_size=""
    // private _hang_issue_ResultPath=""
	// private	_imgCompResultPath=""
	// private	_imgInteractionResultPath=""
    //private _hang_issue_checker_frequency=""

/*    private _method1 = ""
    private _m1_score = ""
    private _m1_match_operator = ""
    private _m1_powered_on=""
    private _group_eval_operator = ""
    private _m1_eval_groupID = ""
    private _method2 = ""
    private _m2_score = ""
    private _m2_match_operator = ""
    private _m2_powered_on=""
    private _m2_eval_groupID = ""
    private _method3 = ""
    private _m3_score = ""
    private _m3_match_operator = ""
    private _m3_powered_on=""
    private _m3_eval_groupID = "" */

    /*private _method4 = ""
    private _m4_score = ""
    private _m4_match_operator = ""
    private _m4_powered_on=""
    private _m4_eval_groupID = ""
    private _method5 = ""
    private _m5_score = ""
    private _m5_match_operator = ""
    private _m5_powered_on=""
    private _m5_eval_groupID = ""
    private _method6 = ""
    private _m6_score = ""
    //private fname = this.dt["args"][0]["imgFile"].split('/').last()


******************************************************************/
