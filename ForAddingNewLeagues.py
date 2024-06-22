import json
import pandas as pd

with open('Files/FilteringDataset(ConfigurationFile).json', 'r') as file:
    configuration_data = json.load(file)


dict_team=configuration_data["FlashScoreToWhoScoredDict"]
dataset1=pd.read_pickle("Files/Dataset(raw)(flashscore)(laliga).pkl")
dataset2=pd.read_pickle("Files/Dataset(raw)(whoscored)(LaLiga).pkl")


unique_values1 = sorted(list(dataset1['Team1_prematch'].replace(dict_team).unique()))
unique_values2 = sorted(list(dataset2['Team1_prematch'].unique()))


print("FlashScore")
print(unique_values1)
print("WhoScored")
print(unique_values2)


print("FlashScore")
print("Team_name Count: ",dataset1["Team1_prematch"].count())
print("Dataset length: ",len(dataset1))
print("WhoScored")
print("Team_name Count: ",dataset2["Team1_prematch"].count())
print("Dataset length: ",len(dataset2))
