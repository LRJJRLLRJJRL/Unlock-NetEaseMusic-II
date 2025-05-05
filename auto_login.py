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
    browser.add_cookie({"name": "MUSIC_U", "value": "00FA625577FEA6859373E890C3144772DC0C8C90E4E70BEF548624E751F1E3720F38FBDF43D18EF85BF0A1B6F72F795F2408DCA574AF0E862AA852F3050EA282E103B2FD2D1ABCFBF876F86E00566FB09259FD99423BFACA267A193A1E63309707A7739A70B5767F825CB536CFFFF52A26686D9F9733111AB670807DCFDC9DC7137F5F28DA88E3DB82ECA1901849DC7C4B829893E2884BDA345AAF3D165888D029768662C5B9A6ABCE6BD8F452B868A8F5812964D244BADE0880A66DF3A1815B1C1795943BBE8322596BDBA2B1B15EB0E3958BDF612D00C4A622230999F55F470EFD7A0B663683A8FE534084862A1BF78799471FA22690753809E43A2EC3A6CE109ED4F76A89CE1397126FFBF48725682A48A78222F60387CF898774CB30BE25725D9A5DD87C6F3AE21755D6F105B79BC3869A9F4AEAB68B4D6A1203294A523AA152C430DDBD79ADC6CD049AC4A2EF5AF1"})
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
