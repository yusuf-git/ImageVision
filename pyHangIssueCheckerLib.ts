/******************** 
* Author : Yusuf
* Authored on : 21-Dec-2021 10:30 AM
* Upates on   : 
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
import { fs_helper as fsh, fs_helper } from "../helpers/fs_helper"
import { async } from 'q';
import {di_pyImgCreativeLib} from "./di_pyImgCreativeLib"
import { di_pyImgCompLib } from "./di_pyImgCompLib"
import {pathRefs} from './pathRefs';
//import {pyCVLibrary} from "./pyCVLibrary"
import { helper } from "kognifai-automation-framework";
import { di_pyHangIssueCheckerLib } from './di_pyHangIssueCheckerLib';

export class pyHangIssueChecker {
    private pathRefs = visionRegistry.pathRefs
    private di_pyImgCompLib = visionRegistry.di_pyImgCompLib
    private pyCVLibrary = visionRegistry.pyCVLib
    private tmp_path = ""
    private baselineImgPath = ""
    private runTimeImgPath = ""
    private diffImgPath = ""
    private pyCVLib = visionRegistry.pyCVLib
    private imageVision_ver = "ImageVision v6"

    public async pyCheckHangIssue(di_pyHangIssueCheckerLib: di_pyHangIssueCheckerLib): Promise<boolean> {
        try {
            console.log("")
            console.log("")
            console.log("*******************************************************pyCheckHangIssue OPERATION BEGINS*************************************************************************************")
            console.log("")
            console.log("")

            this.pyCVLibrary.buildHangIssueCheckerPath(di_pyHangIssueCheckerLib)
            console.log("Hang Issue Checker - runtime img :",di_pyHangIssueCheckerLib.runtime_img_path)
            console.log("Hang Issue Checker - result path :",di_pyHangIssueCheckerLib.net_result_path)
            console.log("Hang Issue Checker - report path :",di_pyHangIssueCheckerLib.hang_issue_reports_path)

            let pyArgsJsonFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/hang_issue_checker.json")
            let pyImgBatFile = path.join(browser.params.baseDir, '..', "py/cv_img_matcher/pyHangIssueChecker.bat")
            let promptChangerBat = path.join(browser.params.baseDir, '..', "py/cv-img-grab/prompt.bat")

            let dt = this.unpackDI(di_pyHangIssueCheckerLib, pyArgsJsonFile);
            let strData = JSON.stringify(dt);
            if(di_pyHangIssueCheckerLib.intermediate_output == "true")
                console.log(strData)
            console.log("----------------------------------------------")
            await this.pyCVLibrary.writeToPyArgsFile(pyArgsJsonFile, strData, di_pyHangIssueCheckerLib.intermediate_output);
            await this.pyCVLib.runPromptChanger(promptChangerBat);
            await this.pyCVLibrary.pyRun(pyImgBatFile, pyArgsJsonFile);
            console.log("----------------------------------------------")

            /* check the result file - if present, read it and set the test outcome accordingly */ 
            let result = this.getHangIssueCheckerResult()
            console.log("ImageVision --> Hang Issue Checker operation result:"+result);
            di_pyHangIssueCheckerLib.setDefault()
            console.log("reset the Hang Issue Checker configs to default....done")
            
            if(!result)
                expect("ImageVision | Hang Issue Checker result : success").toEqual("ImageVision | Hang Issue Checker result : failed","ImageVision --> Hang Issue Checker result : FAILED")

            console.log("")
            console.log("")
            console.log("*************************************END OF pyCheckHangIssue OPERATION***********************************************************************************")
            return result
        }
        catch (err) {
            console.error("********************ImageVision error location : pyCheckHangIssue()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("***************************************************************************************************")
            throw new Error(`ImageVision | Hang Issue Checker error : ${err.name}:${err.message}`)
        }
    }


    private unpackDI(di_pyHangIssueCheckerLib:di_pyHangIssueCheckerLib, argFile) : di_pyHangIssueCheckerLib | null
    {
        try
        {
            //let dt = require(argFile);
            let dt = JSON.parse(fs.readFileSync(argFile, 'utf-8'))
            dt["compare_args"]["appFeatures_CV"] = di_pyHangIssueCheckerLib.appFeatures_CV
            dt["compare_args"]["runtime_img_path"] = di_pyHangIssueCheckerLib.runtime_img_path
            dt["compare_args"]["hang_issue_reports_path"] = di_pyHangIssueCheckerLib.hang_issue_reports_path
            dt["compare_args"]["net_result_path"] = di_pyHangIssueCheckerLib.net_result_path;
            dt["compare_args"]["realtime"] = di_pyHangIssueCheckerLib.realtime;
            dt["compare_args"]["maskRegion"] = di_pyHangIssueCheckerLib.maskRegion;
            dt["compare_args"]["maskRegionExcluding"] = di_pyHangIssueCheckerLib.maskRegionExcluding;
            dt["compare_args"]["aspect_ratio_required"] = di_pyHangIssueCheckerLib.aspect_ratio_required;
            dt["compare_args"]["intermediate_output"] = di_pyHangIssueCheckerLib.intermediate_output;
            dt["compare_args"]["purge_old_artifacts"] = di_pyHangIssueCheckerLib.purge_old_reports;
            dt["compare_args"]["imgcap"] = di_pyHangIssueCheckerLib.imgcap;
            dt["compare_args"]["p_hash_parametric"]["hash_size"] = di_pyHangIssueCheckerLib.p_hash_parametric.hash_size;
            dt["compare_args"]["hang_issue_checker"]["check_frequency_min"] = di_pyHangIssueCheckerLib.hang_issue_checker.check_frequency_min;
 
            dt["compare_args"]["similarity"][0]["method1"] = di_pyHangIssueCheckerLib.similarity.method1;
            dt["compare_args"]["similarity"][0]["m1_score"] = di_pyHangIssueCheckerLib.similarity.m1_score;
            dt["compare_args"]["similarity"][1]["method2"] = di_pyHangIssueCheckerLib.similarity.method2;
            dt["compare_args"]["similarity"][1]["m2_score"] = di_pyHangIssueCheckerLib.similarity.m2_score;
            return dt;
        }
        catch(err){
            console.error("********************ImageVision error location : unpackDI() i.e. reading hang_issue_checker.json********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("****************************************************************************************************************************")
            throw new Error(`ImageVision | ImageComp error : ${err.name}:${err.message}`)
        }
    }


    private readHangIssueCheckResult(): any {
        //  let resultFile = path.join(this.pathRefs.resultPath, path.basename(dt_comp.imgFile).split(".")[0] + "-comp.json")
        let resultFile = path.join(pathRefs.hangIssueChecker_ResultsPath, "hang_issue_result.json")
        let result_dt: any = null;
        console.log("hang issue result file:" + resultFile);
        if (!fsh.pathExistsSync(resultFile)) {
            console.log("unable to locate hang issue result file :" + resultFile);
            expect(true).toEqual(false,`ImageVision - unable to locate hang issue result file:`+resultFile);
            return result_dt;
        }
        //result_dt = require(resultFile);
        result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        return result_dt;
    }


    private getHangIssueCheckerResult(): boolean {
        let result = false
        let result_dt = this.readHangIssueCheckResult();
        if (result_dt["result"].toString().toLowerCase() == "true")
            result = true;
        else {
            result = false;
            expect(false).toBe(true, "ImageVision - hang issue check result : FAILED");
        }
        return result;
    }
}