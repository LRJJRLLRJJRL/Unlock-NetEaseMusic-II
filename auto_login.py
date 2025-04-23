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
    browser.add_cookie({"name": "MUSIC_U", "value": "00AD1A8DA791720FAFB523317E80BC5B2C487FB2B4D4DC2FD02C57EA22C95AA26A0BCE19D00FE0F7F06C0FBA1411B5DED6055CDF33416A22BBB7FDB5AAC6CF28E39A0567C928D8CDA5D20C4ABE4B09FEBEE72A651AAA5F0E625585AFF19BC82ADA563874AAE8E03E1CC8D791182F2356CBBD9A01D4BFF49FD9E044D45E41B4F0B0CC815F159D3FE860A1858DDF33AA7FF408F1F6B46A5A9E1D4D5749462884A0B49D5794CFA02727CF7D49A9256D31B85943CAD7E4F2D8E3D5B6EC8B79B3774DF3B3C631C32FF08802F9AD618B8ABBF5AAFA07F8DA656B2E718E0750E0C7D8B26F664082EDFF2F8B33987EF52CAD77785120AFACBFBACD07C8E79497A16ACE9D97E45FA231AD171B2FBAD3284ADE8CD9076AC5A615889C297F5C1D5FDC137232077223E04C696B4368CFE7C53B3E76F530459D1D2839A67F6D515422BC99E5D5BEB75A6E2DDC37CC56AE379139792FE804"})
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
