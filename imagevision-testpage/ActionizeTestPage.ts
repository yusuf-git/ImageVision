/*
    Author     : Yusuf
    Created on : 10th Dec 2021 06:10 AM
    Updates on : 10th Dec 2021 04:20 PM
    Purpose    : Model Page Object for ImageVision - Actionize module
*/

import { browser, by, By, ExpectedConditions } from 'protractor';
import { wrapperElement as element } from "kognifai-automation-framework";
import { KognifaiCoreReg as kognifaiCore } from "../../factory/KognifaiCoreRegistory";
import { ImageVisionRegistry as visionRegistry } from "../../factory/ImageVisionRegistry";
import { fs_helper as fsh} from "../../helpers/fs_helper"
import {AppFeatures_CV} from "../../imagevision-tdk/appfeatures_cv"
import { helper } from "kognifai-automation-framework";
import { pyCVLibrary } from '../../imagevision-tdk/pyCVLibrary';
import { pathRefs } from 'src/imagevision-tdk/pathRefs';
import { di_pyImgCreativeLib } from 'src/imagevision-tdk/di_pyImgCreativeLib';
import { Login } from 'kognifai-login/build-js/pages/Login';
import { di_pyImgCompLib } from 'src/imagevision-tdk/di_pyImgCompLib';
var path = require('path');

export class ImageVision{
    imgGrab = visionRegistry.pyImgCreativeLib
    imgGrabOpts = visionRegistry.di_pyImgCreativeLib
    imgComp = visionRegistry.pyImgCompLib;
    imgCompOpts = visionRegistry.di_pyImgCompLib;
    hangChecker = visionRegistry.pyHangIssueChecker
    hangCheckerOpts = visionRegistry.di_pyHangIssueCheckerLib
    actionize = visionRegistry.pyImgInteractLib;
    actionizeOpts = visionRegistry.di_pyImgInteractLib;
    pathRefs = visionRegistry.pathRefs;
}

export class ActionizeTestPage {
    private imgVis = new ImageVision();
    private imgInteract = visionRegistry.pyImgInteractLib;
    private imgInteractOpts = visionRegistry.di_pyImgInteractLib;
    pathRefs = visionRegistry.pathRefs;


    async Actionize_Ex_PO_1()
    {
        /*  ImageVision instance creation     */
        let imgVis = this.imgVis
        let actionize_result = false, comp_result = false

        /*  Set-1 */
        /*  Actionize - reset configurations to default settings  */
        imgVis.actionizeOpts.appFeatures_CV = AppFeatures_CV.google_page.toString()
        /* Count number of vessles that are in unsafe zone*/
        imgVis.actionizeOpts.actions = "IsVisible/moveMouse/wait/doubleClick/wait/mouseRightClick/wait/click/moveMouseRel/wait/mouseRightClick/wait"
        /* Count number of vessles in safe zone */
        imgVis.actionizeOpts.actions = "IsVisible/moveMouse/wait"
        /* Hover the mouse over the vessles that are in unsafe zone */

        //imgVis.actionizeOpts.action_inputs.wait_seconds = "2"
        imgVis.actionizeOpts.action_inputs.rel_x_y = "22,12"

        actionize_result = await this.imgInteract.pyActionize(imgVis.actionizeOpts, "1.png")
        console.log("result:",actionize_result)
    }
}