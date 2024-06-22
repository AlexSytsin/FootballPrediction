from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import pickle
from bs4 import BeautifulSoup
import DriverSettings
import json


def SomeUpdateNeeded(configuration_data):
    for liga in configuration_data["leagues_whoscored"]:
        if configuration_data["leagues_whoscored"][liga]["update_need"] == 1:
            return True
    return False
def GetSeasonIdsWhoScored(liga,configuration_data,driver):
    if len(configuration_data["leagues_whoscored"][liga]['season_ids'])!=(configuration_data["leagues_whoscored"][liga]["current_season"]-2012):
        a={}
        region_id=configuration_data["leagues_whoscored"][liga]["region_id"]
        tourn_id = configuration_data["leagues_whoscored"][liga]["tourn_id"]
        driver.get(f'https://www.whoscored.com/Regions/{region_id}/Tournaments/{tourn_id}')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        seasons=soup.find("select",id="seasons").find_all("option")
        for season in seasons:
            seas_year=int(season.text.split("/")[0])
            idd=int(season['value'].split("/")[6])
            if seas_year<=configuration_data["leagues_whoscored"][liga]["current_season"] and seas_year>=2013:
                a[seas_year]=idd
        if len(a)!=configuration_data["leagues_whoscored"][liga]["current_season"]-2012:
            raise Exception("Can't get season ids whoscored")
        a=dict(sorted(a.items()))
        configuration_data["leagues_whoscored"][liga]["season_ids"]=a

def GetLinksMonth(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    matches = soup.find("div", class_="TournamentFixtures-module_accordion__f-5gu").find_all("a",class_="Match-module_score__5Ghhj")
    tourn2=[]
    for match in matches:
        if(match.find("span").text.lstrip().rstrip()=="-"):
            tourn2.append([match["id"].replace("scoresBtn-","").lstrip().rstrip(),"Залупа"])
        else:
            tourn2.append([match["id"].replace("scoresBtn-", "").lstrip().rstrip(), "FT"])
    return tourn2


def KickNotPlayedMatches(matches):
    filtered_matches = [x[0] for x in matches if x[1] == "FT"]
    return filtered_matches

def GetPlayedMatchLinksFromWhoScored(configuration_data):
    if SomeUpdateNeeded(configuration_data):
        driver = DriverSettings.LoadDriverWho()
        for liga in configuration_data["leagues_whoscored"]:
            if configuration_data["leagues_whoscored"][liga]["update_need"] == 1:
                GetSeasonIdsWhoScored(liga, configuration_data, driver)

                region_id = configuration_data["leagues_whoscored"][liga]["region_id"]
                tourn_id = configuration_data["leagues_whoscored"][liga]["tourn_id"]
                season_ids = configuration_data["leagues_whoscored"][liga]["season_ids"]
                last_season = configuration_data["leagues_whoscored"][liga]["season"]

                all_matches = []
                for season in season_ids:
                    all_matches_seas = []
                    if int(season) >= int(last_season):
                        driver.get(
                            f"https://www.whoscored.com/Regions/{region_id}/Tournaments/{tourn_id}/Seasons/{season_ids[season]}/Stages/0/Fixtures")
                        time.sleep(0.5)

                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        selector = soup.find("select", id="stages")
                        if selector:
                            options = selector.find_all("option")
                            for option in options:
                                if option.text.lstrip().rstrip() == liga:
                                    link = option["value"]
                                    driver.get("https://www.whoscored.com" + link.replace("Show", "Fixtures"))
                                    break




                        show_dates = driver.find_element(By.CSS_SELECTOR, 'button[id="toggleCalendar"]')
                        show_dates.click()
                        show_years_button = driver.find_element(By.CSS_SELECTOR, 'button[class="DatePicker-module_buttonOff__5hWQd"]')
                        show_years_button.click()

                        years = driver.find_element(By.CSS_SELECTOR,'tbody[class="DatePicker-module_yearsTbody__QKmQu"]').find_elements(By.CSS_SELECTOR,'td')
                        year=years[1]
                        year.click()

                        months = driver.find_element(By.CSS_SELECTOR, 'tbody[class="DatePicker-module_monthsTbody__mt1iA"]').find_elements(By.CSS_SELECTOR,"tr")
                        for i in range(4):
                            for j in range(3):
                                if months[i].find_elements(By.CSS_SELECTOR, "td")[j].get_attribute("class") != "":
                                    months[i].find_elements(By.CSS_SELECTOR, "td")[j].click()
                                    time.sleep(1)
                                    matches = GetLinksMonth(driver)
                                    all_matches_seas = all_matches_seas + matches
                                    show_dates.click()
                                    months = driver.find_element(By.CSS_SELECTOR,'tbody[class="DatePicker-module_monthsTbody__mt1iA"]').find_elements(By.CSS_SELECTOR, "tr")

                        show_years_button = driver.find_element(By.CSS_SELECTOR,'button[class="DatePicker-module_buttonOff__5hWQd"]')
                        show_years_button.click()

                        years = driver.find_element(By.CSS_SELECTOR,'tbody[class="DatePicker-module_yearsTbody__QKmQu"]').find_elements(By.CSS_SELECTOR, 'td')
                        year = years[0]
                        year.click()

                        months = driver.find_element(By.CSS_SELECTOR,'tbody[class="DatePicker-module_monthsTbody__mt1iA"]').find_elements(By.CSS_SELECTOR, "tr")
                        for i in range(4):
                            for j in range(3):
                                if months[i].find_elements(By.CSS_SELECTOR, "td")[j].get_attribute("class") != "":
                                    months[i].find_elements(By.CSS_SELECTOR, "td")[j].click()
                                    time.sleep(1)
                                    matches = GetLinksMonth(driver)
                                    all_matches_seas = all_matches_seas + matches
                                    show_dates.click()
                                    months = driver.find_element(By.CSS_SELECTOR,'tbody[class="DatePicker-module_monthsTbody__mt1iA"]').find_elements(By.CSS_SELECTOR, "tr")

                        max_matches = configuration_data["leagues_whoscored"][liga]["max_matches"]
                        mmmm=[x[0] for x in all_matches_seas]
                        if len(set(mmmm)) != max_matches:
                            print(f"Got {len(set(mmmm))} matches out of {max_matches}")
                            raise "Didn't Get All Matches From WhoScored"

                        filtered_matches=KickNotPlayedMatches(all_matches_seas)

                        all_matches = all_matches + filtered_matches
                        configuration_data["leagues_whoscored"][liga]["season"] = season
                all_matches = list(reversed(all_matches))

                try:
                    with open(f'Files/Used_Links(whoscored)({liga}).pkl', 'rb') as file:
                        used_links = pickle.load(file)
                except FileNotFoundError:
                    used_links = []
                all_matches=list(set(all_matches)-set(used_links))

                with open(f'Files/Links(whoscored)({liga}).pkl', 'wb') as file:
                    pickle.dump(all_matches, file)

                configuration_data["leagues_whoscored"][liga]["update_need"] = 0

                with open("Files/UpdatingDataset(ConfigurationFile).json", 'w') as file:
                    json.dump(configuration_data, file, indent=4)

        driver.quit()



