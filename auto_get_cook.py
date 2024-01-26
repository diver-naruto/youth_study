import time
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import ddddocr
import os

DRIVER_PATH = 'chromedriver'
options = ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')  # 无头参数//
options.add_argument('--disable-gpu')

options.add_argument("--disable-blink-features=automationControlled")
options.add_argument('-ignore-certificate-errors')
options.add_argument('-ignore -ssl-errors')
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
root = os.getcwd()
print(root)
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': f"{root}\youth_study\youth_excel"}
options.add_experimental_option("prefs",prefs)
download_file_path = "youth_study/youth_excel"

filepath = "youth_study/youth_excel/"



#该方法实现登陆功能
def get_youth_cook():
    charge = os.path.exists(f"{filepath}/1.xlsx")
    if charge == True:
        os.remove(f"{filepath}1.xlsx")
    url = 'http://home.yngqt.org.cn/user/login.aspx'
    driver = Chrome(executable_path=DRIVER_PATH, options=options)

    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 
            'params':{'behavior':'allow', 'downloadPath':f"{root}\youth_study\youth_excel"}}
    driver.execute("send_command", params=params)



    driver.implicitly_wait(15)
    driver.get(f'{url}')
    def fill_in():
        #填写账号
        driver.find_element(By.CSS_SELECTOR,'#txtusername').send_keys("") 
        #填写密码
        driver.find_element(By.CSS_SELECTOR,"#txtpassword").send_keys("")
    
        driver.find_element(By.CSS_SELECTOR,"#imgVerify").screenshot("youth_study/verification_photo/1.png")
        ocr = ddddocr.DdddOcr()
        with open('youth_study/verification_photo/1.png', 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)

        driver.find_element(By.CSS_SELECTOR,"#txtcode").send_keys(f"{res}")
        driver.find_element(By.CSS_SELECTOR,"#form1 > div.row.lyear-wrapper > div > div > div:nth-child(5) > button").click()
            
    fill_in()    
    while True:
        # time.sleep(1)
        ele_cunzi = driver.find_elements(By.CSS_SELECTOR,"#form1 > div.lyear-layout-web > div > header > nav > div > ul > li.dropdown.dropdown-profile > a > img")
        if len(ele_cunzi) == 0:
            driver.refresh()
            fill_in()
            continue
        if len(ele_cunzi) == 1:
            driver.find_element(By.CSS_SELECTOR,"#form1 > div.lyear-layout-web > div > header > nav > div > div > div").click()
            driver.find_element(By.CSS_SELECTOR,"#form1 > div.lyear-layout-web > div > aside > div.lyear-layout-sidebar-scroll.ps > nav > ul > li:nth-child(2) > a > i").click()
            driver.find_element(By.CSS_SELECTOR,"#form1 > div.lyear-layout-web > div > aside > div.lyear-layout-sidebar-scroll.ps > nav > ul > li.nav-item.nav-item-has-subnav.open > ul > li:nth-child(1) > a").click()

            break
        else:
            driver.refresh()
            fill_in()
            continue

 
    driver.find_element(By.CSS_SELECTOR,"#form1 > div.lyear-layout-web > div > main > div > div > div > div > div > div > table > tbody > tr:nth-child(1) > td:nth-child(3) > a").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,".layui-layer-btn0").click()
    #获取刚下载的excel名字
    def getLatestDownloadedFileName():
        if len(os.listdir(filepath)) == 0:
            return None
        return max (
            [filepath+ f for f in os.listdir(filepath)],
            key=os.path.getctime
        )
    
    while True:
        file_name = getLatestDownloadedFileName()
        if file_name == None:
            time.sleep(1)
            print("1")
            continue
        if "crdownload" in file_name:
            time.sleep(1)
            continue
        else:
            break
    print(file_name)
    os.rename(f"{file_name}",f"{filepath}/1.xlsx")

    driver.close()
    
    


if __name__ == "__main__":
    get_youth_cook()












