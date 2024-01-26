from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from read_cook import read_json

DRIVER_PATH = 'chromedriver'
filepath = "youth_study/youth_cook"


def auto_login():
    name = "youth_study"
    cookies = read_json(name)
    chrome_options = Options()

    # UA 必须要是手机设备的
    UA = (
        "Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3"
    )
    mobileEmulation = {
        "deviceMetrics": {"width": 400, "height": 587, "pixelRatio": 3},
        "userAgent": UA,
    }

    # chrome_options.add_experimental_option("mobileEmulation", mobileEmulation)
    chrome_options.add_argument("--disable-blink-features=automationControlled")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])

    driver = webdriver.Chrome(executable_path=DRIVER_PATH,options=chrome_options)
    # 学生
    url = 'http://home.yngqt.org.cn/user/login.aspx'

    driver.implicitly_wait(5)
    driver.get(f'{url}')
    for cook in cookies:
        if 'expiry' in cook:
            del cook['expiry']
        print(cook)
    driver.add_cookie(cook)
    driver.refresh()
    # time.sleep(100)
auto_login()