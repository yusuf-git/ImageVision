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
var path = require('path');

export class ImgCreativeTestPage {

    private imgCreative = visionRegistry.pyImgCreativeLib
    private imgCreativeOpts = visionRegistry.di_pyImgCreativeLib
    private imgComp = visionRegistry.pyImgCompLib;
    private imgCompOpts = visionRegistry.di_pyImgCompLib;
    private imgInteract = visionRegistry.pyImgInteractLib;
    private imgInteractOpts = visionRegistry.di_pyImgInteractLib;
    private hangChecker = visionRegistry.pyHangIssueChecker
    private hangCheckerOpts = visionRegistry.di_pyHangIssueCheckerLib
    pathRefs = visionRegistry.pathRefs;

    //public baseUrl = "https://kdikrsatdev10/Poseidonnext/live/#/"
    //public storeUrl =  "https://kdikrsatdev10/Store/WITSML"


    private userId = element(by.css('input#login-username'))
    private userName = element(by.id('login-username'))
    private passWord = element(by.id('login-password'))
    private submit = element(by.name('button'))
    private body = element(by.xpath('//body[@class="kx-page"]'))
  
     
    /* Test goals: read the last operation configurations, reset to factory settings, offline data plotting, baselining, 
      no forced failure on baselining, custom path for storage, read the last operation result
      
      Outcome : PASS
    */
    async grabImg_1()
    {
      let u1 = await this.userId.takeScreenshot();
      let u2 = await this.userId.takeScreenshot();
      let p1 = await this.passWord.takeScreenshot();
      let p2 = await this.passWord.takeScreenshot();
      let b1 = await this.body.takeScreenshot();
      let b2 = await this.body.takeScreenshot();
      let commonLib = kognifaiCore.commonLib;
      commonLib.writeScreenShot(u1,"u11.png");
      commonLib.writeScreenShot(u2,"u22.png");
      commonLib.writeScreenShot(p1,"p11.png");
      commonLib.writeScreenShot(p2,"p22.png");
      commonLib.writeScreenShot(b1,"b11.png");
      commonLib.writeScreenShot(b2,"b22.png");
      await browser.sleep(5000)
      u1 = await this.userId.takeScreenshot();
      await browser.sleep(5000)
      u2 = await this.userId.takeScreenshot();
      await browser.sleep(5000)
      p1 = await this.passWord.takeScreenshot();
      await browser.sleep(5000)
      p2 = await this.passWord.takeScreenshot();
      await browser.sleep(5000)
      b1 = await this.body.takeScreenshot();
      await browser.sleep(5000)
      b2 = await this.body.takeScreenshot();
      await browser.sleep(5000)
      let imgCreativeOpts = this.imgCreativeOpts
      let currConfig = imgCreativeOpts.getCurrentConfigs()
      console.log("curr value - appFeatures_CV      :"+currConfig.appFeatures_CV)
      console.log("curr value - approvedAsBaseline:"+currConfig.approvedAsBaseline)
      console.log("curr value - imgArchivesPath   :"+currConfig.imgArchivesPath)
      console.log("curr value - resultPath          :"+currConfig.imgCapResultPath)
      console.log("curr value - uiObjSnaap          :"+currConfig.uiObjSnap)
      console.log("curr value - resetTDDault    :"+currConfig.resetToDefault);

      imgCreativeOpts.resetConfig(this.imgCreativeOpts)
      console.log("post reset - appFeatures_CV       :"+imgCreativeOpts.appFeatures_CV)
      console.log("post reset - approvedAsBaseline :"+imgCreativeOpts.approvedAsBaseline)
      console.log("post reset - uiObjSnaap           :"+imgCreativeOpts.uiObjSnap)
      console.log("post reset - resetTDDault     :"+imgCreativeOpts.resetToDefault);

      imgCreativeOpts.appFeatures_CV = AppFeatures_CV.CircularWidget.toString()
      imgCreativeOpts.approvedAsBaseline = "true";
      imgCreativeOpts.realtime = "false"
      imgCreativeOpts.uiObjSnap = "false"
      imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      await this.imgCreative.pyGrabImage(this.userId,"user1.png",imgCreativeOpts, "test1")
      await this.imgCreative.pyGrabImage(this.userId,"user2.png",imgCreativeOpts, "test1")
      await this.imgCreative.pyGrabImage(this.passWord,"pass1.png",imgCreativeOpts, "test1")
      await this.imgCreative.pyGrabImage(this.passWord,"pass2.png",imgCreativeOpts, "test1")
      await this.imgCreative.pyGrabImage(this.body,"body1.png",imgCreativeOpts, "test1")
      await this.imgCreative.pyGrabImage(this.body,"body2.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.userId,"user11.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.userId,"user22.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.passWord,"pass11.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.passWord,"pass22.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.body,"body11.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
      await this.imgCreative.pyGrabImage(this.body,"body22.png",imgCreativeOpts, "test1")
      await browser.sleep(5000);
          
      await this.imgCreative.pyGrabImage(this.userId,"user1.png",imgCreativeOpts, "userid_pwd_1")
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
      
      await this.imgCreative.pyGrabImage(this.userId,"user2.png",imgCreativeOpts, "userid_pwd_1")
      ImgCreativeResult = this.imgCreative.getImgGrabResult(imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);

      await this.imgCreative.pyGrabImage(this.passWord,"user3.png",imgCreativeOpts)
      ImgCreativeResult = this.imgCreative.getImgGrabResult(imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
      
      await this.imgCreative.pyGrabImage(this.passWord,"user4.png",this.imgCreativeOpts, "userid_pwd_1")
      ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
    }


    /* real-time, interval less than a sec, baselining, no forced failure on baselining, custom path storage, 
      baseline overwrite, read the last operation result

      Outcome = PASS
    */
    async grabImg_2()
    {
      let imgCreativeOpts = this.imgCreativeOpts
      imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      imgCreativeOpts.realtime = "true"
      imgCreativeOpts.realtimeImgGrabDurationMins = "1"
      imgCreativeOpts.interval = "0.91"
      imgCreativeOpts.approvedAsBaseline = "true";
      imgCreativeOpts.imgArchivesPath = path.join(browser.params.imgArchivesPath);
      imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      imgCreativeOpts.overwriteBaseline = "false"
      await this.imgCreative.pyGrabImage(this.body, "body1.png", imgCreativeOpts, "body_1")
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
      //imgCreativeOpts.overwriteBaseline = "true"
      //await this.imgCreative.pyGrabImage(this.passWord, "body1.png", imgCreativeOpts, "body_1") //for overwrite verification
      //ImgCreativeResult = this.imgCreative.getImgGrabResult(imgCreativeOpts)
      //console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
      
      
      /* despite uiObjSnaap being true, realtime is explicitly set to false. If both are true, realtime takes precedence */
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.realtime = "false"
      this.imgCreativeOpts.uiObjSnap = "true"
      this.imgCreativeOpts.approvedAsBaseline = "true";
      await this.imgCreative.pyGrabImage(this.body,"body2.png",imgCreativeOpts)
      ImgCreativeResult = this.imgCreative.getImgGrabResult(imgCreativeOpts)
      console.log(`Image : ${imgCreativeOpts.imgFile}, img grab result : ${ImgCreativeResult}`);
    }

    
    /*
      historical = yes, no mask region = yes, expected outcome = pass, baseline copy = yes, fail test on baseline copy ? = no

      Outcome = PASS
    */
    async grabImg_3()
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.realtimeImgGrabDurationMins = "1"
      this.imgCreativeOpts.cycles = "8";
      this.imgCreativeOpts.interval = "1";
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      this.imgCreativeOpts.browserDependent = "true";
      this.imgCreativeOpts.maskRegion = "0,0,0,0";
      this.imgCreativeOpts.realtime = "false";
      this.imgCreativeOpts.uiObjSnap = "false";
      await this.imgCreative.pyGrabImage(this.body, "body1A.png", this.imgCreativeOpts)
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log(`Image : ${this.imgCreativeOpts.imgFile}, img capture result : ${ImgCreativeResult}`);
    }


    /* 
      historical, # of cycles will be 1 - though set 7, baselining, force fail the test on baselining 
      outcome = FAIL
    */
    async grabImg_4()
    { 
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.Gauges.toString()
      this.imgCreativeOpts.cycles = "7";
      this.imgCreativeOpts.maskRegion = "";
      
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "true";
      await this.imgCreative.pyGrabImage(this.userName,"userName1A.png",this.imgCreativeOpts)
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log(`Image : ${this.imgCreativeOpts.imgFile}, img capture result : ${ImgCreativeResult}`);
    }
    

  /* historical = true, baseline approval = false, configure to force fail = true
      
      outcome : PASS
    */
    async grabImg_5()
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.cycles = "6";
      this.imgCreativeOpts.approvedAsBaseline = "false";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "true";
      this.imgCreativeOpts.overwriteBaseline = "true";
      this.imgCreativeOpts.failCurrentTestOnFailedImgOp= "true";
      //this.imgCreativeOpts.maskRgion_excluding = "0,0,20,25";
      await this.imgCreative.pyGrabImage(this.passWord,"password1.png", this.imgCreativeOpts)
      this.imgCreativeOpts.overwriteBaseline = "false";
    }

    
      /* Realtime with cycles setting without explicit interval. Implicit assignment to interval with 1 sec.
        Copy to baseline with expected test outcome being pass.
        Note the realtimeImgGrabDealtimeMmgGrabDurationMins settings with explicit empty string assignment

        outcome : PASS
      */
    async grabImg_6()
    { 
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.realtime = "true"
      this.imgCreativeOpts.realtimeImgGrabDurationMins = ""; //valid: 0, 0.0, ""
      this.imgCreativeOpts.cycles = "10";
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      this.imgCreativeOpts.failCurrentTestOnFailedImgOp= "true"
      await this.imgCreative.pyGrabImage(this.userName,"userName1B.png",this.imgCreativeOpts)
    }


    /* invalid img_arcives_path to cause explicit failure with cycles > 1 for a historic scenario 
        
      outcome : FAIL
    */
    async grabImg_7()
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.realtime = "false"
      this.imgCreativeOpts.imgArchivesPath = "F:/abc";
      this.imgCreativeOpts.cycles = "4";
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      this.imgCreativeOpts.failCurrentTestOnFailedImgOp= "true"
      await this.imgCreative.pyGrabImage(this.userName,"userName1C.png",this.imgCreativeOpts)
    }


    /* invalid imgArchivesPath but without effecting test failure for a historic scenario 
      
      outcome : FAIL
    */
    async grabImg_8()
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.imgArchivesPath = "F:/abc";
      this.imgCreativeOpts.cycles = "3";
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      this.imgCreativeOpts.failCurrentTestOnFailedImgOp= "false";
      await this.imgCreative.pyGrabImage(this.userName,"userName1D.png",this.imgCreativeOpts)
    }


  /* image file set to empty string, img archival path set back to valid, forced baseline overwrite = yes, uiobj snap = yes 
      outcome : PASS
  */

    async grabImg_9() 
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.imgFile = "";
      this.imgCreativeOpts.imgArchivesPath = path.join(browser.params.imgArchivesPath);
      this.imgCreativeOpts.cycles = "2"; // despite being specified 2, implicitly it will be set to 1 for uiobj snaps
      this.imgCreativeOpts.browserDependent = "true";
      this.imgCreativeOpts.realtime = "false";
      this.imgCreativeOpts.uiObjSnap = "true"
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failCurrentTestOnFailedImgOp= "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      await this.imgCreative.pyGrabImage(this.submit, "submit1.png", this.imgCreativeOpts, "baseline-overwrite")
      this.imgCreativeOpts.overwriteBaseline = "true"
      await this.imgCreative.pyGrabImage(this.userId, "submit1.png", this.imgCreativeOpts, "baseline-overwrite")
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log("Image :"+ this.imgCreativeOpts.imgFile +", img capture result :"+ ImgCreativeResult)
    }


  /* realtime with 30 cyles of grab at 0.5 sec interval,  maskRegion specified 

     outcome : FAIL
  */ 
  async grabImg_10() 
  {
    let imgCreativeOpts = this.imgCreativeOpts;
    imgCreativeOpts.appFeatures_CV = AppFeatures_CV.MyWells.toString();
    imgCreativeOpts.imgFile = "";
    imgCreativeOpts.imgArchivesPath = path.join(browser.params.imgArchivesPath);
    imgCreativeOpts.cycles = "30";
    imgCreativeOpts.interval = "0.5";
    imgCreativeOpts.realtimeImgGrabDurationMins = "0";
    imgCreativeOpts.browserDependent = "true";
    imgCreativeOpts.realtime = "true";
    imgCreativeOpts.uiObjSnap = "false";
    imgCreativeOpts.maskRegion = "0,0,90,50";
    imgCreativeOpts.approvedAsBaseline = "true";
    imgCreativeOpts.failCurrentTestOnFailedImgOp= "true";
    imgCreativeOpts.failTestOnBaselineAutoApproval = "true";
    imgCreativeOpts.overwriteBaseline = "false"
    await this.imgCreative.pyGrabImage(this.submit, "submit_mask1.png", this.imgCreativeOpts)
    let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
    console.log("Image :"+ this.imgCreativeOpts.imgFile +", img capture result :"+ ImgCreativeResult)
  }


  /* realtime with 20 cyles of grab at one sec interval,  maskRegionExcluding specified and hence maskRegion is set empty
     
     outcome : PASS   
  */ 
  async grabImg_11() 
  {
    let imgCreativeOpts = this.imgCreativeOpts;
    imgCreativeOpts.appFeatures_CV = AppFeatures_CV.NumericMonitoring.toString();
    imgCreativeOpts.imgFile = "";
    imgCreativeOpts.imgArchivesPath = path.join(browser.params.imgArchivesPath);
    imgCreativeOpts.realtime = "true";
    imgCreativeOpts.cycles = "20";
    imgCreativeOpts.interval = "1";
    imgCreativeOpts.realtimeImgGrabDurationMins = "0";
    imgCreativeOpts.browserDependent = "true";
    imgCreativeOpts.uiObjSnap = "false";
    imgCreativeOpts.maskRegion = "";
    imgCreativeOpts.maskRegionExcluding = "0,0,90,50";
    imgCreativeOpts.approvedAsBaseline = "true";
    imgCreativeOpts.failCurrentTestOnFailedImgOp= "true";
    imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
    imgCreativeOpts.overwriteBaseline = "false"
    await this.imgCreative.pyGrabImage(this.submit, "submit_mask_exclude1.png", this.imgCreativeOpts)
    let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
    console.log("Image :"+ this.imgCreativeOpts.imgFile +", img capture result :"+ ImgCreativeResult)
  }



  async grabNCompImg_12(dt:any)
    {
      this.imgCreativeOpts.appFeatures_CV = AppFeatures_CV.LogWidget.toString()
      this.imgCreativeOpts.realtimeImgGrabDurationMins = "1"
      this.imgCreativeOpts.cycles = "8";
      this.imgCreativeOpts.interval = "1";
      this.imgCreativeOpts.approvedAsBaseline = "true";
      this.imgCreativeOpts.failTestOnBaselineAutoApproval = "false";
      this.imgCreativeOpts.browserDependent = "true";
      this.imgCreativeOpts.maskRegion = "0,0,0,0";
      this.imgCreativeOpts.realtime = "false";
      this.imgCreativeOpts.uiObjSnap = "false";
      await this.imgCreative.pyGrabImage(this.body, "body1A.png", this.imgCreativeOpts)
      let ImgCreativeResult = this.imgCreative.getImgGrabResult(this.imgCreativeOpts)
      console.log(`Image : ${this.imgCreativeOpts.imgFile}, img capture result : ${ImgCreativeResult}`);

      //*************Comparison*********************** */

      dt[""][""][""] = "abc123";
      let result = await this.imgComp.checkHangIssue(dt);
      dt[""][""][""] = "def456";
      let result1 = await this.imgComp.pyCompareImages(dt)
      /*if(result && result1)
      {
        
      }*/
    }
}


