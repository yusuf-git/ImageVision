/******************** 
* Author : Yusuf
* Authored on : 30-Jul-2020 09:45 PM
* Upates on   : 31-Jul-2020 06:50 AM, 14-Dec-2020 08:45 PM, 08-Dec-2021 02:30 AM, 09-Dec-2021 03:10 AM, 10-Dec-2021 10:50 PM, 16-Dec-2021 02:00 AM, 17-Dec-2021 08:30 AM to 02:30 PM, 18-Dec-2021 11:30 AM ,19-Dec-2021 08:40 PM, 20-Dec-2021 07:30 AM to 11:55 PM, 21-Dec-2021 03:15 AM
* Lib for performing CV based actions
*
*********************/

/*future improvements(recorded on 20-Jul-2020 12:45 AM):
    - support for protractor parallelism while calling python img lib through cmd and static img-cap-args.json
    - create REST APIs for python img lib and call them
    - immediate - crop the specified portion of the captured image - for time scale real-time scenarios
*/

import * as fse from 'fs-extra';
import { ImageVisionRegistry as visionRegistry } from "../factory/ImageVisionRegistry";
import { browser, by, protractor,ExpectedConditions } from "protractor";
import * as path from "path";
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework";
import * as cp from 'child_process';
//import {PythonShell} from 'python-shell';
import * as fs from 'fs';
import { fs_helper as fsh, fs_helper} from "./../helpers/fs_helper"
import { async } from 'q';
import {di_pyImgInteractLib} from "./di_pyImgInteractLib"
import { helper } from "kognifai-automation-framework";
import {pathRefs} from './pathRefs';

export class pyImgInteractLib {

    //public async pyGrabImage(el:IElementWrapper,imgFile: string,cn?:number) {

        private pathRefs = visionRegistry.pathRefs
        private di_pyImgInteractLib = visionRegistry.di_pyImgInteractLib
        private pyCVLibrary = visionRegistry.pyCVLib
        private tmp_path = ""
        private baselineImgPath = ""
        private runTimeImgPath = ""
        private diffImgPath = ""

        //public async pyActionize(di_pyActionizeLib: di_pyImgInteractLib, template_img:string, dirCustomName?:string ): Promise<boolean> {
        public async pyActionize(di_pyActionizeLib: di_pyImgInteractLib, template_img?:string): Promise<boolean> {
            try {
                console.log("")
                console.log("")
                console.log("*******************************************************Actionize OPERATION BEGINS*************************************************************************************")
                console.log("")
                console.log("")
                pathRefs.actionizeOpResult = false
                di_pyActionizeLib.realtime_mode = "false"
                this.resetStandardPathRefPaths()
                await this.pyCVLibrary.addBrowserEntry();
                console.log("added active browser name to cache :"+helper.testRunCache.readKey("currentBrowser"));
                if(template_img != null && template_img != "")
                    di_pyActionizeLib.template_img = template_img
                this.pyCVLibrary.buildActionizePath(di_pyActionizeLib);
    
                di_pyActionizeLib.template_img = path.join(pathRefs.actionizeTemplateImgPath,template_img);
                console.log("template img:",di_pyActionizeLib.template_img)
                //console.log("runtime img:",di_pyActionizeLib.runtime_img)
                console.log("pathRefs.actionizeRuntimePath:",pathRefs.actionizeRuntimePath)
    
                if(di_pyActionizeLib.template_img == null || di_pyActionizeLib.template_img == ""){
                    return false
                }
                if(di_pyActionizeLib.net_result_path == null || di_pyActionizeLib.net_result_path == "")
                    di_pyActionizeLib.net_result_path = pathRefs.actionizeRuntimePath
                
                    if(di_pyActionizeLib.reports_path == null || di_pyActionizeLib.reports_path == "")
                       di_pyActionizeLib.reports_path = pathRefs.actionizeRuntimePath
                di_pyActionizeLib.imgArchivesPath = pathRefs.imgOpsSessionRootPath;
    
                let pyArgsJsonFile = path.join(browser.params.baseDir, '..', "py/cv-img-interact/actionize_configs.json")
                let pyImgBatFile = path.join(browser.params.baseDir, '..', "py/cv-img-interact/pyActionize.bat")
                let promptChangerBat = path.join(browser.params.baseDir, '..', "py/cv-img-grab/prompt.bat")
    
                let dt = this.unpackDI(di_pyActionizeLib, pyArgsJsonFile);
                let strData = JSON.stringify(dt);
                if(di_pyActionizeLib.intermediate_output == "true")
                    console.log(strData)
                console.log("----------------------------------------------")
                await this.pyCVLibrary.writeToPyArgsFile(pyArgsJsonFile, strData, di_pyActionizeLib.intermediate_output);
                await this.pyCVLibrary.runPromptChanger(promptChangerBat);
                await this.pyCVLibrary.pyRun(pyImgBatFile, pyArgsJsonFile);
                console.log("----------------------------------------------")
    
                /* check the result file - if present, read it and set the test outcome accordingly */ 
                let result = this.getActionizeResult()
                console.log("template image :"+ path.basename(di_pyActionizeLib.template_img)+" --> Actionize operation result:"+result);
                di_pyActionizeLib.setDefault()
                console.log("reset the Actionize configs to default....done")

                if(!result){
                    let tmpMsg = this.getErrorMsg()
                    expect("ImageVision | Actionize : success").toBe("ImageVision | Actionize : failed","ImageVision --> Actionize -"+tmpMsg)
                }

   
                console.log("")
                console.log("")
                console.log("*************************************END OF Actionize OPERATION***********************************************************************************")
                return result
            }
            catch (err) {
                console.error("********************ImageVision error location : pyActionize()********************************")
                console.error(`error message: ${err.name}:${err.message}`)
                console.error("stack:",err.stack)
                console.error("***************************************************************************************************")
                throw new Error(`ImageVision | Actionize error : ${err.name}:${err.message}`)
    
            }
        }

/*        public async get_RT_RuntimePath(di_pyActionizeLib: di_pyImgInteractLib){
            if(di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path == null || di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path == ""){
                di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path = pathRefs.runTimeImgPath
            }
            return di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path
        }*/

    
        public async RT_DetectAnomaly(di_pyActionizeLib: di_pyImgInteractLib, dirCustomName="") { //data gap (negative)
 
            this.resetRTPathRefs()
            
            /* RULE : realtime_mode must be true and neg_condition_check_mode must be set to true */
            di_pyActionizeLib.realtime_mode = "true"
            di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode = "true"
            this.setupSteps_InvokeRT(di_pyActionizeLib, dirCustomName)
        }

 
        public async RT_RunPositiveChecks(di_pyActionizeLib: di_pyImgInteractLib, dirCustomName=""){ //tool tip validation
 
            this.resetRTPathRefs()
            
            /* RULE : realtime_mode must be true and neg_condition_check_mode must be set to false */
            di_pyActionizeLib.realtime_mode = "true"
            di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode = "false"
            this.setupSteps_InvokeRT(di_pyActionizeLib, dirCustomName)
        }


        public getRTPositiveBaselinePath(){
            return pathRefs.RT_PositiveBaselinePath
        }
  
        public getRTNegativeBaselinePath(){
            return pathRefs.RT_NegativeBaselinePath
        }
    
        public getRTRuntimePath(){
            return pathRefs.RT_RuntimeImgsPath
        }

        /*
          One RT test case - by QA
          
          1. How many it() blocks ? : 
                
          2. Scope for it() block-1 ?
                
                - Start simulation for one hour : 4000 ft. depth difference between start and end. 
                                                  Ex: 19000 to 23000 ft. depth
                
                - Select Wellbore --> Add Mnemonics --> Apply "Goto" : duration 8 mins.
                
                - Run positive checks for tool tip validation
        
          3. Scope for it() block-2 ?
                - Simulate data for one hour. Expected time lag before capture : 8 mins.
                - Capture 




        */


        private async setupSteps_InvokeRT(di_pyActionizeLib:di_pyImgInteractLib, dirCustomName=""){
            /* building the RT paths is the same for both neg and pos conditions */
            this.pyCVLibrary.buildRTPaths(di_pyActionizeLib, dirCustomName)
            
            let pyArgsJsonFile = path.join(browser.params.baseDir, '..', "py/cv-img-interact/actionize_configs.json")
            let pyImgBatFile = path.join(browser.params.baseDir, '..', "py/cv-img-interact/pyActionize.bat")
            let promptChangerBat = path.join(browser.params.baseDir, '..', "py/cv-img-grab/prompt.bat")

            /* perform unpack of the dependency injection and assign user assigned property values */
            let dt = this.unpackDI(di_pyActionizeLib, pyArgsJsonFile);
            let strData = JSON.stringify(dt);
            if(di_pyActionizeLib.intermediate_output == "true")
                console.log(strData)

            /* Invoke the ImageVision backend engine by supplying the configurations */
            console.log("----------------------------------------------")
            await this.pyCVLibrary.writeToPyArgsFile(pyArgsJsonFile, strData, di_pyActionizeLib.intermediate_output);
            await this.pyCVLibrary.runPromptChanger(promptChangerBat);
            await this.pyCVLibrary.pyRun(pyImgBatFile, pyArgsJsonFile);
            console.log("----------------------------------------------")
            
            /* Get the operation result message on the basis of either positive or negative conditions*/
            let tmpMsg = this.getOperationResultMsg(di_pyActionizeLib)

            /* check the result file - if present, read it and set the test outcome accordingly */ 
            let result = this.getRTResult(di_pyActionizeLib)
            console.log(tmpMsg + result);

            /* set the configurations to default values so that it's set to be clean for the next RT call */
            di_pyActionizeLib.setDefault()
            console.log("reset the RT & Actionize configs to default....done")

            /* fail the current test on the result of the ImageVision - RT operation becomes false */
            if(!result){
                console.log("Testing failureeeeeeeee....done")
                expect("ImageVision | Actionize : success").toBe("ImageVision | Actionize : failed", tmpMsg + " FAILED")
            }
            else
            console.log("Testing Passsssssssssssssss....done")
        }


     
        private unpackDI(di_pyActionizeLib:di_pyImgInteractLib, pyArgsJsonFile) : di_pyImgInteractLib | null
        {
            try
            {
                //let dt = require(pyArgsJsonFile)
                let dt = JSON.parse(fs.readFileSync(pyArgsJsonFile, 'utf-8'))
                dt["actionize_args"]["appFeatures_CV"] = di_pyActionizeLib.appFeatures_CV
                dt["actionize_args"]["template_img"] = di_pyActionizeLib.template_img
                dt["actionize_args"]["reports_path"] = di_pyActionizeLib.reports_path
                dt["actionize_args"]["net_result_path"] = di_pyActionizeLib.net_result_path
                dt["actionize_args"]["browserDependent"] = di_pyActionizeLib.browserDependent
                dt["actionize_args"]["intermediate_output"] = di_pyActionizeLib.intermediate_output
                dt["actionize_args"]["purge_old_artifacts"] = di_pyActionizeLib.purge_old_artifacts
                dt["actionize_args"]["continue_on_failure"] = di_pyActionizeLib.continue_on_failure
                dt["actionize_args"]["imgArchivesPath"] = di_pyActionizeLib.imgArchivesPath

                dt["actionize_args"]["actions"] = di_pyActionizeLib.actions
                dt["actionize_args"]["action_inputs"]["type_text"] = di_pyActionizeLib.action_inputs.type_text
                dt["actionize_args"]["action_inputs"]["scroll_up_units"] = di_pyActionizeLib.action_inputs.scroll_up_units
                dt["actionize_args"]["action_inputs"]["scroll_down_units"] = di_pyActionizeLib.action_inputs.scroll_down_units
                dt["actionize_args"]["action_inputs"]["rel_x_y"] = di_pyActionizeLib.action_inputs.rel_x_y
                dt["actionize_args"]["action_inputs"]["mouse_move_delay"] = di_pyActionizeLib.action_inputs.mouse_move_delay
                dt["actionize_args"]["action_inputs"]["mouse_drag_to_coords"] = di_pyActionizeLib.action_inputs.mouse_drag_to_coords
                dt["actionize_args"]["action_inputs"]["drop_target_img"] = di_pyActionizeLib.action_inputs.drop_target_img
                dt["actionize_args"]["action_inputs"]["wait_seconds"] = di_pyActionizeLib.action_inputs.wait_seconds
                dt["actionize_args"]["action_inputs"]["matched_instance"] = di_pyActionizeLib.action_inputs.matched_instance
                dt["actionize_args"]["search_methods"][0]["method1"] = di_pyActionizeLib.search_methods.method1
                dt["actionize_args"]["search_methods"][0]["m1_threshold"] = di_pyActionizeLib.search_methods.m1_threshold

                /* RT_Anomaly_Detection */ 
                dt["actionize_args"]["realtime_mode"] = di_pyActionizeLib.realtime_mode
                dt["actionize_args"]["RT_anomaly_detection"]["neg_condition_check_mode"] = di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode
                dt["actionize_args"]["RT_anomaly_detection"]["reports_path"] = di_pyActionizeLib.RT_anomaly_detection.reports_path
                dt["actionize_args"]["RT_anomaly_detection"]["net_result_path"] = di_pyActionizeLib.RT_anomaly_detection.net_result_path
                dt["actionize_args"]["RT_anomaly_detection"]["positive_conditions"]["baseline_path"] = di_pyActionizeLib.RT_anomaly_detection.positive_conditions.baseline_path
                dt["actionize_args"]["RT_anomaly_detection"]["negative_conditions"]["baseline_path"] = di_pyActionizeLib.RT_anomaly_detection.negative_conditions.baseline_path
                dt["actionize_args"]["RT_anomaly_detection"]["runtime_imgs_path"] = di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path
                return dt;
            }
            catch(err){
                console.error("********************ImageVision error location : unpackDI() i.e. reading actionize_args.json********************************")
                console.error(`error message: ${err.name}:${err.message}`)
                console.error("stack:",err.stack)
                console.error("****************************************************************************************************************************")
                throw new Error(`ImageVision | Actionize error : ${err.name}:${err.message}`)
            }
    }

    private resetStandardPathRefPaths(){
        pathRefs.actionizeTemplateImgPath = ""
        pathRefs.actionizeRuntimePath = ""
        pathRefs.actionizeReportsPath = ""
        pathRefs.actionizeResultsPath = ""
        pathRefs.actionizeOpResult = false
        pathRefs.RT_mode = false
    }

    private resetRTPathRefs(){
        pathRefs.RT_NegativeBaselinePath = ""
        pathRefs.RT_PositiveBaselinePath = ""
        //pathRefs.RT_RuntimeImgsPath = ""
        pathRefs.RT_ResultsPath = ""
        pathRefs.RT_ReportsPath = ""
    }
 
    private getOperationResultMsg(di_pyActionizeLib:di_pyImgInteractLib) : string {
        let tmpMsg = ""
        if(di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode.toLowerCase() != "true")
            tmpMsg = "ImageVision --> RT anomaly detection(positive condition) operation result :"
        else
            tmpMsg = "ImageVision --> RT anomaly detection(negative condition) operation result :"
        return tmpMsg
    }

    private readActionizeResult(): any {
        //  let resultFile = path.join(this.pathRefs.resultPath, path.basename(dt_comp.imgFile).split(".")[0] + "-comp.json")
        let resultFile = path.join(pathRefs.actionizeResultsPath, "actionize_result.json")
        let result_dt: any = null;
        console.log("actionize result file:" + resultFile);
        if (!fsh.pathExistsSync(resultFile)) {
            console.log("unable to locate actionize result file :" + resultFile);
            expect(true).toEqual(false,`ImageVision - unable to locate actionize resultFile:`+resultFile);
            return result_dt;
        }
        //result_dt = require(resultFile);
        result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        return result_dt;
    }

    private getActionizeResult(): boolean {
        let result = false
        let result_dt = this.readActionizeResult();
        let tmpMsg = ""
        if (result_dt["result"].toString().toLowerCase() == "true")
            result = true;
        else {
            result = false;
            tmpMsg = result_dt["message"].toString()
            expect(false).toBe(true, "ImageVision - Actionize operation result : FAILED -"+ tmpMsg);
        }
        return result;
        //let result_msg:Array<boolean | string>;
        //result_msg.push(result)
        //result_msg.push(result_dt[0]["message"].toString())
    }

    private readRTResult(di_pyActionizeLib:di_pyImgInteractLib): any {
        //  let resultFile = path.join(this.pathRefs.resultPath, path.basename(dt_comp.imgFile).split(".")[0] + "-comp.json")
        let resultFile = ""
        if(di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode.toLowerCase() == "true")
            resultFile = path.join(pathRefs.RT_ResultsPath, "RT_data_gap_net_result.json")
        else
            resultFile = path.join(pathRefs.RT_ResultsPath, "RT_data_gap_net_result.json")
        let result_dt: any = null;
        console.log("RT result file:" + resultFile);
        if (!fsh.pathExistsSync(resultFile)) {
            console.log("unable to locate RT result file :" + resultFile);
            expect(true).toEqual(false,`ImageVision - unable to locate RT resultFile:`+resultFile);
            return result_dt;
        }
        //result_dt = require(resultFile);
        result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        return result_dt;
    }

    private getRTResult(di_pyActionizeLib:di_pyImgInteractLib): boolean {
        let result = false
        let result_dt = this.readRTResult(di_pyActionizeLib);
        let tmpMsg = ""
        let negative_check = true

        if(di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode.toLowerCase() != "true"){
             negative_check = false
             tmpMsg = "ImageVision - RT anomaly detection(positive condition) operation result :"
        }
        else{
             tmpMsg = "ImageVision - RT anomaly detection(negative condition) operation result :"
        }

        if (result_dt["net_result"].toString().toLowerCase() == "true"){
            result = true;
            console.log(tmpMsg + " PASSED")
        }
        else {
            result = false;
            expect(false).toBe(true, tmpMsg + " FAILED");
        }
        return result;
    }

    private getErrorMsg(): string {
        let result_dt = this.readActionizeResult();
        let tmpMsg = ""
        if (result_dt["result"].toString().toLowerCase() != "true")
            tmpMsg = result_dt["message"].toString()
        return tmpMsg
    }
}