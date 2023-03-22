/***
 * Authored on: 26-Jul-2020 01:30 PM
 * Updates on : 27-Jul-2020 02:00 AM, 09-Dec-2020 02:50 AM, 10-Dec-2020 01:40 AM, 12-Mar-2022 08:20 AM
 */
import * as fse from 'fs-extra';
import { browser, by, protractor, ExpectedConditions } from "protractor";
import * as path from "path";
import { helper } from "kognifai-automation-framework";
import { wrapperElement as element, IElementWrapper } from "kognifai-automation-framework";
import * as cp from 'child_process';
//import {PythonShell} from 'python-shell';
import * as fs from 'fs';
//import { fs_helper as fsh, fs_helper} from "./../helpers//fs_helper"
import { async } from 'q';
import { di_pyImgCreativeLib } from "./di_pyImgCreativeLib"
import { AppFeatures_CV } from "./appfeatures_cv"


export class pathRefs {

    /*private static imgArchivesPath__:string;
    private static runTimeImgPath__:string;
    private static runTimeDiffImgPath__:string;
    private static sdvRuntimeImgPathLiteral__ = path.join(__dirname, "..", "..", "sdv-archives", "images");

    private static get browserName():string{
        return helper.testRunCache.readKey("currentBrowser");
    }

    static get getImgArchivesPath():string {
        if (pathRefs.imgArchivesPath__ === undefined) {
            pathRefs.imgArchivesPath__ = this.sdvRuntimeImgPathLiteral__;
        }
        return pathRefs.imgArchivesPath__;
    }

    static get getRuntimeImgPath():string {
        if (pathRefs.runTimeImgPath__ === undefined) {
            let dateTimeSecs = new Date().getSeconds();
            pathRefs.runTimeImgPath__ = path.join(this.getImgArchivesPath, dateTimeSecs.toString(), this.browserName);
        }
        return pathRefs.runTimeImgPath__;
    }

    static get getImgDiffPath():string {
        if (pathRefs.runTimeDiffImgPath__ === undefined) {
            pathRefs.runTimeDiffImgPath__ = path.join(this.getRuntimeImgPath, );
            pathRefs.runTimeImgPath__ = this.sdvRuntimeImgPathLiteral__;
        }
        return pathRefs.runTimeImgPath__;
    }*/


    //private browserName = this.browserName()
    private dt = new Date();
    private dateTimeSecs = this.dt.getDay().toString() + this.dt.getMonth().toString() + this.dt.getFullYear().toString() + "_" + this.dt.getHours().toString() + this.dt.getMinutes().toString() + this.dt.getSeconds().toString();
    public static imgArchivesPath = "";
    public static baselineImgPath = path.join(browser.params.baseDir, '..', 'src\\test-inputs\\imagevision\\baseline')
    public static baselineRootPath = path.join(browser.params.baseDir, '..', 'src\\test-inputs\\imagevision')
    public static brisk_flann_baseline_path = path.join(browser.params.baseDir, 'src\\test-inputs\\imagevision\\data\\baseline')
    //runTimeImgPath = path.join(this.imgArchivesPath, this.dateTimeSecs.toString());
    public static runTimeImgPath = "";
    public static reportsPath = "";
    public static imgOpsSessionRootPath = "";
    public static baseline_img = ""
    public static runtime_img = ""
    //public static resultsRootPath = ""
    public static resultPath = ""
    public static imgGrabOpResult = false
    public static imgCompOpResult = false
    public static actionizeTemplateImgPath  = ""
    public static actionizeRuntimePath = ""
    public static actionizeResultsPath = ""
    public static actionizeReportsPath = ""
    public static actionizeOpResult = false
    public static RT_RuntimeImgsPath = ""
    public static RT_PositiveBaselinePath = ""
    public static RT_NegativeBaselinePath = ""
    public static RT_ReportsPath = ""
    public static RT_ResultsPath = ""
    public static RT_mode = false
    public static hangIssueChecker_RuntimePath = ""
    public static hangIssueChecker_ReportsPath = ""
    public static hangIssueChecker_ResultsPath = ""


    browserName(): string {
        try {
            return helper.testRunCache.readKey("currentBrowser");
        }
        catch {
            console.log("currentBrowser key is not present in testruncache")
            return ""
        }
    }

    featureImgPath: Record<AppFeatures_CV, string> = {
        1: path.join('\\mywells\\'),
        2: path.join('\\log-widget\\'),
        3: path.join('\\history-plot\\'),
        4: path.join('\\survey-widget\\'),
        5: path.join('\\spectrum-plot\\'),
        6: path.join('\\wireline-widgets\\'),
        7: path.join('\\gauges\\'),
        8: path.join('\\twoDTrajectory\\'),
        9: path.join('\\numeric-monitoring\\'),
        10: path.join('\\circular-widget\\'),
        11: path.join('\\crossplotting-widget\\'),
        12: path.join('\\steeringRose-widget\\'),
        13: path.join('\\log-widget\\goto\\'),
        14: path.join('\\log-widget\\curvemousemove\\'),
        15: path.join('\\log-widget\\tooltip\\'),
        16: path.join('\\actionize_demo\\google_page\\')
    };


    subFeatureImgPath: Record<AppFeatures_CV, string> = {
        1: path.join('\\sub-feat1\\sub-feat2\\'),
        2: path.join('\\1\\2\\'),
        3: path.join('\\sub-feat1\\'),
        4: path.join('\\sub-feat1\\'),
        5: path.join('\\sub-feat1\\'),
        6: path.join('\\sub-feat1\\'),
        7: path.join('\\sub-feat1\\'),
        8: path.join('\\sub-feat1\\'),
        9: path.join('\\sub-feat1\\'),
        10: path.join('\\sub-feat1\\'),
        11: path.join('\\sub-feat1\\'),
        12: path.join('\\sub-feat1\\'),
        13: path.join(''),
        14: path.join(''),
        15: path.join(''),
    };
}