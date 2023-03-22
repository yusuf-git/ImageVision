/******************** 
* Author : Yusuf
* Authored on : 11-Jul-2020 10:45 AM
* Upates on   : 11-Jul-2020 08:00 PM, 12-Jul-2020 12:30 AM, 13-Jul-2020 to 19-Jul-2020 02:40 AM, 20-Jul-2020 03:30 PM, 21-Jul-2020 04:30 PM, 22-Jul-2020, 23-Jul-2020 02:45 AM, 10-Dec-2020 03:10 AM, 12-Dec-2020 01:30 AM, 09:30 AM to 11:50 PM, 13-Dec-2020 02:25 AM, 06:15 PM, 14-Dec-2020 02:00 AM, 08:45 PM, 20-Dec-2020 09:10 PM, 22-Dec-2020 01:50 AM, 24-Oct-2020 02:45 AM, 22-Nov-2021 02:30 AM, 16-Dec-2021 02:00 AM, 17-Dec-2021 08:30 AM to 02:30 PM, 18-Dec-2021 11:30 AM, 11:50 PM, 20-Dec-2021 07:30 AM to 12:30 PM, 10:30 PM to 11:55 PM, 21-Dec-2021 12:00 AM to 03:20 AM
* Lib for handling CV python library 
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
import { fs_helper as fsh, fs_helper} from "../helpers/fs_helper"
import { async } from 'q';
import {di_pyImgCreativeLib} from "./di_pyImgCreativeLib"
import { helper } from "kognifai-automation-framework";
import { di_pyImgCompLib } from './di_pyImgCompLib';
import { di_pyImgInteractLib } from './di_pyImgInteractLib';
import {pathRefs} from './pathRefs';
import { Guid } from "guid-typescript";
import { di_pyImgLib } from './di_pyImgLib';
import { di_pyHangIssueCheckerLib } from './di_pyHangIssueCheckerLib';

export class pyCVLibrary {

    //public async pyGrabImage(el:IElementWrapper,imgFile: string,cn?:number) {

        pathRefs = visionRegistry.pathRefs
        baselineImgPath = ""
        actionizeTemplateImgPath = ""
        actionizeRuntimePath = ""
        actionizeResultsPath = ""
        actionizeReportsPath = ""
        runTimeImgPath = ""
        reportsPath = ""
        imgOpsSessionRootPath = ""
        resultPath = ""
        public static sessionID = ""
        imageVision_ver = "ImageVision v6"
        failCurrentTestOnFailedImgOp = ""
        
        
        buildfeatureImgPaths(di_pyImgLib:di_pyImgCreativeLib|di_pyImgCompLib, dirCustomName="") : void|null
        {
            try{
                let dt = new Date();
                let dateTimeStamp = dt.getDay().toString()+(dt.getMonth()+1).toString()+dt.getFullYear().toString()+"_"+dt.getHours().toString()+dt.getMinutes().toString()+dt.getSeconds().toString();
                let runtimePathSubstr = "";
                let tmp_baseline_path = "";
                //pathRefs.resultPath = ""
                this.resultPath = ""
           
                /* block for building runtime path */
                runtimePathSubstr = this.getSessionID();
                runtimePathSubstr = this.getFeature_DirLabel_Path(dirCustomName, di_pyImgLib, dateTimeStamp)
                this.resultPath = path.join(runtimePathSubstr);
                runtimePathSubstr = this.getScenarioPath(di_pyImgLib, runtimePathSubstr)
                runtimePathSubstr = this.addBrowserToPath(di_pyImgLib, runtimePathSubstr)
                console.log("ceheck this- rutimePathSubstr:",runtimePathSubstr)

                /* block for building baseline path */
                tmp_baseline_path = this.getBaselineFeaturePath(di_pyImgLib);
                tmp_baseline_path = this.getScenarioPath(di_pyImgLib, tmp_baseline_path)
                tmp_baseline_path = this.addBrowserToPath(di_pyImgLib, tmp_baseline_path)
                  
                this.imgOpsSessionRootPath = this.getImgArchivesRootPath(di_pyImgLib);
                this.baselineImgPath = path.join(pathRefs.baselineRootPath, tmp_baseline_path, "baseline");
                this.runTimeImgPath = path.join(this.imgOpsSessionRootPath, runtimePathSubstr, "runTime");
                pathRefs.imgArchivesPath =  path.join(this.imgOpsSessionRootPath);
                pathRefs.imgOpsSessionRootPath = path.join(this.imgOpsSessionRootPath);
                pathRefs.baselineImgPath = this.baselineImgPath;
                pathRefs.runTimeImgPath = this.runTimeImgPath;
                pathRefs.resultPath = path.join(this.runTimeImgPath)
                pathRefs.reportsPath = path.join(this.runTimeImgPath);
                console.log("pathRefs.baselineImgPath:",pathRefs.baselineImgPath)
                console.log("pathRefs.runTimeImgPath:",pathRefs.runTimeImgPath)
                console.log("pathRefs.resultPath:",pathRefs.resultPath)
                console.log("pathRefs.reportsPath:",pathRefs.reportsPath)
                console.log("DEBUG:::Result path:",pathRefs.resultPath)

                //this.diffImgPath = path.join(this.imgOpsSessionRootPath, runtimePathSubstr, "diff");
                //this.resultPath = path.join(this.imgOpsSessionRootPath, this.resultPath);
                //this.resultPath = this.runTimeImgPath;
                //pathRefs.resultsRootPath = this.resultPath
                //this.pathRefs.resultPath = path.join(this.resultPath, "img-capture-results")
                //pathRefs.resultPath = path.join(this.resultPath)
                
                this.createPaths()
                if(typeof di_pyImgLib == typeof di_pyImgCreativeLib){
                    //console.log("activated di type : di_pyImgCreativeLib")
                }
                if(di_pyImgLib instanceof di_pyImgCreativeLib){
                    //console.log("di_pyImgLib instace type : di_pyImgCreativeLib")
                }
                if(di_pyImgLib !instanceof di_pyImgCreativeLib){
                }
            }
            catch(err){
                console.error("********************ImageVision error location : pyCVLibrary | buildfeatureImgPaths()********************************")
                console.error(`error message: ${err.name}:${err.message}`)
                console.error("stack:",err.stack)
                console.error("*********************************************************************************************************************")
                return null;
            }
        }


       private getSessionID() : string {
            if(pyCVLibrary.sessionID == ""){
                pyCVLibrary.sessionID = Guid.create().toString();
            }
            return pyCVLibrary.sessionID;
       }

       private getFeature_DirLabel_Path(dirLabel:string, di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib, dateTimeStamp : string) : string {
           try{
                let min = 1
                let max = 1000
                let tmp_path = ""
                let filename = ""
                if(di_pyImgLib instanceof di_pyImgCreativeLib){
                    filename = path.basename(di_pyImgLib.imgFile)
                }
                if(dirLabel != ""){
                    let randInt = Math.floor(Math.random() * (max - min + 1)) + min
                    tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV], dirLabel+"_"+randInt.toString())
                }
                else
                    tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV], dateTimeStamp)
                return tmp_path
            }
            catch(err){
                console.error("********************ImageVision error location : pyCVLibrary | getFeature_DirLabel_Path()********************************")
                console.error(`error message: ${err.name}:${err.message}`)
                console.error("stack:",err.stack)
                console.error("*************************************************************************************************************************")
                return ""
            }
       }

       private getScenarioPath(di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib , pathSubstr:string):string {
            let tmp_path = ""
            if(di_pyImgLib.uiObjSnap == "true"){
                tmp_path = path.join(pathSubstr, "uiobj");
            }
            else if(di_pyImgLib.realtime == "true"){
                tmp_path = path.join(pathSubstr, "realtime")
            }
            else if((di_pyImgLib.realtime == "false" && di_pyImgLib.uiObjSnap == "false") || (di_pyImgLib.realtime == '' && di_pyImgLib.uiObjSnap == '')){
                tmp_path =  path.join(pathSubstr, "historical")
            }
            return tmp_path
       }

       private addBrowserToPath(di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib, pathSubstr:string):string {
            let tmp_path = ""
            if(di_pyImgLib.browserDependent == "true"){
                let browserName = helper.testRunCache.readKey("currentBrowser");
                tmp_path = path.join(pathSubstr, browserName)
            }
            else 
                tmp_path = pathSubstr
            return tmp_path
       }

       private getImgArchivesRootPath(di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib) : string 
       {
            if(di_pyImgLib.imgArchivesPath != "" && di_pyImgLib.imgArchivesPath != undefined && di_pyImgLib.imgArchivesPath != null)
            {
                console.log("imgArchivesPath != ''")
                this.imgOpsSessionRootPath = di_pyImgLib.imgArchivesPath;
			}
            else if((di_pyImgLib.imgArchivesPath == "" || di_pyImgLib.imgArchivesPath == undefined) && ((browser.params.imgArchivesPath == "" || browser.params.imgArchivesPath == undefined || browser.params.imgArchivesPath == null ))) // || !browser.params.hasOwnProperty('imgArchivesPath')))
            {
                console.log("browser.params.imgArchivesPath isn't existing...")
                this.imgOpsSessionRootPath = path.join(__dirname, "..", "..", "img-archives", "imagevision")
                console.log("Created custom img-archives path..."+this.imgOpsSessionRootPath)
            }
            else if((di_pyImgLib.imgArchivesPath == ""  || di_pyImgLib.imgArchivesPath == undefined) && (browser.params.imgArchivesPath != "" && browser.params.imgArchivesPath != undefined && browser.params.imgArchivesPath != null ))
			{  
			  console.log("== && != ''")
			
			  this.imgOpsSessionRootPath = path.join(browser.params.imgArchivesPath);
			}

            console.log("imgOpsSessionRootPath :",this.imgOpsSessionRootPath);
            return this.imgOpsSessionRootPath;
       }

       private getBaselineFeaturePath(di_pyImgLib:di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib) : string 
       {
            return path.join(this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV])
       }

   
       public async addBrowserEntry(){
            await browser.getCapabilities().then(cap => {
                helper.testRunCache.writeTo([{ "currentBrowser": cap.get('browserName') }])
            })
        }

        
        async writeToPyArgsFile(pyArgsFile, strData, intermediate_output="false"): Promise<boolean> {
            let result =false;
            if(intermediate_output == "true"){
                console.log("============================================")
                console.log("pyArgs :"+strData)
                console.log("============================================")
            }
            await new Promise( (resolve,reject) => {
                try{
                    fs.writeFile(pyArgsFile, strData, 'utf8', (err) => {
                        if (err) {
                            reject("ERROR ::: Writing to " + pyArgsFile + ":" + err);
                        }
                        else {
                            if(fsh.pathExistsSync(pyArgsFile)){
                                result = true;
                                resolve("Created " + pyArgsFile + "...OK");
                            }
                        }
                    });
                }
                catch(Error){
                    throw Error("Error::writing to PyArgs");
                }
            })
            .then(() => console.log("Written to " + pyArgsFile))
            .catch((e) => console.log("Exception caught writing to pyArgs:: " + pyArgsFile,e));
            console.log(pyArgsFile + " pyArgs update operation :",result);
            return result;
        }

       
    async pyRun(pyImgBatFile:string,pyArgsJsonFile:string) {
        //let path = "E:"
        //let path1 = "C:\\Users\\nandik\\SDVAutomation\\src\\test-inputs\\images\\sitecom-viewer\\widgets\\log-widget\\historical\\chrome\\baseline\\B10\\pyth"+i+".png"
        //    var exec = require('child_process').exec;
      
        //cp.execSync(`cmd /c start "" cmd /c python.bat ${path} ${path1}`)
        //let cmd = "python " + path.join(pyFile + " " + pyFileArgs);
        //let pyImgCreativeBat = path.join(browser.params.baseDir, '..', pyImgBatFile)
        let cmd = `cmd /k ` + pyImgBatFile + ` -j ` + pyArgsJsonFile;
        //console.log("cmd:",cmd);
        //cp.execSync(cmd, {stdio: 'inherit'})     
        ///cp.execSync("notepad.exe");
        var options = {
            //cwd:"D:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_86", 
            //cwd:"C:/Program Files/Python-3.7.4",
            cwd:'C:/windows/System32',
            stdio: 'inherit'
        };
        
        //cp.execSync(cmd, {cwd:"D:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_86", stdio: 'inherit'});
        cp.execSync(cmd,options)
        /*cp.exec(cmd, options, (error,stdout,stderr) =>{
            if(error){
                console.log("cp.exec :: error:",error);
            }
            if(stdout){
                console.log("stdout ==>",stdout);
            }
            if(stderr){
                console.log("stderr ==>",stderr);
            }
        });*/
        //console.log("done with pyRun()");
    }

    // getImgGrabResult():boolean
    // {   
    //     let result = false
    //     let compResultFile = path.join(pathRefs.resultPath, path.basename(di_pyImgCreativeLib.imgFile).split(".")[0]+"-cap.json")
    //     let result_dt = this.readCaptureResult(compResultFile);
    //     if(result_dt["result"].toString().toLowerCase() == "true")
    //         result = true;
    //     else if(result_dt["result"].toString().toLowerCase() == "false" && di_pyImgCreativeLib.failCurrentTestOnFailedImgOp.toLowerCase() == "true")
    //         expect(`${this.imageVision_ver} - failed image creation`).toEqual(`${this.imageVision_ver} - successful image creation`,`${this.imageVision_ver} - image creation operation failed - img:` + path.join(di_pyImgCreativeLib.imgFile));

    //     return result;
    //     //let result_msg:Array<boolean | string>;
    //     //result_msg.push(result)
    //     //result_msg.push(result_dt[0]["message"].toString())
    // }


    async runPromptChanger(pyImgBatFile:string) {
        let cmd = `cmd /k ` + pyImgBatFile + " >nul";
        var options = {
            cwd:'C:/windows/System32',
            stdio: 'inherit'
        };
        cp.execSync(cmd,options)
    }


    createPaths(){
        fsh.ensureDirExistsSync(pathRefs.baselineImgPath)
        fsh.ensureDirExistsSync(this.imgOpsSessionRootPath)
        fsh.ensureDirExistsSync(pathRefs.runTimeImgPath)
        //fsh.ensureDirExistsSync(this.pathRefs.diffImgPath)
        fsh.ensureDirExistsSync(pathRefs.resultPath)
        fsh.ensureDirExistsSync(pathRefs.reportsPath)
        fsh.ensureDirExistsSync(pathRefs.brisk_flann_baseline_path)
    }

    async pyInvoke(pyFile:string, options:object) {
        // var path=require('path')
         //let pyPath = "python" + path.join(browser.params.baseDir,'..', "take_screenshot.py")
         //let path1 = "C:\\Users\\nandik\\SDVAutomation\\src\\test-inputs\\images\\sitecom-viewer\\widgets\\log-widget\\historical\\chrome\\baseline\\B10\\pyth"+i+".png"
          //    var exec = require('child_process').exec;
        
         //execSync(`cmd /c start "" cmd /c python.bat ${path} ${path1}`)
         //execSync(`cmd /c start "" cmd /c python.bat ${path} ${path1}`)
       
         //commented below on 09-Dec-2020 09:05 AM
       /*  let opt ={};
         PythonShell.run(pyFile, options, function (err, results) {
             if (err) throw err;
             // results is an array consisting of messages collected during execution
             console.log('results: %j', results);
           }); */
           
     }
 

 cumulativeOffset = function(element) {
    var top = 0, left = 0;
    do {
        top += element.offsetTop  || 0;
        left += element.offsetLeft || 0;
        element = element.offsetParent;
    } while(element);

    return {
        top: top,
        left: left
    };
};

/*          Library functions for Actionize module             */ 


private get_Actionize_Baseline_FeaturePath(di_pyImgLib:di_pyImgInteractLib) : string 
{
     return path.join(this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV])
}

private get_Actionize_SubfeaturePath(di_pyImgLib:di_pyImgInteractLib, pathSubstr:string) : string 
{
     return path.join( pathSubstr ,this.pathRefs.subFeatureImgPath[di_pyImgLib.appFeatures_CV])
}

private get_Actionize_Runtime_Feature_DirLabel_Path(dirLabel:string, di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib, dateTimeStamp : string) : string {
    try{
         let tmp_path = ""
         if(dirLabel != "")
             //tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV], dirLabel)
             tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV])
         else
             //tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV], dateTimeStamp)
             tmp_path = path.join( pyCVLibrary.sessionID, this.pathRefs.featureImgPath[di_pyImgLib.appFeatures_CV])
         return tmp_path
     }
     catch(err){
         console.error("********************ImageVision error location : pyCVLibrary | get_Actionize_Feature_DirLabel_Path()********************************")
         console.error(`error message: ${err.name}:${err.message}`)
         console.error("stack:",err.stack)
         console.error("*************************************************************************************************************************")
         return ""
     }
}

private getActionizeScenarioPath(isUIObjSnap : boolean , pathSubstr:string):string {
    let tmp_path = ""
    if(isUIObjSnap){
        tmp_path = path.join(pathSubstr, "uiobj");
    }
    return tmp_path
}

createActionizePaths(){
    fsh.ensureDirExistsSync(pathRefs.actionizeRuntimePath)
    fsh.ensureDirExistsSync(this.imgOpsSessionRootPath)
    fsh.ensureDirExistsSync(pathRefs.actionizeResultsPath)
    fsh.ensureDirExistsSync(pathRefs.actionizeReportsPath)
}



buildActionizePath(di_pyImgLib:di_pyImgInteractLib, dirCustomName="") : void|null
{
    try{
        let dt = new Date();
        let dateTimeStamp = dt.getDay().toString()+(dt.getMonth()+1).toString()+dt.getFullYear().toString()+"_"+dt.getHours().toString()+dt.getMinutes().toString()+dt.getSeconds().toString();
        let runtimePathSubstr = "";
        let tmp_baseline_path = "";
        //pathRefs.resultPath = ""
        //this.resultPath = ""
   
        /* block for building runtime path */
        runtimePathSubstr = this.getSessionID();
        runtimePathSubstr = this.get_Actionize_Runtime_Feature_DirLabel_Path(dirCustomName, di_pyImgLib, dateTimeStamp)
        this.resultPath = path.join(runtimePathSubstr);
        runtimePathSubstr = this.getActionizeScenarioPath(true, runtimePathSubstr)
        runtimePathSubstr = this.get_Actionize_SubfeaturePath(di_pyImgLib, runtimePathSubstr)
        runtimePathSubstr = this.addBrowserToPath(di_pyImgLib, runtimePathSubstr)
        console.log("check this- rutimePathSubstr:",runtimePathSubstr)

        /* block for building baseline path */
        tmp_baseline_path = this.get_Actionize_Baseline_FeaturePath(di_pyImgLib);
        tmp_baseline_path = this.getActionizeScenarioPath(true, tmp_baseline_path)
        tmp_baseline_path = this.get_Actionize_SubfeaturePath(di_pyImgLib, tmp_baseline_path)
        tmp_baseline_path = this.addBrowserToPath(di_pyImgLib, tmp_baseline_path)
          
        this.imgOpsSessionRootPath = this.getImgArchivesRootPath(di_pyImgLib)
        this.actionizeTemplateImgPath = path.join(pathRefs.baselineRootPath, tmp_baseline_path)
        this.actionizeRuntimePath = path.join(this.imgOpsSessionRootPath, runtimePathSubstr)
        pathRefs.imgArchivesPath =  path.join(this.imgOpsSessionRootPath)
        pathRefs.imgOpsSessionRootPath = path.join(this.imgOpsSessionRootPath)
        pathRefs.actionizeTemplateImgPath = path.join(this.actionizeTemplateImgPath)
        pathRefs.actionizeRuntimePath = path.join(this.actionizeRuntimePath)
        pathRefs.actionizeResultsPath = path.join(this.actionizeRuntimePath)
        pathRefs.actionizeReportsPath = path.join(this.actionizeRuntimePath)
        console.log("pathRefs.baselineImgPath:",pathRefs.actionizeTemplateImgPath)
        console.log("pathRefs.runTimeImgPath:",pathRefs.actionizeRuntimePath)
        console.log("pathRefs.resultPath:",pathRefs.actionizeResultsPath)
        console.log("pathRefs.reportsPath:",pathRefs.actionizeReportsPath)
        //this.diffImgPath = path.join(this.imgOpsSessionRootPath, runtimePathSubstr, "diff");
        //this.resultPath = path.join(this.imgOpsSessionRootPath, this.resultPath);
        //this.resultPath = this.runTimeImgPath;
        //pathRefs.resultsRootPath = this.resultPath
        //this.pathRefs.resultPath = path.join(this.resultPath, "img-capture-results")
        //pathRefs.resultPath = path.join(this.resultPath)
        
        this.createActionizePaths()
        if(typeof di_pyImgLib == typeof di_pyImgCreativeLib){
            //console.log("activated di type : di_pyImgCreativeLib")
        }
        if(di_pyImgLib instanceof di_pyImgCreativeLib){
            //console.log("di_pyImgLib instace type : di_pyImgCreativeLib")
        }
        if(di_pyImgLib !instanceof di_pyImgCreativeLib){
        }
    }
    catch(err){
        console.error("********************ImageVision error location : pyCVLibrary | buildfeatureImgPaths()********************************")
        console.error(`error message: ${err.name}:${err.message}`)
        console.error("stack:",err.stack)
        console.error("*********************************************************************************************************************")
        return null;
    }
}

            /*              Hang Issue Check library       */
    
    public buildHangIssueCheckerPath(di_pyHangIssueCheckerLib: di_pyHangIssueCheckerLib){

        if(di_pyHangIssueCheckerLib.runtime_img_path == undefined || di_pyHangIssueCheckerLib.runtime_img_path == "")
             di_pyHangIssueCheckerLib.runtime_img_path = pathRefs.hangIssueChecker_RuntimePath
        else if(di_pyHangIssueCheckerLib.runtime_img_path != "")
             pathRefs.hangIssueChecker_RuntimePath = di_pyHangIssueCheckerLib.runtime_img_path 

        pathRefs.hangIssueChecker_ResultsPath = pathRefs.hangIssueChecker_RuntimePath
        pathRefs.hangIssueChecker_ReportsPath = pathRefs.hangIssueChecker_RuntimePath

        di_pyHangIssueCheckerLib.net_result_path = pathRefs.hangIssueChecker_ResultsPath
        di_pyHangIssueCheckerLib.hang_issue_reports_path = pathRefs.hangIssueChecker_ReportsPath 

        fsh.ensureDirExistsSync(pathRefs.hangIssueChecker_RuntimePath)
        fsh.ensureDirExistsSync(pathRefs.hangIssueChecker_ResultsPath)
        fsh.ensureDirExistsSync(pathRefs.hangIssueChecker_ReportsPath)


        /* commented for later enhancements  */
        
        /* 
        if(di_pyHangIssueCheckerLib.runtime_img_path == undefined || di_pyHangIssueCheckeib.runtime_img_path == "")
            di_pyHangIssueCheckerLib.runtime_img_path = pathRefs.hangIssueChecker_RuntimePath
        
        if(di_pyHangIssueCheckerLib.net_result_path == null || di_pyHangIssueCheckerLib.net_result_path == "")
            di_pyHangIssueCheckerLib.net_result_path = pathRefs.hangIssueChecker_ResultsPath
        
        if(di_pyHangIssueCheckerLib.hang_issue_reports_path == null || di_pyHangIssueCheckerLib.hang_issue_reports_path == "")
            di_pyHangIssueCheckerLib.hang_issue_reports_path = pathRefs.hangIssueChecker_ReportsPath
        */
    }

            /*              RT library       */

    public buildRTPaths(di_pyActionizeLib: di_pyImgInteractLib, dirCustomName=""){
        this.buildRTBaselinePath(di_pyActionizeLib)
        this.buildRTRuntimePath(di_pyActionizeLib, dirCustomName)
    }


    private buildRTBaselinePath(di_pyActionizeLib: di_pyImgInteractLib){
        try{
            let tmp_baseline_path = ""
            let RT_pos_baseline = di_pyActionizeLib.RT_anomaly_detection.positive_conditions.baseline_path
            let RT_neg_baseline = di_pyActionizeLib.RT_anomaly_detection.negative_conditions.baseline_path

            tmp_baseline_path = this.getBaselineFeaturePath(di_pyActionizeLib);
            tmp_baseline_path = path.join(tmp_baseline_path, "realtime")
            tmp_baseline_path = this.addBrowserToPath(di_pyActionizeLib, tmp_baseline_path)

            let baselineImgPathPos = path.join(pathRefs.baselineRootPath, tmp_baseline_path, "baseline", "positive");
            let baselineImgPathNeg = path.join(pathRefs.baselineRootPath, tmp_baseline_path, "baseline", "negative");
            
           
            fsh.ensureDirExistsSync(baselineImgPathPos)
            fsh.ensureDirExistsSync(baselineImgPathNeg)
            di_pyActionizeLib.RT_anomaly_detection.positive_conditions.baseline_path = baselineImgPathPos
            di_pyActionizeLib.RT_anomaly_detection.negative_conditions.baseline_path = baselineImgPathNeg
            pathRefs.RT_PositiveBaselinePath = baselineImgPathPos
            pathRefs.RT_NegativeBaselinePath = baselineImgPathNeg
        }
        catch(err){
            console.error("********************ImageVision error location : pyCVLibrary | buildRTBaselinePath()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("*********************************************************************************************************************")
            return null;
        }

    }


    private buildRTRuntimePath(di_pyActionizeLib:di_pyImgInteractLib, dirCustomName="") : void|null
    {
        try{
            let RT_reportsPath = di_pyActionizeLib.RT_anomaly_detection.reports_path
            let RT_resultsPath = di_pyActionizeLib.RT_anomaly_detection.net_result_path
            let RT_runtimePath = di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path

            let dt = new Date();
            let dateTimeStamp = dt.getDay().toString()+(dt.getMonth()+1).toString()+dt.getFullYear().toString()+"_"+dt.getHours().toString()+dt.getMinutes().toString()+dt.getSeconds().toString();
            let runtimePathSubstr = "", runtimeImgPathPos = "", runtimeImgPathNeg = "";

            /* block for building runtime path */

            runtimePathSubstr = this.getSessionID();
            runtimePathSubstr = this.getFeature_DirLabel_Path(dirCustomName, di_pyActionizeLib, dateTimeStamp)
            runtimePathSubstr = path.join(runtimePathSubstr, "realtime")
            runtimePathSubstr = this.addBrowserToPath(di_pyActionizeLib, runtimePathSubstr)
            console.log("check this- runtimePathSubstr:",runtimePathSubstr)
          
            
            let imgOpsSessionRootPath = this.getImgArchivesRootPath(di_pyActionizeLib)
            pathRefs.imgArchivesPath =  path.join(this.imgOpsSessionRootPath)
            pathRefs.imgOpsSessionRootPath = path.join(this.imgOpsSessionRootPath)

            // if(di_pyActionizeLib.realtime_mode == "true" && di_pyActionizeLib.RT_anomaly_detection.neg_condition_check_mode.toLowerCase() == "true") {
            //    pathRefs.RT_RuntimeImgsPath = path.join(imgOpsSessionRootPath, runtimePathSubstr, "runtime", "negative");
            // }
            // else{
            //     pathRefs.RT_RuntimeImgsPath = path.join(imgOpsSessionRootPath, runtimePathSubstr, "runtime", "positive");
            // }
            pathRefs.RT_ResultsPath = pathRefs.RT_RuntimeImgsPath
            pathRefs.RT_ReportsPath = pathRefs.RT_RuntimeImgsPath

            di_pyActionizeLib.RT_anomaly_detection.runtime_imgs_path = pathRefs.RT_RuntimeImgsPath
            di_pyActionizeLib.RT_anomaly_detection.net_result_path = pathRefs.RT_ResultsPath
            di_pyActionizeLib.RT_anomaly_detection.reports_path = pathRefs.RT_ReportsPath
            
            console.log("runtimeeeeeeeeeeeeeeeee",pathRefs.RT_RuntimeImgsPath)
            fsh.ensureDirExistsSync(pathRefs.RT_RuntimeImgsPath)
            
            console.log("pathRefs.baselineImgPath-pos:",pathRefs.RT_PositiveBaselinePath)
            console.log("pathRefs.baselineImgPath-neg:",pathRefs.RT_NegativeBaselinePath)
            console.log("pathRefs.runTimeImgPath:",pathRefs.RT_RuntimeImgsPath)
            console.log("pathRefs.RT_resultPath:",pathRefs.RT_ResultsPath)
            console.log("pathRefs.RT_reportsPath:",pathRefs.RT_ReportsPath)
        }
        catch(err){
            console.error("********************ImageVision error location : pyCVLibrary | buildRTRuntimePath()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("*********************************************************************************************************************")
            return null;
        }
}


    
}



/***********Temp code *******
*await browser.driver.sleep(1000)
        await browser.wait(ExpectedConditions.visibilityOf(this.canvas.first().baseElement), 5000)
        let act_ImgFile = this.imagePathRepository.pyGetImagePath(WidgetType.logWidget, "buildjs")[0] + imageName;
        if (type.toLowerCase() == 'time') {

            // JsHelper.takeCroppedScreenShot(element.all(by.tagName('canvas')).get(0),{x:100,y:470},{x:330,y:0},"rightFill")  
            let size = await this.canvas.get(0).getSize();
            let img = await this.canvas.get(0).getLocation()
            this.writeScreenShot(img, this.imagePathRepository.pyGetImagePath(WidgetType.logWidget, "buildjs")[0] + imageName);
        }

        if (type.toLowerCase() == 'depth') {
            //let img = await this.canvas.get(1).takeScreenshot()
            let size = await this.canvas.get(1).getSize();
            let img = await this.canvas.get(1).getLocation()
            this.writeScreenShot(img, this.imagePathRepository.pyGetImagePath(WidgetType.logWidget, "buildjs")[0] + imageName);
            // JsHelper.takeCroppedScreenShot(element.all(by.tagName('canvas')).get(0),{x:100,y:470},{x:330,y:0},"rightFill")  
            //return this.canvas.get(1).getSize().then(size => this.poseidon.testServicesForImage.takeElementScreenShot(this.canvas.get(1), imageName, new ImagePathRepository().getImagePath(WidgetType.logWidget, "buildjs")[0]));
        }
**************************/

//**********Experimented - 20-Jul-2020 12:15 AM***************************** */
/*let scx = await browser.executeScript('var xx =  window.screenX;return xx;');
        let scy = await browser.executeScript('var xx =  window.screenY;return xx;');
        let scrx = await browser.executeScript('var xx =  window.scrollX;return xx;');
        let scry = await browser.executeScript('var xx =  window.scrollY;return xx;');
        let scTop = await browser.executeScript('var xx =  window.screenTop;return xx;');
        let scLeft = await browser.executeScript('var xx =  window.screenLeft;return xx;');

      /*console.log("scx:",scx);
        console.log("scy:",scy);
        console.log("scrx:",scrx);
        console.log("scry:",scry);
        console.log("scTop:",scTop);
        console.log("scLeft:",scLeft);
        //console.log("screen X:",window.screenX,"screen Y:",window.screenY, "scroll X:",window.scrollX, "scroll Y:",window.scrollY)
        //console.log("screen top:",window.screenTop, "screen left:",window.screenLeft);
        //let x2 = x1 + (size.width - x1), y2 = (y1 + size.height - y1);
        //x1 = x1 + parseInt(scrHeight);
******************************************************************************/


/**********************************29-Jul-2020 1:40 AM**************************************
 *      //pyImgCreativeCLIArgs = " -f " + imgFile + " -tx " + x1 + " -ty " + y1 + " -bx " + x2 + " -by " + y2;
        //pyImgCreativeCLIArgs = "";
        //console.log(" pyImgCreativeCLIArgs:",pyImgCreativeCLIArgs);
        let options = {          //options for pythonshell package
                mode: 'text',
                //pythonPath: '',
                pythonPath: 'C:/Program\ Files/Python-3.7.4',
                pythonOptions: ['-u'], // get print results in real-time
                scriptPath: path.join(browser.params.baseDir, '..', 'py'),
                args: [" -f " + di_pyImgCreativeLib.imgFile, " -tx " + x1 , " -ty " + y1 , " -bx " + x2 , " -by " + y2]
        };

************************************************************************************/

/***********************************14-Dec-2020 01:50 AM ******************************/
  /* private getBaselineScenarioPath(di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib, pathSubstr:string):string 
       {
            let tmp_path = ""
            if(di_pyImgLib.uiObjSnap == "true"){
                tmp_path = path.join(pathSubstr, "uiobj");
            }
            else if(di_pyImgLib.realtime == "true"){
                tmp_path = path.join(pathSubstr, "realtime")
            }
            else if(di_pyImgLib.realtime == "false" && di_pyImgLib.uiObjSnap == "false"){
                tmp_path =  path.join(pathSubstr, "historical")
            }
            return tmp_path
       }

       private addBrowserToBaselinePath(di_pyImgLib : di_pyImgCreativeLib | di_pyImgCompLib | di_pyImgInteractLib, pathSubstr:string):string {
        let tmp_path = ""
        if(di_pyImgLib.browserDependent == "true"){
            let browserName = helper.testRunCache.readKey("currentBrowser");
            tmp_path = path.join(pathSubstr, browserName)
        }
        else 
            tmp_path = pathSubstr
        return tmp_path
   }
   *************************************************************************************/
