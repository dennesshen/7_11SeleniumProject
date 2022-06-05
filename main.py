from ManipulateScript import Seven_11Script
from chromeDriver import Seven_11Driver
from ExcelManipulate import ExcelManipulate
from exception_for7_11Script import StoreNotFoundException
from exception_for7_11Script import ExecuteOverErrorLimitException, EnterDataHasErrorException
import sys

def startAutomation(infoParameter:list):
    # 啟動driver 並連到交貨便首頁
    driver7_11 = Seven_11Driver("./chromedriver/chromedriver")
    driver7_11.runPageByURL("https://myship.7-11.com.tw/MyShip/Shipinfo?showUrlType=intra")
    seven_11Script = Seven_11Script(driver7_11.driver, infoParameter)

    print("第一頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.firstPageScript)

    print("第二頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.secondPageScript)

    print("第三頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.thirdPageScript)

    print("第四頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.fourthPageScript)

    print("第五頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.fifthPageScript)

    print("第六頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.sixthPageScript)

    print("第七頁開始執行")
    driver7_11.execute_with_errorLimit(3, seven_11Script.seventhPageScript)

    driver7_11.driver.quit()

    return infoParameter[10]

if __name__ == "__main__":
    print(sys.path)
    print("提醒：excel 檔必須要是xlsx的版本，不能是舊版本xls")
    print("     該Excel檔案不能有標題欄或列。")
    print("     開始執行程式前需要先關閉該Excel檔。")
    excelPath      = input("請輸入欲執行之Excel檔路徑：")
    senderName     = input("請輸入寄件人姓名：") or "謝宗元"
    senderPhone    = input("請輸入寄件人電話：") or "0932732281"
    senderEmail    = input("請輸入寄件人Email：") or "denneshen@gmail.com"
    senderStoreID  = input("請輸入寄件門市店號：(若不需要請直接按Enter)")

    senderInfoList = [senderName, senderPhone, senderEmail, senderStoreID]

    # 取得這一輪要處理的所有資料
    excelManipulate = ExcelManipulate(excelPath, senderInfoList)
    dealdataLists = excelManipulate.read7_11Excel()
    print(dealdataLists)

    # 接下來讓 dealdataLists 的每一筆資料進行自動化交貨便，並將最後結果填回Excel表
    resultRowIndex = 1 # 表示第幾筆資料
    for data in dealdataLists:
        resultString = ""
        try:
            resultString = startAutomation(data)
            print(str(data[5]) + "is ok")

        except StoreNotFoundException as e:
            print("storeNotFound")
            resultString = "選定門市時錯誤"

        except EnterDataHasErrorException:
            print("交貨便最終顯示資料有誤，請重新執行交貨便")
            resultString = "交貨便最終顯示資料有誤，請重新執行交貨便"

        except ExecuteOverErrorLimitException as e:
            print(e.args[0])
            resultString = "執行該筆資料填入時發生未知錯誤"

        except Exception:
            print("其他錯誤")
            resultString = "發生未知錯誤"

        excelManipulate.writeBackToExcel(resultRowIndex,resultString)
        resultRowIndex += 1

    print("完成本次自動化工作")


# # 列印單據頁面
# driver.implicitly_wait(5)
# # handles2 = driver.window_handles
# # print(len(handles2))
# # for i in handles2:
# #     print(i.title())
# print("test3--------------------------------")
# html = driver.execute_script("return document.body.outerHTML;")
# # print(html)
# # >div[class='AgreeBtn']>a[id='printOrder']
# printButtonLocate = "body>div[class='PageComtent']>div[class='AgreeBtn']>a[id='printOrder']"
# confirmButton = driver.find_element(By.CSS_SELECTOR, printButtonLocate)
# confirmButton.click()
#
# time.sleep(10)
# # 最後取得標籤序號頁面
# html = driver.execute_script("return document.body.outerHTML;")
#
#
# print(html)
# print("test4-----------------------------------")
# print("最終交貨便代碼："+ driver.find_element(By.ID, "pinno").text)
# #driver.get("https://epayment.7-11.com.tw/C2C/C2CWeb/PrintC2CPinCode.aspx")
# # driver.switch_to.frame( )
# # driver.find_element(By.ID, "printOrder").click()
