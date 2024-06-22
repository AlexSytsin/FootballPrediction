import sys
import pickle

import pandas as pd
import AddingMatchFlashscore
import AddingMatchWhoScored
import DriverSettings

def Save(used_links,links,dataset,liga,site):
    with open(f'Files/Used_Links({site})({liga}).pkl', 'wb') as file:
        pickle.dump(used_links, file)
    with open(f'Files/Links({site})({liga}).pkl', 'wb') as file:
        pickle.dump(links, file)
    with open(f'Files/Dataset(raw)({site})({liga}).pkl', 'wb') as file:
        pickle.dump(dataset,file)


def AddPlayedMatchesToDataset(configuration_data):
    driver=DriverSettings.LoadDriverFlash()
    for liga in configuration_data["leagues_flashscore"]:
        with open(f'Files/Links(flashscore)({liga}).pkl', 'rb') as file:
            links=pickle.load(file)
        try:
            with open(f'Files/Dataset(raw)(flashscore)({liga}).pkl', 'rb') as file:
                dataset=pickle.load(file)
        except FileNotFoundError:
            dataset = pd.DataFrame()

        try:
            with open(f'Files/Used_Links(flashscore)({liga}).pkl', 'rb') as file:
                used_links = pickle.load(file)
        except FileNotFoundError:
            used_links=[]
        z=range(len(links))
        for i in z:
            try:
                dataset=AddingMatchFlashscore.AddMatchFlashscore(dataset,links[0],driver)
            except:
                Save(used_links,links,dataset,liga,"flashscore")
                raise
            used_links.append(links.pop(0))
        Save(used_links,links, dataset, liga, "flashscore")


    driver.quit()

    driver=DriverSettings.LoadDriverWho()

    for liga in configuration_data["leagues_whoscored"]:
        with open(f'Files/Links(whoscored)({liga}).pkl', 'rb') as file:
            links = pickle.load(file)
        try:
            with open(f'Files/Dataset(raw)(whoscored)({liga}).pkl', 'rb') as file:
                dataset = pickle.load(file)
        except FileNotFoundError:
            dataset = pd.DataFrame()

        try:
            with open(f'Files/Used_Links(whoscored)({liga}).pkl', 'rb') as file:
                used_links = pickle.load(file)
        except FileNotFoundError:
            used_links=[]
        z = range(len(links))
        for i in z:
            try:
                dataset = AddingMatchWhoScored.AddMatchWhoScored( dataset,links[0], driver)
            except:
                Save(used_links,links, dataset, liga, "whoscored")
                raise
            used_links.append(links.pop(0))
        Save(used_links,links, dataset, liga, "whoscored")

    driver.quit()