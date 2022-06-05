
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from exception_for7_11Script import StoreNotFoundException


def moneyIntervalOf7_11(amount:int) -> str :
    interval = amount//1000 + 1
    if amount%1000 == 0 :
        interval = interval-1
    match interval:
        case 1:
            return "756_888"
        case 2:
            return "7P3_888"
        case 3:
            return "7PC_888"
        case 4:
            return  "7PL_888"
        case 5:
            return "7PU_888"


def dealAdress(address:str):
    address.strip()
    zoneUnits = ("鄉", "鎮", "市", "區")
    roadUnits = ("路", "街", "道")
    otherUnit = ("里", "村", "鄰")
    cityIndex =0
    roadIndex =0
    otherIndex =0

    for unit in zoneUnits:
        try:
            index = address[3:].index(unit)+3
            cityIndex = index
            break
        except:
            pass

    for unit in otherUnit:
        index = address.find(unit, cityIndex)
        otherIndex = index if index > otherIndex  else otherIndex
    print(otherIndex)

    for unit in roadUnits:
        try:
            index = address.index(unit)
            roadIndex = index
            break
        except:
            pass

    if address[roadIndex+2] == "段":
        roadIndex += 2

    city = address[0:3]
    zone = address[3:cityIndex+1]
    road = address[otherIndex+1:roadIndex+1] if  0 < otherIndex < roadIndex else address[cityIndex+1:roadIndex+1]
    return [city, zone, road]

def choose7_11Map(driver:WebDriver, store_id:str):

    try:
        mainView = driver.current_window_handle
        driver.find_element(By.ID, "checkStore").click()
        select7_11 = driver.window_handles[1]
        driver.switch_to.window(select7_11)
        driver.implicitly_wait(20)

        # 切換到用門市店號搜尋的頁面
        driver.find_element(By.ID, "byID").click()
        driver.implicitly_wait(20)

        iframe2 = driver.find_element(By.ID, "frmMain")
        driver.switch_to.frame(iframe2)

        driver.find_element(By.ID, "storeIDKey").send_keys(store_id)
        driver.find_element(By.ID, "send").click()

        """ 下面是如果要用地址來找店的腳本
        Select(driver.find_element(By.ID, "sel_area")).select_by_value(city)
        time.sleep(1)
        Select(driver.find_element(By.ID, "zone")).select_by_value(zone)
        driver.implicitly_wait(10)
        driver.find_element(By.ID, "road_chosen").click()
        time.sleep(1)
    
        roadNamelocate = "li[class=must]>div[class=style_select]>div[id='road_chosen']>div[class='chosen-drop']>" \
                         "ul[class='chosen-results']>li"
        roadNames = driver.find_elements(By.CSS_SELECTOR, roadNamelocate)
        roadName_isExact = False
    
        精準比對 道路名稱，如果不行，就找有包含的就好
        for roadName in roadNames:
            if roadName.text == road:
                roadName.click()
                roadName_isExact = True
                break
        if not roadName_isExact:
            for roadName in roadNames:
                if road in roadName.text:
                    roadName.click()
                    break
        """

        driver.implicitly_wait(10)

        targetSearchString = "showMap(" + str(store_id) +")"
        storeNameLocate = "div[class='right_block']>ul>li[class='must']>ol[id='ol_stores']>li"
        storeNames = driver.find_elements(By.CSS_SELECTOR, storeNameLocate)
        for storeName in storeNames:
            if(storeName.get_attribute('onclick') == targetSearchString):
                storeName.click()
                break
        driver.switch_to.default_content()
        driver.implicitly_wait(10)
        driver.find_element(By.ID, "sevenDataBtn").click()
        driver.find_element(By.ID, "AcceptBtn").click()
        driver.find_element(By.ID, "submit_butn").click()

        driver.switch_to.window(mainView)
        driver.switch_to.frame( driver.find_element(By.ID, "mainframe"))
        driver.implicitly_wait(5)
        driver.find_element(By.ID, "nextStep").click()
    except Exception:
        raise StoreNotFoundException




