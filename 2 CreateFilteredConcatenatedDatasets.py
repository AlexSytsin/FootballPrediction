import json
import sys
import time

import pandas as pd
import pickle
import warnings

warnings.filterwarnings("ignore", category=Warning)
pd.set_option('future.no_silent_downcasting', True)
pd.set_option('display.max_columns', None)
def MergeDatasets(dataset_flash,dataset_who,merge_columns=['Year_prematch', 'Month_prematch','House_prematch','Team1_prematch', 'Team2_prematch', 'Score_Team1_postmatch', 'Score_Team2_postmatch']):
    suffixes = ('', '_xxx_')
    dataset_flash[merge_columns]=dataset_flash[merge_columns].astype(str)
    dataset_who[merge_columns] = dataset_who[merge_columns].astype(str)
    merged_dataset = pd.merge(dataset_who, dataset_flash, on=merge_columns, how='inner', suffixes=suffixes)
    filtered_columns = [col for col in merged_dataset.columns if not col.endswith('_xxx_')]
    merged_dataset = merged_dataset[filtered_columns]
    return merged_dataset


def AddFlags(dataset,columns):
    for column in columns:
        dataset[column + "_flag"] = dataset[column + "_team1_postmatch"].notnull().astype(int)
    dictionary = dict.fromkeys(columns, 0)
    dataset=FillWithValues(dataset,dictionary,["_team1_postmatch","_team2_postmatch"])
    return dataset

def Encode(dataset,columns,encoding_dict,postfixes):
    for column in columns:

        cur_cols = [column + word for word in postfixes]
        values = list(set(dataset[cur_cols].values.ravel()))

        for value in values:
            if value not in encoding_dict:
                encoding_dict[value] = len(encoding_dict)
        dataset[cur_cols] = dataset[cur_cols].replace(encoding_dict)

    return dataset,encoding_dict

def FillWithValues(dataset,columns_with_values,postfixes):
    for column in columns_with_values:
        cur_cols = [column + word for word in postfixes]
        dataset[cur_cols] = dataset[cur_cols].fillna(columns_with_values[column])
    dataset["Disqualification_postmatch"] = dataset["Disqualification_postmatch"].fillna(0)
    return dataset

def FillStylesAndShit(dataset):
    columns=[
        "style",
        "strength",
        "weakness",
        "forecast",
      "missHighLeft",
      "missHighCentre",
      "missHighRight",
      "missLeft",
      "missRight",
      "postLeft",
      "postCentre",
      "postRight",
      "onTargetHighLeft",
      "onTargetHighCentre" ,
      "onTargetHighRight"   ,
      "onTargetLowLeft" ,
      "onTargetLowCentre" ,
      "onTargetLowRight" ]
    for column in dataset.columns:
        for column1 in columns:
            if column1 in column:
                dataset[column] = dataset[column].fillna(0)
                break
    return dataset
def Drop(dataset,columns,postfixes):
    for column in columns:
        cur_cols = [column + word for word in postfixes]
        intersection = list(set(cur_cols) & set(dataset.columns))
        dataset = dataset.drop(columns=intersection)
    if 'WhoScoredPostMatchStats_flag' in dataset.columns:
        dataset=dataset.drop(columns=['WhoScoredPostMatchStats_flag'])
    return dataset

def DropByMinute(dataset):
    h2h = dataset[[col for col in dataset.columns if 'h2h' in col]]
    dataset= dataset.filter(regex='^(?!.*_\d+_)')
    dataset=pd.concat([dataset,h2h],axis=1)
    columns_to_drop = [col for col in dataset.columns if ('_44+' in col or '_89+' in col)]
    dataset=dataset.drop(columns=columns_to_drop)
    return dataset


def HandleRatings(dataset):
    for j in range(1,3):
        for k in range(6):
            dataset[f"ratings_{15 * k}-{15 * (k + 1)}_team{j}_postmatch"]=dataset[f"ratings_{15*(k+1)-1}_team{j}_postmatch"]
            for i in range(2,7):
                dataset[f"ratings_{15 * k}-{15 * (k + 1)}_team{j}_postmatch"] =dataset[f"ratings_{15 * k}-{15 * (k + 1)}_team{j}_postmatch"].fillna( dataset[f"ratings_{15*(k+1)-i}_team{j}_postmatch"])
            dataset[f"ratings_{15 * k}-{15 * (k + 1)}_team{j}_postmatch"] = dataset[
                f"ratings_{15 * k}-{15 * (k + 1)}_team{j}_postmatch"].fillna(6)

    return dataset

def GroupByMinute(dataset,columns):
    for column in columns:
        columns2 = dataset.columns
        for j in range(1, 3):
            for i in range(6):
                start = 15 * i
                end = start + 15
                cols_to_sum = [f'{column}_{minute}_team{j}_postmatch' for minute in range(start, end) if
                               f'{column}_{minute}_team{j}_postmatch' in columns2]
                if end == 45:
                    cols_to_sum2 = [f'{column}_44+{minute}_team{j}_postmatch' for minute in range(40) if
                                    f'{column}_44+{minute}_team{j}_postmatch' in columns2]
                    cols_to_sum += cols_to_sum2
                if end == 90:
                    cols_to_sum2 = [f'{column}_89+{minute}_team{j}_postmatch' for minute in range(40) if
                                    f'{column}_89+{minute}_team1_postmatch' in columns2]
                    cols_to_sum += cols_to_sum2
                dataset[f'{column}_{start}-{end}_team{j}_postmatch'] = dataset[cols_to_sum].sum(axis=1)
    return dataset

def FilterDataset(dataset, configuration_data):

    dataset=Drop(dataset, configuration_data["drop_columns_postmatch"], ["_team1_postmatch", "_team2_postmatch"])
    dataset = FillWithValues(dataset, configuration_data["fill_with_value_columns"], ["_team1_postmatch", "_team2_postmatch"])
    dataset = AddFlags(dataset, configuration_data["add_flag_columns"])
    dataset,configuration_data["Teams_Ecnoding_dict"] = Encode(dataset, ["Team1", "Team2"], configuration_data["Teams_Ecnoding_dict"], ["_prematch"])
    dataset, configuration_data["House_dict"] = Encode(dataset, ["House"],configuration_data["House_dict"], ["_prematch"])
    dataset, configuration_data["League_dict"] = Encode(dataset, ["Tournament"],configuration_data["League_dict"], ["_prematch"])
    dataset=GroupByMinute(dataset,configuration_data["group_by_minute_columns"])
    dataset=FillStylesAndShit(dataset)
    dataset=HandleRatings(dataset)
    dataset=DropByMinute(dataset)

    return dataset,configuration_data

def CreateFilteredConcatenatedDatasets(configuration_data_upd,configuration_data_filt):
    for liga_flash, liga_who in zip(configuration_data_upd["leagues_flashscore"],
                                    configuration_data_upd["leagues_whoscored"]):

        with open(f'Files/Dataset(raw)(flashscore)({liga_flash}).pkl', 'rb') as file:
            dataset_flash = pickle.load(file)
        with open(f'Files/Dataset(raw)(whoscored)({liga_who}).pkl', 'rb') as file:
            dataset_who = pickle.load(file)

        dataset_flash["Team1_prematch"] = dataset_flash["Team1_prematch"].replace(
            configuration_data_filt["FlashScoreToWhoScoredDict"], regex=False)
        dataset_flash["Team2_prematch"] = dataset_flash["Team2_prematch"].replace(
            configuration_data_filt["FlashScoreToWhoScoredDict"], regex=False)

        z=MergeDatasets(dataset_flash, dataset_who)

        dataset,configuration_data_filt = FilterDataset(z,configuration_data_filt)

        print(dataset.shape)
        print(dataset_who.shape)
        print(dataset_flash.shape)
        print()
        with open('Files/FilteringDataset(ConfigurationFile).json', 'w') as file:
            json.dump(configuration_data_filt,file,indent=4)

        with open(f'Files/Dataset(filtered)({liga_who}).pkl', 'wb') as file:
            pickle.dump(dataset,file)


with open('Files/FilteringDataset(ConfigurationFile).json', 'r') as file:
    configuration_data_filt = json.load(file)
with open('Files/UpdatingDataset(ConfigurationFile).json', 'r') as file:
    configuration_data_upd = json.load(file)


CreateFilteredConcatenatedDatasets(configuration_data_upd,configuration_data_filt)
