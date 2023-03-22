/******************** 
* Author : Yusuf
* Authored on : 20-Jul-2020 11:25 AM
* Updates on   : 20-Jul-2020 04:30 PM,21-Jul-2020 01:00 PM, 22-Jul-2020, 23-Jul-2020 02:45 AM, 04-Aug-2020 03:45 AM, 05-Aug-2020 03:10 AM, 09-Dec-2020 10:05 AM, 11-Dec-2020 12:50 AM, 12-Dec-2020 04:15 PM, 13-Dec-2020 02:10 AM, 15-Dec-2020 12:25 PM, 26-Dec-2020 01:25 AM
* Depdendency Injection for py CV image library
*
*********************/


import * as fse from 'fs-extra';
import { browser, by, protractor,ExpectedConditions } from "protractor";
import * as path from "path";
import * as cp from 'child_process';
//import {PythonShell} from 'python-shell';
import * as fs from 'fs';
import { fs_helper as fsh, fs_helper} from "../helpers/fs_helper"
import { async } from 'q';
import { AppFeatures_CV } from "./appfeatures_cv";
import { pathRefs } from './pathRefs';

export class di_pyImgCreativeLib{
    private  resetToDefaultLocal = "false";
    constructor(){
      this.realtimeImgGrabDurationMins = "0"
      this.realtime = "false"
      this.uiObjSnap = "false"
    }
    
    private argFile = path.join(browser.params.baseDir,'..', "py/cv-img-grab/img-cap-args.json")
    //private dt = require(this.argFile)
    private dt = JSON.parse(fs.readFileSync(this.argFile, 'utf-8'))
    private _appFeatures_CV = null
    private _imgFile = ""
    private _imgArchivesPath = ""
    private _cycles = "1"
    private _realtimeImgGrabDurationMins = "0"
    private _interval = "0"
    private _maskRegionExcluding = ""
    private _maskRegion = ""
    private _browserDependent = "true"
    private _approvedAsBaseline = "true"
    private _baselineImage = ""
    private _failTestOnBaselineAutoApproval = "false"
    private _realtime = "false"
    private _uiObjSnap = "false"
    private _imgCapResultPath = ""
    private _resetToDefault = this.resetToDefaultLocal
    private _failCurrentTestOnFailedImgOp = "true"
    private _overwriteBaseline = "false"
    //private fname = this.dt["args"][0]["imgFile"].split('/').last()

    appFeatures_CV = ""
    imgFile = ""
    imgArchivesPath = ""
    cycles = "1"
    realtimeImgGrabDurationMins = "0"
    interval = "0"
    maskRegionExcluding = ""
    maskRegion = ""
    browserDependent = "true"
    approvedAsBaseline = "true"
    baselineImage = ""
    failTestOnBaselineAutoApproval = "false"
    realtime = "false"
    uiObjSnap = "false"
    imgCapResultPath = ""
    resetToDefault = this.resetToDefaultLocal
    failCurrentTestOnFailedImgOp = "true"
    overwriteBaseline = "false"
    

    resetConfig(di_pyImgCreativeLib:di_pyImgCreativeLib){
        /*if(di_pyImgCreativeLib.appFeatures_CV != "" || di_pyImgCreativeLib.appFeatures_CV != null)
            this.appFeatures_CV = di_pyImgCreativeLib.appFeatures_CV
        else
            this.appFeatures_CV = this._appFeatures_CV*/
        this.appFeatures_CV = ""
        this.imgFile = ""
        this.imgArchivesPath = ""
        this.cycles = "1"
        this.realtimeImgGrabDurationMins = "0"
        this.interval = "0"
        this.maskRegionExcluding = ""
        this.maskRegion = ""
        this.uiObjSnap = "false"
        this.browserDependent = "true"
        this.approvedAsBaseline = "true"
        this.baselineImage = ""
        this.failTestOnBaselineAutoApproval = "false"
        this.realtime = "false"
        this.imgCapResultPath = ""
        this.failCurrentTestOnFailedImgOp = "true"
        this.overwriteBaseline = "false"
        this.resetToDefault = this.resetToDefaultLocal

        this._appFeatures_CV = ""
        this._imgFile = ""
        this._imgArchivesPath = ""
        this._cycles = "1"
        this._realtimeImgGrabDurationMins = "0"
        this._interval = "0"
        this._maskRegionExcluding = ""
        this._maskRegion = ""
        this._uiObjSnap = "false"
        this._browserDependent = "true"
        this._approvedAsBaseline = "true"
        this._baselineImage = ""
        this._failTestOnBaselineAutoApproval = "false"
        this._realtime = "false"
        this._imgCapResultPath = ""
        this._failCurrentTestOnFailedImgOp = "true"
        this._overwriteBaseline = "false"
        this._resetToDefault = this.resetToDefaultLocal
        //pathRefs.imgGrabOpResult = false
        //pathRefs.imgCompOpResult = false
        //pathRefs.visActionOpResult = false
        console.log("image creation  - reset to default values....done")
    }
    
    getCurrentConfigs():IpyImgCreativeLib{
        let fname_arr = this.dt["args"][0]["imgFile"].split('/')
        let fname = fname_arr[fname_arr.length-1]
        let di_py = {
            appFeatures_CV: this.dt["args"][0]["appFeatures_CV"],
            imgFile: this.dt["args"][0]["imgFile"],
            imgArchivesPath: this.dt["args"][0]["imgArchivesPath"],
            cycles: this.dt["args"][0]["cycles"],
            realtimeImgGrabDurationMins:this.dt["args"][0]["realtimeImgGrabDurationMins"],
            interval:this.dt["args"][0]["interval"],
            maskRegionExcluding : this.dt["args"][0]["maskRegionExcluding"],
            maskRegion : this.dt["args"][0]["maskRegion"],
            uiObjSnap:this.dt["args"][0]["uiObjSnap"],
            browserDependent:this.dt["args"][0]["browserDependent"],
            approvedAsBaseline:this.dt["args"][0]["approvedAsBaseline"],
            baselineImage:this.dt["args"][0]["baselineImage"],
            failTestOnBaselineAutoApproval:this.dt["args"][0]["failTestOnBaselineAutoApproval"],
            realtime:this.dt["args"][0]["realtime"],
            imgCapResultPath:this.dt["args"][0]["imgCapResultPath"],
            failCurrentTestOnFailedImgOp:this.dt["args"][0]["failCurrentTestOnFailedImgOp"],
            overwriteBaseline:this.dt["args"][0]["overwriteBaseline"],
            resetToDefault : this.resetToDefault,

            _appFeatures_CV : this.dt["args"][0]["appFeatures_CV"],
            _imgFile : this.dt["args"][0]["imgFile"],
            _imgArchivesPath : this.dt["args"][0]["imgArchivesPath"],
            _cycles : this.dt["args"][0]["cycles"],
            _realtimeImgGrabDurationMins : this.dt["args"][0]["realtimeImgGrabDurationMins"],
            _interval : this.dt["args"][0]["interval"],
            _maskRegion : this.dt["args"][0]["maskRegion"],
            _maskRegionExcluding : this.dt["args"][0]["maskRegionExcluding"],
            _browserDependent : this.dt["args"][0]["browserDependent"],
            _approvedAsBaseline : this.dt["args"][0]["approvedAsBaseline"],
            _baselineImage : this.dt["args"][0]["baselineImage"],
            _failTestOnBaselineAutoApproval : this.dt["args"][0]["failTestOnBaselineAutoApproval"],
            _realtime : this.dt["args"][0]["realtime"],
            _uiObjSnap : this.dt["args"][0]["uiObjSnap"],
            _imgCapResultPath : this.dt["args"][0]["imgCapResultPath"],
            _failCurrentTestOnFailedImgOp : this.dt["args"][0]["failCurrentTestOnFailedImgOp"],
            _overwriteBaseline : this.dt["args"][0]["overwriteBaseline"],
            _resetToDefault : this.resetToDefault

        };
        return di_py;
    }
}

export interface IpyImgCreativeLib {
    appFeatures_CV:AppFeatures_CV;
    imgFile:string;
    imgArchivesPath:string;
    cycles:string;
    realtimeImgGrabDurationMins:string;
    interval:string;
    maskRegionExcluding:string;
    maskRegion:string;
    browserDependent:string;
    approvedAsBaseline:string;
    baselineImage:string;
    failTestOnBaselineAutoApproval:string;
    realtime:string;
    uiObjSnap:string;
    imgCapResultPath:string;
    failCurrentTestOnFailedImgOp:string;
    overwriteBaseline:string;
    resetToDefault:string;
}

    
/******************Temporary-experimental code************************
    
    /*static get imgFile1():string {
        console.log("argList - JSON object:",this.dt);
        let fname = this.dt["args"][0]["imgFile"].split('/').last();
        console.log(path.join(browser.params.imgArchivesPath,fname));
        return path.join(browser.params.imgArchivesPath,fname);
    }

    static set imgFile2(abc:string) {
        console.log("argList - JSON object:",this.dt);
        let fname = this.dt["args"][0]["imgFile"].split('/').last();
        console.log(path.join(browser.params.imgArchivesPath,fname));
        //return path.join(browser.params.imgArchivesPath,fname);
    }

    get cycles():string {
        let cycles = this.dt["args"][0]["cycles"];
        console.log("cycles",cycles);
        return cycles;
    }

    get realtimeImgGrabDurationMins():string {
        let duration = this.dt["args"][0]["realtimeImgGrabDurationMins"];
        console.log("cycles",duration);
        return duration;
    }

    get interval():string {
        let cycles = this.dt["args"][0]["cycles"];
        console.log("cycles",cycles);
        return cycles;
    }


    /*if(this._imgFile==""){
            this._appFeatures_CV = this.dt["args"][0]["appFeatures_CV"]
            this._imgFile = this.dt["args"][0]["imgFile"]
            console.log("----------------------------------------------"+this._imgFile)
            this._imgArchivesPath = ""
            this._cycles = this.dt["args"][0]["cycles"]
            this._realtimeImgGrabDurationMins = this.dt["args"][0]["realtimeImgGrabDurationMins"]
            this._interval = this.dt["args"][0]["interval"]
            this._maskRegion = this.dt["args"][0]["maskRegion"]
            this._maskRegionExcluding = this.dt["args"][0]["maskRegionExcluding"]
            this._browserDependent = this.dt["args"][0]["browserDependent"]
            this._approvedAsBaseline = this.dt["args"][0]["approvedAsBaseline"]
            this._baselineImage = this.dt["args"][0]["baselineImage"]
            this._failTestOnBaselineAutoApproval = this.dt["args"][0]["failTestOnBaselineAutoApproval"]
            this._realtime = this.dt["args"][0]["realtime"]
            this._uiObjSnap = this.dt["args"][0]["uiObjSnap"]
            this._imgCapResultPath = ""
            this._failCurrentTestOnFailedImgOp = this.dt["args"][0]["failCurrentTestOnFailedImgOp"]
            this._overwriteBaseline = this.dt["args"][0]["overwriteBaseline"]
            this._resetToDefault = this.resetToDefault
            let fname_arr = this.dt["args"][0]["imgFile"].split('/')
            let fname = fname_arr[fname_arr.length-1]
            this.appFeatures_CV = this.dt["args"][0]["appFeatures_CV"]
            this.imgFile = path.join(browser.params.imgArchivesPath, fname)
            console.log("----------------------------------------------"+this.imgFile)
            this.cycles = this.dt["args"][0]["cycles"]
            this.imgArchivesPath = ""
            this.realtimeImgGrabDurationMins = this.dt["args"][0]["realtimeImgGrabDurationMins"]
            this.interval = this.dt["args"][0]["interval"]
            this.maskRegion = this.dt["args"][0]["maskRegion"]
            this.maskRegionExcluding = this.dt["args"][0]["maskRegionExcluding"]
            this.browserDependent = this.dt["args"][0]["browserDependent"]
            this.approvedAsBaseline = this.dt["args"][0]["approvedAsBaseline"]
            this.baselineImage = this.dt["args"][0]["baselineImage"]
            this.failTestOnBaselineAutoApproval = this.dt["args"][0]["failTestOnBaselineAutoApproval"]
            this.realtime = this.dt["args"][0]["realtime"]
            this.uiObjSnap = this.dt["args"][0]["uiObjSnap"]
            this.imgCapResultPath = ""
            this.failCurrentTestOnFailedImgOp = this.dt["args"][0]["failCurrentTestOnFailedImgOp"]
            this.overwriteBaseline = this.dt["args"][0]["overwriteBaseline"]
            this.resetToDefault = this.resetToDefault
        }
******************************************************************/
