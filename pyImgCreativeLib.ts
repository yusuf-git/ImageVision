/******************** 
* Author : Yusuf
* Authored on : 28-Jul-2020 10:00 PM
* Upates on   : 02-Aug-2020 02:30 AM, 04-Aug-2020 03:50 AM, 06-Aug-2020 11:40 PM, 09-Dec-2020 09:45 AM to 11:50 PM, 10-Dec-2020 01:50 AM, 13-Dec-2020 02:10 AM, 14-Dec-2020 02:00 AM, 08:45 PM, 15-Dec-2020 02:00 AM, 17-Dec-2020 08:15 PM, 19-Dec-2020 11:05 PM, 23-Dec-2020 01:50 AM, 22-Nov-2021 01:30 AM, 20-Dec-2021 05:35 PM
* Lib for capturing images with python CV library 
*
*********************/

/*future improvements(recorded on 20-Jul-2020 12:45 AM):
    - support for protractor parallelism while calling python img lib through cmd and static img-cap-args.json
    - create REST APIs for python img lib and call them
    - immediate - crop the specified portion of the captured image - for time scale real-time scenarios
*/

import * as fse from 'fs-extra';
//import { KognifaiCoreReg as kognifaiCore } from "../factory/KognifaiCoreRegistory";
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
import {pathRefs} from './pathRefs';
import { helper } from "kognifai-automation-framework";
import { pyCVLibrary } from './pyCVLibrary';

export class pyImgCreativeLib {

        pathRefs = visionRegistry.pathRefs
        private pyCVLib = visionRegistry.pyCVLib
        private x1 = 0
        private y1 = 0
        private x2 = 0
        private y2 = 0
        private imageVision_ver = "ImageVision v6"
      
        public async pyGrabImage(el:IElementWrapper, imgFile:string, di_pyImgCreativeLib: di_pyImgCreativeLib, dirCustomName="") : Promise<boolean>
        {
            try 
            {
                console.log("")
                console.log("")
                console.log("*******************************************************pyGrabImage OPERATION BEGINS*************************************************************************************")
                console.log("")
                console.log("")
                console.log("element name:",await el.getText())
                console.log("image name:",di_pyImgCreativeLib.imgFile)

                this.resetStandardPathRefPaths()

                /*populate all types of image paths for referencing later*/
                await this.pyCVLib.addBrowserEntry();
                console.log("added active browser name to cache :"+helper.testRunCache.readKey("currentBrowser"));
                this.pyCVLib.buildfeatureImgPaths(di_pyImgCreativeLib, dirCustomName);
                
                /*If the current image is not present in the baseline path, create the baseline in the respective path*/
                if(di_pyImgCreativeLib.approvedAsBaseline.toLowerCase() == "true"){
                    di_pyImgCreativeLib.baselineImage = path.join(pathRefs.baselineImgPath,imgFile);
                }
                di_pyImgCreativeLib.imgFile = path.join(this.pyCVLib.runTimeImgPath,imgFile);
                pathRefs.runtime_img = di_pyImgCreativeLib.imgFile;
                pathRefs.baseline_img = path.join(pathRefs.baselineImgPath, imgFile)
                console.log("check1 - pathRefs.baseline_img: ", pathRefs.baseline_img)
                console.log("check2 - pathRefs.runtime_img: ", pathRefs.runtime_img)
                
                /* Set the runtime path for Hang Issue Checker so that it will be implicitly used  anytime later by Hang Issue Checker*/
                pathRefs.hangIssueChecker_RuntimePath = pathRefs.runTimeImgPath
                pathRefs.RT_RuntimeImgsPath=pathRefs.runTimeImgPath
                /************************************************************* */


                di_pyImgCreativeLib = this.conditionallySetFlags(di_pyImgCreativeLib)
                
                if(di_pyImgCreativeLib.uiObjSnap == "true" || (di_pyImgCreativeLib.realtime == "false" && di_pyImgCreativeLib.uiObjSnap == "false")){
                    di_pyImgCreativeLib.cycles = "1"
                }
                if(di_pyImgCreativeLib.realtime == ''){
                    di_pyImgCreativeLib.realtime = "false"
                }
                if(di_pyImgCreativeLib.uiObjSnap == ''){
                    di_pyImgCreativeLib.uiObjSnap = "false"
                }
                if(di_pyImgCreativeLib.realtimeImgGrabDurationMins == "" ){
                    di_pyImgCreativeLib.realtimeImgGrabDurationMins = "0"
                }
                if(di_pyImgCreativeLib.interval == ""){
                    di_pyImgCreativeLib.interval = "0"
                }
                if(di_pyImgCreativeLib.cycles == ""){
                    di_pyImgCreativeLib.cycles = "1"
                }
                di_pyImgCreativeLib.imgArchivesPath = pathRefs.imgOpsSessionRootPath;
                di_pyImgCreativeLib.imgCapResultPath = pathRefs.resultPath;

                let pyArgsJsonFile = path.join(browser.params.baseDir,'..', "py/cv-img-grab/img-cap-args.json")
                let pyImgBatFile = path.join(browser.params.baseDir,'..', "py/cv-img-grab/pyImgCreative.bat") 
                let promptChangerBat = path.join(browser.params.baseDir,'..', "py/cv-img-grab/prompt.bat") 
            
                console.log("baseline path:",pathRefs.baselineImgPath);
                console.log("runtime path:",pathRefs.runTimeImgPath);
                console.log("reports path:",pathRefs.reportsPath);
                console.log("appFeatures_CV:",di_pyImgCreativeLib.appFeatures_CV);

                await this.getUIBoundingRect(el)
                let dt = this.unpackDI(di_pyImgCreativeLib, pyArgsJsonFile, this.x1,this.y1,this.x2,this.y2);
                let strData = JSON.stringify(dt);
                console.log("----------------------------------------------")
                await this.pyCVLib.writeToPyArgsFile(pyArgsJsonFile,strData);
                await this.pyCVLib.runPromptChanger(promptChangerBat);
                await this.pyCVLib.pyRun(pyImgBatFile,pyArgsJsonFile);
                console.log("----------------------------------------------")
               
                /* check the result file - if present, read it and set the test outcome accordingly */ 
                let result = this.getImgGrabResult(di_pyImgCreativeLib)
                console.log("image :"+ path.basename(di_pyImgCreativeLib.imgFile)+" --> capture operation result:"+result);

                if(result && di_pyImgCreativeLib.approvedAsBaseline.toLowerCase() == "true" && di_pyImgCreativeLib.failTestOnBaselineAutoApproval.toLowerCase() == "true")
                    expect(`unapproved auto-baseline`).toEqual('approved baseline', `image auto-baselined : true, should test fail ? : true`)

                if(di_pyImgCreativeLib.resetToDefault == "true")
                {
                    di_pyImgCreativeLib.resetConfig(di_pyImgCreativeLib);
                    console.log("ImageVision | ImageGrab : reset the configs to default....done")
                }

                console.log("")
                console.log("")
                console.log("*************************************END OF pyGrabImage OPERATION***********************************************************************************")
                this.x1 = 0, this.y1=0, this.x2=0, this.y2=0
                return result
        }
        catch(err){
            console.error("********************ImageVision error location : pyGrabImage()********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("***************************************************************************************************")
            throw new Error(`ImageVision | ImageGrab error : ${err.name}:${err.message}`)
        }
    } 


    private resetStandardPathRefPaths(){
        pathRefs.runTimeImgPath = ""
        pathRefs.runtime_img = ""
        pathRefs.baselineImgPath = ""
        pathRefs.baseline_img = ""
        pathRefs.reportsPath = ""
        pathRefs.resultPath = ""
        pathRefs.imgGrabOpResult = false
    }

    private async getUIBoundingRect(el:IElementWrapper)
    {
        let size = await el.getSize();
        let loc = await el.getLocation()
        console.log("size.width, size.height: ", size.width, size.height)
        this.x1 = loc.x, this.y1 = loc.y;
        let bound = await browser.executeScript("return arguments[0].getBoundingClientRect();", el.getWebElement());
        let scrHeight:string = await browser.executeScript('return window.outerHeight - window.innerHeight;');
        console.log("Full screen offset height :",scrHeight);
        console.log("bounding rect:",bound);
        console.log("Orig x1,y1:",this.x1,this.y1);
        this.y1 = this.y1 + parseInt(scrHeight);
        this.x2 = this.x1 + (size.width), this.y2 = this.y1 + (size.height);
        console.log("Original x2, y2:", this.x2, this.y2)
        //Commenting below due to screen cropping issue in SDP/Live, commented 19th March, 2021
        // if(this.x2 > 1920){
        //     this.x2 = 1920
        // }
        return;
    }

    
    private conditionallySetFlags(di_pyImgCreativeLib:di_pyImgCreativeLib) : di_pyImgCreativeLib
    {
        if(di_pyImgCreativeLib.realtime == "true" && di_pyImgCreativeLib.uiObjSnap == "true")
            di_pyImgCreativeLib.uiObjSnap = "false"
        //if(di_pyImgCreativeLib.uiObjSnap = "true")
          //  di_pyImgCreativeLib.realtime == "false"
        if(di_pyImgCreativeLib.maskRegion != "")
            di_pyImgCreativeLib.maskRegionExcluding = ""
        if(di_pyImgCreativeLib.maskRegionExcluding != "")
            di_pyImgCreativeLib.maskRegion = ""
        if(di_pyImgCreativeLib.approvedAsBaseline == "false")
            di_pyImgCreativeLib.failTestOnBaselineAutoApproval="false"
            di_pyImgCreativeLib.overwriteBaseline == "false"
        
        return di_pyImgCreativeLib;
    }

    private unpackDI(di_pyImgCreativeLib:di_pyImgCreativeLib, argFile, x1, y1, x2, y2) : di_pyImgCreativeLib | null
    {
        try
        {
            //let dt = require(argFile);
            let dt = JSON.parse(fs.readFileSync(argFile, 'utf-8'))
            dt["args"][0]["appFeatures_CV"] = di_pyImgCreativeLib.appFeatures_CV;
            dt["args"][0]["imgFile"] = di_pyImgCreativeLib.imgFile;
            dt["args"][0]["cycles"] = di_pyImgCreativeLib.cycles;
            dt["args"][0]["imgArchivesPath"] = di_pyImgCreativeLib.imgArchivesPath;
            dt["args"][0]["realtimeImgGrabDurationMins"] = di_pyImgCreativeLib.realtimeImgGrabDurationMins;
            dt["args"][0]["interval"] = di_pyImgCreativeLib.interval;
            dt["args"][0]["browserDependent"] = di_pyImgCreativeLib.browserDependent;
            dt["args"][0]["approvedAsBaseline"] = di_pyImgCreativeLib.approvedAsBaseline;
            dt["args"][0]["baselineImage"] = di_pyImgCreativeLib.baselineImage;
            dt["args"][0]["failTestOnBaselineAutoApproval"] = di_pyImgCreativeLib.failTestOnBaselineAutoApproval;
            dt["args"][0]["maskRegionExcluding"] = di_pyImgCreativeLib.maskRegionExcluding;
            dt["args"][0]["maskRegion"] = di_pyImgCreativeLib.maskRegion;
            dt["args"][0]["uiObjSnap"] = di_pyImgCreativeLib.uiObjSnap;
            dt["args"][0]["resultPath"] = di_pyImgCreativeLib.imgCapResultPath;
            dt["args"][0]["realtime"] = di_pyImgCreativeLib.realtime;
            dt["args"][0]["failCurrentTestOnFailedImgOp"] = di_pyImgCreativeLib.failCurrentTestOnFailedImgOp;
            dt["args"][0]["overwriteBaseline"] = di_pyImgCreativeLib.overwriteBaseline;
            dt["args"][0]["x1"] = x1.toString();
            dt["args"][0]["y1"] = y1.toString();
            dt["args"][0]["x2"] = x2.toString();
            dt["args"][0]["y2"] = y2.toString();
            return dt;
        }
        catch(err){
            console.error("********************ImageVision error location : unpackDI() i.e. reading img-cap-args.json********************************")
            console.error(`error message: ${err.name}:${err.message}`)
            console.error("stack:",err.stack)
            console.error("**************************************************************************************************************************")
            throw new Error(`ImageVision | ImageGrab  error : ${err.name}:${err.message}`)
        }
    }

    private readCaptureResult(di_pyImgCreativeLib:di_pyImgCreativeLib):any
    {
        let resultFile = path.join(pathRefs.resultPath, path.basename(di_pyImgCreativeLib.imgFile).split(".")[0]+"-cap.json")
        let result_dt : any = null;
        console.log("result file:"+resultFile);
        if(!fsh.pathExistsSync(resultFile))
        {
            console.log("unable to locate result file :"+resultFile);
            if(di_pyImgCreativeLib.failCurrentTestOnFailedImgOp.toLowerCase() == "true")
                expect(`${this.imageVision_ver} - no result file`).toEqual(`${this.imageVision_ver} - result file should be present`,`${this.imageVision_ver} - unable to locate image creation resultFile:`+resultFile);
            return result_dt;
        }
        //result_dt = require(resultFile);
        result_dt = JSON.parse(fs.readFileSync(resultFile, 'utf-8'))
        return result_dt;
    }

    private getImgGrabResult(di_pyImgCreativeLib:di_pyImgCreativeLib):boolean
    {   
        let result = false
        let result_dt = this.readCaptureResult(di_pyImgCreativeLib);
        if(result_dt["result"].toString().toLowerCase() == "true")
            result = true;
        else if(result_dt["result"].toString().toLowerCase() == "false" && di_pyImgCreativeLib.failCurrentTestOnFailedImgOp.toLowerCase() == "true")
            expect(`${this.imageVision_ver} - failed image creation`).toEqual(`${this.imageVision_ver} - successful image creation`,`${this.imageVision_ver} - image creation operation failed - img:` + path.join(di_pyImgCreativeLib.imgFile));
        pathRefs.imgGrabOpResult = result;
        return result;
        //let result_msg:Array<boolean | string>;
        //result_msg.push(result)
        //result_msg.push(result_dt[0]["message"].toString())
    }

    /*private async writeToPyArgsFile(pyArgsFile, strData): Promise<boolean> {
        let result =false;
        await new Promise( (resolve,reject) => {
            try{
                fs.writeFile(pyArgsFile, strData, 'utf8', (err) => {
                    if (err) {
                        reject("ERROR ::: Writing to python img-cap-args.json :" + err);
                    }
                    else {
                        if(fsh.pathExistsSync(pyArgsFile)){
                            result = true;
                            resolve("Created python img-cap-args.json...OK");
                        }
                    }
                });
            }
            catch(e){
                console.log("python img-cap-args.json - error :",e);
            }
        })
        .then(() => console.log("Written to img-cap-args.json"))
        .catch((e) => console.log("Exception caught :: img-cap-args.json write",e));
        console.log("python img-cap-args.json update - result:",result);
        return result;
    }*/
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
****************************************************************************

async pyRun(pyImgBatFile, pyArgsJsonFile ) {
        //let pyImgCreativeBat = path.join(browser.params.baseDir,'..', "py/pyImgCreativeture.bat")
        let pyImgCreativeBat = path.join(browser.params.baseDir,'..', pyImgBatFile)
        //let cmd = `cmd /k `+pyImgCreativeBat+` -j img-cap-args.json`;
        let cmd = `cmd /k `+pyImgCreativeBat+` -j `+ pyArgsJsonFile;
        console.log("cmd:",cmd);
        var options = {
            cwd:'C:/windows/System32',
            stdio: 'inherit'
        };
        cp.execSync(cmd,options)
        console.log("done with pyRun()");
    }
        

******************************************************************************/

