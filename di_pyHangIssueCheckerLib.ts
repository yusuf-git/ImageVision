/***************************************************
* Author : Yusuf
* Authored on : 21-Dec-2021 10:30 AM
* Updates on  : 21-Dec-2021 03:20 PM
* Depdendency Injection for py CV hang issue checker
*****************************************************/

import * as fse from 'fs-extra'
import { browser, by, protractor, ExpectedConditions } from "protractor"
import * as path from "path"
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework"
import * as cp from 'child_process'
//import {PythonShell} from 'python-shell'
import * as fs from 'fs'
import { fs_helper as fsh, fs_helper } from "../helpers/fs_helper"
import { async } from 'q'
import { AppFeatures_CV } from "./appfeatures_cv"
import { pathRefs } from './pathRefs'

export class di_pyHangIssueCheckerLib {

    constructor() {
        this.setDefault()
    }
   

    setDefault() {
        this.appFeatures_CV = ""
        this.runtime_img_path = ""
        this.hang_issue_reports_path = ""
        this.net_result_path = ""
        this.realtime = "false"
        this.maskRegion = ""
        this.maskRegionExcluding = ""
        this.aspect_ratio_required = "true"
        this.intermediate_output = "false"
        this.imgcap = "5000"
        this.purge_old_reports = "false"
        this.p_hash_parametric.hash_size = "8"
        this.hang_issue_checker.check_frequency_min = "1"
        // this.hang_issue_ResultPath=this.hang_issue_ResultPath
	    // this.imgCompResultPath=this.imgCompResultPath
	    // this.imgInteractionResultPath=this.imgInteractionResultPath
        //this.hang_issue_checker_frequency=this.hang_issue_checker_frequency        

        this.similarity.method1 = "SSI"
        this.similarity.m1_score = "0.95"
                
        this.similarity.method2 = "perceptual_hashing"
        this.similarity.m2_score = "1"

        pathRefs.hangIssueChecker_RuntimePath = ""
        pathRefs.hangIssueChecker_ReportsPath = ""
        pathRefs.hangIssueChecker_ResultsPath = ""
    }

    public getCurrentConfigs():IpyHangIssueChecker{
        let di_py = {
        appFeatures_CV : this.dt["compare_args"]["appFeatures_CV"],
        runtime_img_path : this.dt["compare_args"]["runtime_img_path"],
        hang_issue_reports_path : this.dt["compare_args"]["hang_issue_reports_path"],
        net_result_path : this.dt["compare_args"]["net_result_path"],
        realtime : this.dt["compare_args"]["realtime"],
        maskRegion : this.dt["compare_args"]["maskRegion"],
        maskRegionExcluding : this.dt["compare_args"]["maskRegionExcluding"],
        aspect_ratio_required : this.dt["compare_args"]["aspect_ratio_required"],
        intermediate_output : this.dt["compare_args"]["intermediate_output"],
        purge_old_reports : this.dt["compare_args"]["purge_old_artifacts"],
        imgcap : this.dt["compare_args"]["imgcap"],
        hang_issue_checker_freq_min : this.dt["compare_args"]["hang_issue_checker"]["check_frequency_min"],
        p_hash_size : this.dt["compare_args"]["p_hash_parametric"]["hash_size"],
      
        method1 : this.dt["compare_args"]["similarity"][0]["method1"],
        m1_score : this.dt["compare_args"]["similarity"][0]["m1_score"],
        method2 : this.dt["compare_args"]["similarity"][1]["method2"],
        m2_score : this.dt["compare_args"]["similarity"][1]["m2_score"],


        // this.hang_issue_ResultPath=this.dt["compare_args"]["hang_issue_ResultPath"]
        // this.imgCompResultPath=this.dt["compare_args"]["imgCompResultPath"]
        // this.imgInteractionResultPath=this.dt["compare_args"]["imgInteractionResultPath"]            
        //this.hang_issue_checker_frequency=this.dt["compare_args"]["hang_issue_checker"]["check_frequency_min"]     
        }
        this.p_hash_parametric.hash_size = di_py.p_hash_size
        this.hang_issue_checker.check_frequency_min = di_py.hang_issue_checker_freq_min

        this.similarity.method1 = di_py.method1
        this.similarity.m1_score = di_py.m1_score
        
        this.similarity.method2 = di_py.method2
        this.similarity.m2_score = di_py.m2_score

        return di_py

    }

    public get p_hash_parametric():p_hash_parametric{
        if(this._p_hash_parametric == null || this._p_hash_parametric == undefined){
            this._p_hash_parametric = new p_hash_parametric()
        }
        console.log("this._p_hash_parametric.hash_size:",this._p_hash_parametric.hash_size)
        return this._p_hash_parametric
    }


    public get hang_issue_checker():hang_issue_checker {
        if(this._hang_issue_checker == null || this._hang_issue_checker == undefined){
            this._hang_issue_checker = new hang_issue_checker()
        }
        return this._hang_issue_checker
    }

    public get similarity():similarity{
        if(this._similarity == null || this._similarity == undefined){
            this._similarity = new similarity()
        }
        return this._similarity
    }

 /*  public get realtime():string{
       return this._realtime
   }
   public set realtime(paramValue:string){
       this._realtime = paramValue
   } */

 
    private argFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/hang_issue_checker.json")
    //private dt = require(this.argFile)
    private dt = JSON.parse(fs.readFileSync(this.argFile, 'utf-8'))
    private _appFeatures_CV = ""
    private _runtime_img_path = ""
    private _hang_issue_reports_path = ""
    private _net_result_path = ""
    private _realtime = ""
    private _maskRegion = ""
    private _maskRegionExcluding=""
    private _aspect_ratio_required=""
    private _intermediate_output=""
    private _purge_old_reports=""
    private _imgcap = ""
    private _p_hash_parametric:p_hash_parametric = null
    private _hang_issue_checker:hang_issue_checker = null
    private _similarity:similarity = null
    
    appFeatures_CV = ""
    runtime_img_path = ""
    hang_issue_reports_path = ""
    net_result_path = ""
    realtime = ""
    maskRegion = ""
    maskRegionExcluding=""
    aspect_ratio_required=""
    intermediate_output=""
    purge_old_reports=""
    imgcap = ""
}



export interface IpyHangIssueChecker {
    appFeatures_CV : string
    runtime_img_path : string
    hang_issue_reports_path : string
    net_result_path : string
    realtime : string
    maskRegion : string
    maskRegionExcluding : string
    aspect_ratio_required : string
    intermediate_output : string
    purge_old_reports : string
    imgcap : string
    hang_issue_checker_freq_min : string   
    p_hash_size : string
    method1 : string
    m1_score : string
    method2 : string
    m2_score : string
}

export class p_hash_parametric{
    public hash_size:string
}

export class hang_issue_checker{
    public check_frequency_min:string
}

export class similarity{
    method1 = ""
    m1_score = ""
    method2 = ""
    m2_score = ""
}