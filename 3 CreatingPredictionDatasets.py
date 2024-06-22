import json
import pickle
import pandas as pd
import sys
from tqdm import tqdm
sys.path.append('PredictionFeatures')
import CreatePredictionFeatures


with open('Files/CreatingNewFeatures(ConfigurationFile).json', 'r') as file:
    configuration_data = json.load(file)
with open('Files/UpdatingDataset(ConfigurationFile).json', 'r') as file:
    configuration_data_upd = json.load(file)

def GetRowsOnlyPresentInFirstDataset(dataset1, dataset2, columns=['Year_prematch', 'Month_prematch','House_prematch','Team1_prematch', 'Team2_prematch', 'Score_Team1_postmatch', 'Score_Team2_postmatch']):
    suffixes = ('','_xxx_')
    joined_dataset = pd.merge(dataset1, dataset2, on=columns, how='left', indicator=True, suffixes=suffixes,validate="one_to_one")
    missing_rows = joined_dataset[joined_dataset['_merge'] == 'left_only']
    missing_rows = missing_rows.drop(columns='_merge')
    filtered_columns = [col for col in missing_rows.columns if not col.endswith('_xxx_')]
    missing_rows = missing_rows[filtered_columns]
    return missing_rows

def FindFirstUnhandledRow(configuration_data,league):
    min=-1
    for feature in configuration_data["Leagues"][league]:
        if min==-1 or feature["count"]<min:
            min=feature["count"]
    return min

def DocumentAllFeatures(configuration_data,league):
    if not configuration_data["Leagues"] or league not in configuration_data["Leagues"]:
        configuration_data["Leagues"][league] = {}
    for feature in configuration_data["Features"]:
        if feature not in configuration_data["Leagues"][league]:
            configuration_data["Leagues"][league][feature]={}
            configuration_data["Leagues"][league][feature]["count"] = 0
            configuration_data["Leagues"][league][feature]["info"] = {}
    return configuration_data


def MaintainNewPredictionFeatures(configuration_data,configuration_data_upd):
    for league in configuration_data_upd["leagues_whoscored"]:

        with open(f'Files/Dataset(filtered)({league}).pkl', 'rb') as file:
            dataset=pickle.load(file)

        try:
            with open(f'Files/Dataset(full-ready)({league}).pkl', 'rb') as file:
                new_dataset = pickle.load(file)
        except FileNotFoundError:
            columns=['Year_prematch', 'Month_prematch','House_prematch','Team1_prematch', 'Team2_prematch', 'Score_Team1_postmatch', 'Score_Team2_postmatch']
            new_dataset =pd.DataFrame(columns=columns)

        addition_dataset=GetRowsOnlyPresentInFirstDataset(dataset,new_dataset)

        sort_columns=["Year_prematch","Month_prematch","Day_prematch"]
        addition_dataset.sort_values(by=sort_columns,inplace=True)

        new_dataset= pd.concat([new_dataset, addition_dataset], axis=0,ignore_index=True)
        
        configuration_data=DocumentAllFeatures(configuration_data,league)

        new_dataset,configuration_data=CreatePredictionFeatures.CreateFeatures(new_dataset,configuration_data,league)

        with open(f'Files/Dataset(full-ready)({league}).pkl', 'wb') as file:
            pickle.dump(new_dataset,file)

    with open('Files/CreatingNewFeatures(ConfigurationFile).json','w') as file:
         json.dump(configuration_data,file,indent=4)



MaintainNewPredictionFeatures(configuration_data,configuration_data_upd)