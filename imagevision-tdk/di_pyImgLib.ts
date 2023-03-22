/******************** 
* Author : Yusuf
* Authored on : 20-Jul-2020 11:25 AM
* Updates on   : 20-Jul-2020 04:30 PM,21-Jul-2020 01:00 PM, 22-Jul-2020, 23-Jul-2020 02:45 AM, 20-Dec-2021 06:45 PM
* Depdendency Injection for py CV image library
*
*********************/


import * as fse from 'fs-extra';
import { browser, by, protractor,ExpectedConditions } from "protractor";
import * as path from "path";
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework";
import * as cp from 'child_process';
//import {PythonShell} from 'python-shell';
import * as fs from 'fs';
import { fs_helper as fsh, fs_helper} from "./../helpers//fs_helper"
import { async } from 'q';
import { AppFeatures_CV } from "./appfeatures_cv";

export class di_pyImgLib{ // renamed the class name on 10-Dec-2020 09:40 PM
    constructor(){
        if(this._imgFile==""){
            this._appFeatures_CV = this.dt["args"][0]["appFeatures_CV"]
            this._imgFile = this.dt["args"][0]["imgFile"]
            this._cycles = this.dt["args"][0]["cycles"]
            this._realtimeImgGrabDurationMins = this.dt["args"][0]["realtimeImgGrabDurationMins"]
            this._interval = this.dt["args"][0]["interval"]
            this._cropleft = this.dt["args"][0]["crop_box"]
            this._cropright = this.dt["args"][0]["crop_right"]
            this._croptop = this.dt["args"][0]["crop_top"]
            this._cropbottom = this.dt["args"][0]["crop_bottom"]
            let fname_arr = this.dt["args"][0]["imgFile"].split('/')
            let fname = fname_arr[fname_arr.length-1]
            this.appFeatures_CV = this.dt["args"][0]["appFeatures_CV"]
            this.imgFile = path.join(browser.params.imgArchivesPath, fname)
            this.cycles = this.dt["args"][0]["cycles"]
            this.realtimeImgGrabDurationMins = this.dt["args"][0]["realtimeImgGrabDurationMins"]
            this.interval = this.dt["args"][0]["interval"]
            this.crop_box = this.dt["args"][0]["crop_box"]
            this.crop_right = this.dt["args"][0]["crop_right"]
            this.crop_top = this.dt["args"][0]["crop_top"]
            this.crop_bottom = this.dt["args"][0]["crop_bottom"]
        }
    }
    private argFile = path.join(browser.params.baseDir,'..', "py/img-cap-args.json")
    //private dt = require(this.argFile)
    private dt = JSON.parse(fs.readFileSync(this.argFile, 'utf-8'))
    private _appFeatures_CV = null
    private _imgFile = ""
    private _cycles = ""
    private _realtimeImgGrabDurationMins = ""
    private _interval = ""
    private _cropleft = ""
    private _cropright = ""
    private _croptop = ""
    private _cropbottom = ""
    //private fname = this.dt["args"][0]["imgFile"].split('/').last()

    appFeatures_CV = null
    imgFile = ""
    cycles = ""
    realtimeImgGrabDurationMins = ""
    interval = ""
    crop_box = ""
    crop_right = ""
    crop_top = ""
    crop_bottom = ""

    setDefault(){
        this.appFeatures_CV = this._appFeatures_CV
        this.imgFile = this._imgFile
        this.cycles = this._cycles
        this.realtimeImgGrabDurationMins = this._realtimeImgGrabDurationMins
        this.interval = this._interval
        this.crop_box = this._cropleft
        this.crop_right = this._cropright
        this.crop_top = this._croptop
        this.crop_bottom = this._cropbottom
    }
    
    getValues():IpyImgLib{
        let fname_arr = this.dt["args"][0]["imgFile"].split('/')
        let fname = fname_arr[fname_arr.length-1]
        let di_py = {
            appFeatures_CV: this.dt["args"][0]["appFeatures_CV"],
            imgFile: path.join(browser.params.imgArchivesPath, fname),
            cycles: this.dt["args"][0]["cycles"],
            realtimeImgGrabDurationMins:this.dt["args"][0]["realtimeImgGrabDurationMins"],
            interval:this.dt["args"][0]["interval"],
            crop_box:this.dt["args"][0]["crop_box"],
            crop_right:this.dt["args"][0]["crop_right"],
            crop_top:this.dt["args"][0]["crop_top"],
            crop_bottom:this.dt["args"][0]["crop_bottom"],
        };
        return di_py;
    }
}

export interface IpyImgLib {
    appFeatures_CV:AppFeatures_CV;
    imgFile:string;
    cycles:string;
    realtimeImgGrabDurationMins:string;
    interval:string;
    crop_box:string;
    crop_right:string;
    crop_top:string;
    crop_bottom:string;
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
******************************************************************/