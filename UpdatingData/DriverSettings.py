from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


def LoadDriverFlash():
    o = Options()
    o.add_experimental_option("detach", True)
    o.add_argument('--window-size=900,1200')
    o.page_load_timeout = 200
    o.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=o)
    driver.get("https://www.flashscore.com/")
    time.sleep(1)
    button = driver.find_element(By.CSS_SELECTOR, 'button[id="onetrust-accept-btn-handler"]')
    button.click()
    return driver

def LoadDriverWho():
    o = Options()
    o.add_experimental_option("detach", True)
    o.add_argument('--window-size=900,1200')
    o.page_load_timeout = 200
    o.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=o)
    return driver

