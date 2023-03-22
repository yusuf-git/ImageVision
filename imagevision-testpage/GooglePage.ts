import { browser, by, By, ExpectedConditions } from 'protractor';
import { wrapperElement as element } from "kognifai-automation-framework";

export class GooglePage {
  private g_img = element(by.xpath("//img[@class='lnXdpd']"))

  async open(baseUrl:string) {
        console.log("baseURL:",baseUrl)
        await browser.sleep(5000)
        await browser.get(baseUrl)
        await browser.wait(ExpectedConditions.visibilityOf(this.g_img.baseElement), 8000)
  }
}