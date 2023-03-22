import { KognifaiCoreReg as kognifaiCore } from "../../factory/KognifaiCoreRegistory";
import { ImageVisionRegistry as visionRegistry } from "../../factory/ImageVisionRegistry";
import { helper, wrapperElement as element } from "kognifai-automation-framework";
import { browser, by, ExpectedConditions } from 'protractor';
import { AppPages } from "../../pages/Discovery-Viewer-Next/SDVHomePage";
import { execSync } from "child_process";
import * as path from "path";
import { fs_helper as fsh} from "../../helpers/fs_helper"
import { login } from "kognifai-login";

let loginPage = kognifaiCore.loginPage,
    step: typeof helper.allureHelpers.step = helper.allureHelpers.step.bind(helper.allureHelpers),
    localLoginPage = kognifaiCore.localLoginPage,
    pyImgCreativePage = visionRegistry.pyImgCreativePage,
    pyImgCompPage = visionRegistry.pyImgCompPage

describe('ImageVision v1 - ImageCreative validation:', async () => {

    beforeAll(async () => {

        step("1", "Log in to the application")
        browser.ignoreSynchronization = true
        await localLoginPage.logIn()
        
    });

    afterAll(async () => {

    }); 
    
    beforeEach(async()=> {

    });

    afterEach(async()=> {
        
    });

    fit("ImageCreative test-1", async () => { 
        console.log("test-1....")
        //await pyImgCreativePage.grabImg_1();
        await pyImgCompPage.ImageComp_Exp_1()
    });//EOT

    it("ImageCreative test-2", async () => { 
        console.log("test-2....")
        await pyImgCreativePage.grabImg_2();
    });//EOT

    it("ImageCreative test-3", async () => { 
        console.log("test-3....")
        await pyImgCreativePage.grabImg_3();
    });//EOT

    it("ImageCreative test-4", async () => { 
        console.log("test-4....")
        await pyImgCreativePage.grabImg_4();
    });//EOT

    it("ImageCreative test-5", async () => { 
        console.log("test-5....")
        await pyImgCreativePage.grabImg_5();
    });//EOT

    it("ImageCreative test-6", async () => { 
        console.log("test-6....")
        await pyImgCreativePage.grabImg_6();
    });//EOT

    it("ImageCreative test-7", async () => { 
        console.log("test-7....")
        await pyImgCreativePage.grabImg_7();
    });//EOT

    it("ImageCreative test-8", async () => { 
        console.log("test-8....")
        await pyImgCreativePage.grabImg_8();
    });//EOT

    it("ImageCreative test-9", async () => { 
        console.log("test-9....")
        await pyImgCreativePage.grabImg_9();
    });//EOT

    it("ImageCreative test-10", async () => { 
        console.log("test-10....")
        await pyImgCreativePage.grabImg_10();
    });//EOT

    it("ImageCreative test-11", async () => { 
        console.log("test-11....")
        await pyImgCreativePage.grabImg_11();
    });//EOT
 });//EOS
