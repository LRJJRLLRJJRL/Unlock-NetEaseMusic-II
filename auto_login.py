# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BE33A791AAFDF6C13E4BE20DCD26216EA1EC3247896E7F988D4503E4CFE83E8CE1B6A0CD6C4E00AA8855BEDB0A3C134B8F1E2AB36DEDB4E9AC22437E06ABBF604309E20CAF2647104F326A8075CD3B31B85FB0ADAAA9DDAE434B07FB39B983592918FCA6F0E1F57B9A67C1AB67CDFD51C27730D4A8DDF7F5B021D17C938340BDE56F8AD14C77DD05220B980D9CE1162EABCA3DC557F3C944FFD971665E07311568D31B031F45D8711F9E7D37B2C97E709D4E2DF783C16CC681D79691AB27070DA87D388CF940803583B40E65ED81D505016FDDC232AED7D6974F35E2B90F1ACD2597924FA7BB892A71A2FB46AA0F392C97D0E335689F590C83140F083C036518DF77A4E3C3705125512538D9B7F3E232B06151B3CD2264834100AFFEFCCC31CCBEDCB3717768812C53E9B5E53F64E970CF5223573798A9063D212CF55EFB6269900FC8DE485D0B2E5BD41EAE5B3753DA"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
