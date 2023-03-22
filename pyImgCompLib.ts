/******************** 
* Author : Yusuf
* Authored on : 28-Jul-2020 10:00 PM
* Upates on   : 30-Jul-2020 06:00 PM, 06-Aug-2020 11:40 PM, 14-Dec-2020 08:45 PM, 03-Oct-2021 to 07-Oct-2021 01:30 AM, 14-Oct-2021 01:00 AM, 15-Oct-2021 01:00 AM, 16-Oct-2021 02:30 AM, 17-Oct-2021 02:30 AM, 18-Oct-2021 01:00 AM, 20-Nov-2021 11:30 AM To 11:50 PM, 22-Nov-2021 02:45 AM, 20-Dec-2021 06:45 PM
* Lib for capturing images with python CV library 
*
*********************/

/*future improvements(recorded on 20-Jul-2020 12:45 AM):
    - support for protractor parallelism while calling python img lib through cmd and static img-cap-args.json
    - create REST APIs for python img lib and call them
    - immediate - crop the specified portion of the captured image - for time scale real-time scenarios
*/

import * as fse from 'fs-extra';
import { ImageVisionRegistry as visionRegistry } from "../factory/ImageVisionRegistry";
import { browser, by, protractor, ExpectedConditions } from "protractor";
import * as path from "path";
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework";
import * as cp from 'child_process';
//import {PythonShell} from 'python-shell';
import * as fs from 'fs';
import { fs_helper as fsh, fs_helper } from "./../helpers//fs_helper"
import { async } from 'q';
import {di_pyImgCreativeLib} from "./di_pyImgCreativeLib"
import { di_pyImgCompLib } from "./di_pyImgCompLib"
import {pathRefs} from './pathRefs';
//import {pyCVLibrary} from "./pyCVLibrary"
import { helper } from "kognifai-automation-framework";

export class pyImgCompLib {
    private pathRefs = visionRegistry.pathRefs
    private di_pyImgCompLib = visionRegistry.di_pyImgCompLib
    private pyCVLibrary = visionRegistry.pyCVLib
    private tmp_path = ""
    private baselineImgPath = ""
    private runTimeImgPath = ""
    private diffImgPath = ""
    private pyCVLib = visionRegistry.pyCVLib
    private imageVision_ver = "ImageVision v6"

    public async pyCompareImages(di_pyImgCompLib: di_pyImgCompLib): Promise<boolean> {
        try {
            console.log("")
            console.log("")
            console.log("*******************************************************pyCompareImages OPERATION BEGINS*************************************************************************************")
            console.log("")
            console.log("")
            pathRefs.imgCompOpResult = false
            if(!this.checkImageGrabOpResult())
                return

            console.log("baseline img:",di_pyImgCompLib.baselineImage)
            console.log("runtime img:",di_pyImgCompLib.runtime_img)
            console.log("baseline img - pathRefs.baseline:",pathRefs.baseline_img)
            console.log("runtime img - pathRefs.runtime:",pathRefs.runtime_img)

            if(di_pyImgCompLib.baselineImage == null || di_pyImgCompLib.baselineImage == ""){
                di_pyImgCompLib.baselineImage = pathRefs.baseline_img
            }
            if(di_pyImgCompLib.runtime_img == undefined || di_pyImgCompLib.runtime_img == "")
               di_pyImgCompLib.runtime_img = pathRefs.runtime_img
            if(di_pyImgCompLib.net_result_path == null || di_pyImgCompLib.net_result_path == "")
                di_pyImgCompLib.net_result_path = path.dirname(di_pyImgCompLib.runtime_img)
            if(di_pyImgCompLib.comp_reports_path == null || di_pyImgCompLib.comp_reports_path == "")
                di_pyImgCompLib.comp_reports_path = path.dirname(di_pyImgCompLib.runtime_img)
            di_pyImgCompLib.imgArchivesPath = pathRefs.imgOpsSessionRootPath;

            let pyArgsJsonFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/img-comp-args.json")
            let pyImgBatFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/pyImgCompare.bat")
            let promptChangerBat = path.join(browser.params.baseDir, '..', "py/cv-img-grab/prompt.bat")

            let dt = this.unpackDI(di_pyImgCompLib, pyArgsJsonFile);
            let strData = JSON.stringify(dt);
            if(di_pyImgCompLib.intermediate_output == "true")
                console.log(strData)
            console.log("----------------------------------------------")
            await this.pyCVLibrary.writeToPyArgsFile(pyArgsJsonFile, strData, di_pyImgCompLib.intermediate_output);
            await this.pyCVLib.runPromptChanger(promptChangerBat);
            await this.pyCVLibrary.pyRun(pyImgBatFile, pyArgsJsonFile);
            console.log("----------------------------------------------")

            /* check the result file - if present, read it and set the test outcome accordingly */ 
            let result = this.getImgCompResult()
            console.log("image :"+ path.basename(di_pyImgCompLib.baselineImage)+" --> comparison operation result:"+result);
            di_pyImgCompLib.setDefault()
            console.log("reset the ImageComp configs to default....done")
            
            if(!result)
                expect("ImageVision | ImageComp : success").toEqual("ImageVision | ImageComp : failed","ImageVision --> ImageComp : Mismatch")

            /*Disable the comment on having a need to throw an error */
            /*let result1 = this.getImgCompRe0sult()*/
          
            console.log("")
            console.log("")
            console.log("*************************************END OF pyCompareImage OPERATION***********************************************************************************")
            return result
        }
        catch (err) {
            console.error("********************ImageVision error location : pyCompareImages()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("***************************************************************************************************")
            throw new Error(`ImageVision | ImageComp error : ${err.name}:${err.message}`)

        }
    }

    public async checkHangIssue(dt: any) {
        try {
            let pyArgsJsonFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/hang_issue_checker.json")
            let pyImgBatFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/hang_issue_checker.bat")
            let promptChangerBat = path.join(browser.params.baseDir, '..', "py/cv-img-grab/prompt.bat")
            let strData = JSON.stringify(dt);
            console.log("After update - strData(hang_issue_checker.json):", strData)
            console.log("pyArgsJsonFile:", pyArgsJsonFile)
            //await this.pyCVLibrary.writeToPyArgsFile(pyArgsJsonFile, strData);
            await this.pyCVLib.runPromptChanger(promptChangerBat);
            await this.pyCVLibrary.pyRun(pyImgBatFile, pyArgsJsonFile);
            console.log("HangIssueChecker executed");
            //  let hungissueResultFile = require(path.join(dt["compare_args"]["net_result_path"], "/hang_issue_result.json")); //handle this in page object file
            //  return this.getHangIssueResult(hungissueResultFile)
        }
        catch (err) {
            console.error("*******]*************ImageVision error location : checkHangIssue()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("***************************************************************************************************")
            throw new Error(`ImageVision | ImageComp error : ${err.name}:${err.message}`)
        }
    }


    private unpackDI(di_pyImgCompLib:di_pyImgCompLib, argFile) : di_pyImgCompLib | null
    {
        try
        {
            //let dt = require(argFile);
            let dt = JSON.parse(fs.readFileSync(argFile, 'utf-8'))
            dt["compare_args"]["appFeatures_CV"] = di_pyImgCompLib.appFeatures_CV;
            dt["compare_args"]["baselineImage"] = di_pyImgCompLib.baselineImage;
            dt["compare_args"]["runtime_img"] = di_pyImgCompLib.runtime_img;
            dt["compare_args"]["comp_reports_path"] = di_pyImgCompLib.comp_reports_path;
            dt["compare_args"]["net_result_path"] = di_pyImgCompLib.net_result_path;
            dt["compare_args"]["imgArchivesPath"] = di_pyImgCompLib.imgArchivesPath;
            dt["compare_args"]["browserDependent"] = di_pyImgCompLib.browserDependent;
            dt["compare_args"]["realtime"] = di_pyImgCompLib.realtime;
            dt["compare_args"]["uiObjSnap"] = di_pyImgCompLib.uiObjSnap;
            dt["compare_args"]["maskRegion"] = di_pyImgCompLib.maskRegion;
            dt["compare_args"]["maskRegionExcluding"] = di_pyImgCompLib.maskRegionExcluding;
            dt["compare_args"]["aspect_ratio_required"] = di_pyImgCompLib.aspect_ratio_required;
            dt["compare_args"]["intermediate_output"] = di_pyImgCompLib.intermediate_output;
            dt["compare_args"]["purge_old_artifacts"] = di_pyImgCompLib.purge_old_artifacts;
            dt["compare_args"]["result_pattern_analyzer"]["failure_pattern_succession_density"] = di_pyImgCompLib.result_pattern_analyzer.failure_pattern_succession_density;
            dt["compare_args"]["p_hash_parametric"]["hash_size"] = di_pyImgCompLib.p_hash_parametric.hash_size;
            dt["compare_args"]["d_hash_parametric"]["hash_size"] = di_pyImgCompLib.d_hash_parametric.hash_size;
            dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_bl_confirmed_variance_auto_update(disabled)"] = di_pyImgCompLib.BRISK_FLANN_parametric.BRISK_FLANN_bl_confirmed_variance_auto_update_disabled;
            dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_parametric_baseline"] = di_pyImgCompLib.BRISK_FLANN_parametric.BRISK_FLANN_parametric_baseline
            dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_baseline_metrics_auto_update(disabled)"] = di_pyImgCompLib.BRISK_FLANN_parametric.BRISK_FLANN_baseline_metrics_auto_update_disabled
            dt["compare_args"]["BRISK_FLANN_parametric"]["BRISK_FLANN_gp_gpp_check_enabled"] = di_pyImgCompLib.BRISK_FLANN_parametric.BRISK_FLANN_gp_gpp_check_enabled
            dt["compare_args"]["BRISK_FLANN_parametric"]["FLANNmatcher_accuracy"] = di_pyImgCompLib.BRISK_FLANN_parametric.FLANNmatcher_accuracy
 
            dt["compare_args"]["similarity"][0]["method1"] = di_pyImgCompLib.similarity.method1;
            dt["compare_args"]["similarity"][0]["m1_score"] = di_pyImgCompLib.similarity.m1_score;
            dt["compare_args"]["similarity"][0]["m1_match_operator"] = di_pyImgCompLib.similarity.m1_match_operator;
            dt["compare_args"]["similarity"][0]["m1_powered_on"] = di_pyImgCompLib.similarity.m1_powered_on;
            dt["compare_args"]["similarity"][0]["m1_eval_groupID"] = di_pyImgCompLib.similarity.m1_eval_groupID;
            dt["compare_args"]["similarity"][0]["group_eval_operator"] = di_pyImgCompLib.similarity.group_eval_operator;
            dt["compare_args"]["similarity"][1]["method2"] = di_pyImgCompLib.similarity.method2;
            dt["compare_args"]["similarity"][1]["m2_score"] = di_pyImgCompLib.similarity.m2_score;
            dt["compare_args"]["similarity"][1]["m2_match_operator"] = di_pyImgCompLib.similarity.m2_match_operator;
            dt["compare_args"]["similarity"][1]["m2_powered_on"] = di_pyImgCompLib.similarity.m2_powered_on;
            dt["compare_args"]["similarity"][1]["m2_eval_groupID"] = di_pyImgCompLib.similarity.m2_eval_groupID;
            dt["compare_args"]["similarity"][1]["group_eval_operator"] = di_pyImgCompLib.similarity.group_eval_operator;
            dt["compare_args"]["similarity"][2]["method3"] = di_pyImgCompLib.similarity.method3;
            dt["compare_args"]["similarity"][2]["m3_score"] = di_pyImgCompLib.similarity.m3_score;
            dt["compare_args"]["similarity"][2]["m3_match_operator"] = di_pyImgCompLib.similarity.m3_match_operator;
            dt["compare_args"]["similarity"][2]["m3_powered_on"] = di_pyImgCompLib.similarity.m3_powered_on;
            dt["compare_args"]["similarity"][2]["m3_eval_groupID"] = di_pyImgCompLib.similarity.m3_eval_groupID;
            dt["compare_args"]["similarity"][2]["group_eval_operator"] = di_pyImgCompLib.similarity.group_eval_operator;
            return dt;
        }
        catch(err){
            console.error("********************ImageVision error location : unpackDI() i.e. reading img-comp-args.json********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("****************************************************************************************************************************")
            throw new Error(`ImageVision | ImageComp error : ${err.name}:${err.message}`)
        }
    }


    private readCompResult(): any {
        //  let resultFile = path.join(this.pathRefs.resultPath, path.basename(dt_comp.imgFile).split(".")[0] + "-comp.json")
        let resultFile = path.join(pathRefs.resultPath, "result_pattern_analysis.json")
        let result_dt: any = null;
        console.log("img comparison result file:" + resultFile);
        if (!fsh.pathExistsSync(resultFile)) {
            console.log("unable to locate comparison result file :" + resultFile);
            expect(true).toEqual(false,`ImageVision - unable to locate comparison resultFile:`+resultFile);
            return result_dt;
        }
        //result_dt = require(resultFile);
        result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        return result_dt;
    }

    private getImgCompResult(): boolean {
        let result = false
        let result_dt = this.readCompResult();
        if (result_dt["net_comp_result"].toString().toLowerCase() == "true")
            result = true;
        else {
            result = false;
            expect(false).toBe(true, "ImageVision - image comparison result : FAILED");
        }
        return result;
        //let result_msg:Array<boolean | string>;
        //result_msg.push(result)
        //result_msg.push(result_dt[0]["message"].toString())
    }


     private getHangIssueResult(resultFile: any): boolean {
        let result = false
        //let result_dt = require(resultFile);
        let result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        if (result_dt["result"].toString().toLowerCase() == "true")
            result = true;
        else {
            result = false;
            expect(false).toBe(true, "hang occured and failed");
        }
        return result;
    }

    private checkImageGrabOpResult():boolean {
        console.log("Checking the ImageGrab operation result...")
        if(pathRefs.imgGrabOpResult){
           return true
        }
        console.log("Image name                 : ",pathRefs.runtime_img)
        console.log("ImageGrab operation result : ",pathRefs.imgGrabOpResult)
        console.log("Unsuccessful operation. Terminating the ImageComp operation...")
        expect("Unsuccessful ImageGrab Operation").toEqual("Successful ImageGrab Operation","Unsuccessful ImageGrab Operatio")
        console.log("")
        console.log("")
        console.log("*************************************END OF pyCompareImages OPERATION***********************************************************************************")
        return false
    }
}