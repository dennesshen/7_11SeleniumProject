import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import service_for_711Script
from service_for_711Script import choose7_11Map
from exception_for7_11Script import EnterDataHasErrorException

class Seven_11Script:

    def __init__(self,mainDriver:WebDriver, infoParameter:list):
        self.shippingValues = infoParameter[0]
        self.senderName = infoParameter[1]
        self.senderPhone = infoParameter[2]
        self.senderEmail = infoParameter[3]
        self.senderStoreID = infoParameter[4]
        self.receiverName = infoParameter[5]
        self.receiverPhone = infoParameter[6]
        self.receiverEmail = infoParameter[7]
        self.receiverStoreID = infoParameter[8]
        self.infoParameter =infoParameter
        self.mainDriver = mainDriver


    # 7-11交貨便第一頁操作
    def firstPageScript(self):
        iframe = self.mainDriver.find_element(By.NAME, "mainframe")
        self.mainDriver.switch_to.frame(iframe)
        self.mainDriver.find_element(By.CLASS_NAME, "MainBtn").click()
        self.mainDriver.implicitly_wait(10)

    # 7-11交貨便第二頁操作
    def secondPageScript(self):
        self.mainDriver.find_element(By.ID, "checkB").click()
        self.mainDriver.find_element(By.CLASS_NAME, "MainBtn").click()
        self.mainDriver.implicitly_wait(10)


    # 7-11交貨便第三頁操作
    def thirdPageScript(self):
        moneyIntervalSymbol = service_for_711Script.moneyIntervalOf7_11(self.shippingValues)
        Select(self.mainDriver.find_element(By.ID, "shippingValue")).select_by_value(moneyIntervalSymbol)
        self.mainDriver.find_element(By.ID, "orderAmount").send_keys(str(self.shippingValues))
        self.mainDriver.find_element(By.ID, "nextStep").click()
        self.mainDriver.implicitly_wait(10)


    # 7-11交貨便第四頁操作
    def fourthPageScript(self):
        self.mainDriver.find_element(By.ID, "senderName").send_keys(self.senderName)
        self.mainDriver.find_element(By.ID, "senderPhone").send_keys(self.senderPhone)
        self.mainDriver.find_element(By.ID, "senderEmail").send_keys(self.senderEmail)
        if self.senderStoreID=="":
            self.mainDriver.find_element(By.ID, "nextStep").click()
            self.mainDriver.implicitly_wait(10)
            return
        choose7_11Map(self.mainDriver, self.senderStoreID)
        self.mainDriver.implicitly_wait(10)

    # 7-11交貨便第五頁操作
    def fifthPageScript(self):
        self.mainDriver.find_element(By.ID, "receiverName").send_keys(self.receiverName)
        self.mainDriver.find_element(By.ID, "receiverPhone").send_keys(self.receiverPhone)
        self.mainDriver.find_element(By.ID, "receiverEmail").send_keys(self.receiverEmail)
        choose7_11Map(self.mainDriver, self.receiverStoreID)
        self.mainDriver.implicitly_wait(10)

    def sixthPageScript(self):
        time.sleep(2)
        phone = self.mainDriver.find_element(By.ID, "receiverPhone").get_attribute("innerText")
        name  = self.mainDriver.find_element(By.ID, "receiverName").get_attribute("innerText")
        sendStoreID = self.mainDriver.find_element(By.CSS_SELECTOR, "span[id='sendStoreId']").get_attribute("innerText")

        # 驗證資料是否有誤
        print("第六頁資訊：", phone, name, sendStoreID)
        if phone != self.receiverPhone: raise EnterDataHasErrorException
        if phone != self.receiverPhone: raise EnterDataHasErrorException
        if phone != self.receiverPhone: raise EnterDataHasErrorException

        printButtonLocate = "body>div[class='PageComtent']>div[class='AgreeBtn']>a[id='printOrder']"
        confirmButton = self.mainDriver.find_element(By.CSS_SELECTOR, printButtonLocate)
        confirmButton.click()

    def seventhPageScript(self):
        time.sleep(5)
        # 取得交貨便代碼
        symbol = self.mainDriver.find_element(By.ID, "pinno").text
        self.infoParameter.append(symbol)
        print(self.receiverName + "的最終交貨便代碼："+ symbol)










