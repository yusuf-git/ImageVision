/* Updates on 12-Mar-2022 07:30 AM */
import { KognifaiCoreReg as kognifaiCore } from "../../factory/KognifaiCoreRegistory";
import { ImageVisionRegistry as visionRegistry } from "../../factory/ImageVisionRegistry";
import { helper, wrapperElement as element } from "kognifai-automation-framework";
import { browser, by, ExpectedConditions } from 'protractor';
import { AppPages } from "../../pages/Discovery-Viewer-Next/SDVHomePage";
import { execSync } from "child_process";
import * as path from "path";
import { fs_helper as fsh} from "../../helpers/fs_helper"

let loginPage = kognifaiCore.loginPage,
    step: typeof helper.allureHelpers.step = helper.allureHelpers.step.bind(helper.allureHelpers),
    googlePage = visionRegistry.googlePage,
    pyImgCreativePage = visionRegistry.pyImgCreativePage,
    pyImgCompPage = visionRegistry.pyImgCompPage,
    actionizePage = visionRegistry.pyActionizePage

describe('ImageVision v1 - ImageCreative validation:', async () => {

    beforeAll(async () => {

        step("1", "Open google search page")
        browser.ignoreSynchronization = true
        await googlePage.open("https://google.co.in")
        
    });

    afterAll(async () => {

    }); 
    
    beforeEach(async()=> {

    });

    afterEach(async()=> {
        
    });

    fit("Actionize test-1", async () => { 
        await actionizePage.Actionize_Ex_PO_1()
    });//EOT

 });//EOS
