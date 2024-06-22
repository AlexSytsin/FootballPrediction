from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import pickle
import DriverSettings
from bs4 import BeautifulSoup
import json

def ShowMoreMatches(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    button=soup.find("a",class_="event__more")
    if button:
        return True
    else:
        return False

def SomeUpdateNeeded(configuration_data):
    for liga in configuration_data["leagues_flashscore"]:
        if configuration_data["leagues_flashscore"][liga]["update_need"] == 1:
            return True
    return False

def GetAllMatchesSeason(driver):
    list_of_matches=[]
    while ShowMoreMatches(driver):
        clickable_element = driver.find_element(By.CSS_SELECTOR, 'a.event__more')
        driver.execute_script("arguments[0].click();", clickable_element)
        time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    elements = soup.find_all(class_="event__match")
    for element in elements:
        list_of_matches.append("https://www.flashscore.com/match/" + element.get('id').split("_")[2])

    return list_of_matches

def GetPlayedMatchLinksFromFlashScore(configuration_data):
    if SomeUpdateNeeded(configuration_data):
        driver = DriverSettings.LoadDriverFlash()

        for liga in configuration_data["leagues_flashscore"]:
            all_matches = []
            if configuration_data["leagues_flashscore"][liga]["update_need"] == 1:
                league = configuration_data["leagues_flashscore"][liga]
                country = league["country_title"]
                name = league["name"]
                season = league["season"]

                driver.get(f"https://www.flashscore.com/football/{country}/{liga}-{season}-{season + 1}/results/")
                matches = GetAllMatchesSeason(driver)
                while len(matches) >= configuration_data["leagues_flashscore"][liga]['max_matches']:
                    all_matches = matches + all_matches
                    season += 1
                    driver.get(f"https://www.flashscore.com/football/{country}/{liga}-{season}-{season + 1}/results/")
                    matches = GetAllMatchesSeason(driver)
                all_matches = matches + all_matches

                try:
                    with open(f'Files/Used_Links(flashscore)({liga}).pkl', 'rb') as file:
                        used_links = pickle.load(file)
                except FileNotFoundError:
                    used_links = []
                all_matches=list(set(all_matches)-set(used_links))
                with open(f'Files/Links(flashscore)({name}).pkl', 'wb') as file:
                    pickle.dump(all_matches, file)
                configuration_data["leagues_flashscore"][name]["season"] = season
                configuration_data["leagues_flashscore"][name]["update_need"] = 0
                with open("Files/UpdatingDataset(ConfigurationFile).json", 'w') as file:
                    json.dump(configuration_data, file, indent=4)
        driver.quit()
