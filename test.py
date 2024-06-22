import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pickle
import traceback
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import datetime
import pickle
from bs4 import BeautifulSoup
import json

pd.set_option('display.max_columns', None)

dataset1=pd.read_pickle("Files/Dataset(raw)(flashscore)(serie-a).pkl")
dataset2=pd.read_pickle("Files/Dataset(raw)(whoscored)(Serie A).pkl")



print(dataset1[dataset1["Round_prematch"]=="Additional match"][["Year_prematch","Month_prematch","Day_prematch","Team1_prematch","Team2_prematch"]])


# Get unique values for a specific column
unique_values1 = list(dataset1['Team1_prematch'].unique())
unique_values2 = list(dataset2['Team1_prematch'].unique())


"""

print(dataset2["Team1_prematch"].count())

print(unique_values1)
print(unique_values2)

z=dataset2[dataset2["Team1_prematch"].isna()]
non_empty_cols = z.columns[z.count() > 0]
print(z["Scheme1_prematch"])


def find_missing_rows(dataset1, dataset2, columns):
    suffixes = ('', '_xxx_')
    joined_dataset = pd.merge(dataset1, dataset2, on=columns, how='left', indicator=True,suffixes=suffixes)
    missing_rows = joined_dataset[joined_dataset['_merge'] == 'left_only']
    missing_rows = missing_rows.drop(columns='_merge')
    filtered_columns = [col for col in missing_rows.columns if not col.endswith('_xxx_')]
    missing_rows=missing_rows[filtered_columns]
    return missing_rows


dataset1 = pd.DataFrame({
                         'A': [1, 2, 3, 4, 1],
                         'B': ['a', 'b', 'c', 'd', "a"],
                         'C': [True, False, True, False, None],

})
columns=['A',"B"]
dataset2 = pd.DataFrame(columns=columns)

# Создание второго датасета, который содержит первый датасет



# Вызов функции
missing_rows = find_missing_rows(dataset1, dataset2, ['A', 'B'])

# Вывод результатов
print("Отсутствующие строки:")
print(missing_rows)


with open(f'Files/Used_Links(flashscore)(serie-a).pkl', 'rb') as file:
    dataset_who=pickle.load(file)
if "https://www.flashscore.com/match/f1nTGXc7" in dataset_who:
    print("in")
dataset_who.remove("https://www.flashscore.com/match/f1nTGXc7")
with open(f'Files/Used_Links(flashscore)(serie-a).pkl', 'wb') as file:
    pickle.dump(dataset_who,file)



with open(f'Files/Links(flashscore)(serie-a).pkl', 'rb') as file:
    dataset_who=pickle.load(file)
if "https://www.flashscore.com/match/f1nTGXc7" in dataset_who:
    print("in")
dataset_who.append("https://www.flashscore.com/match/f1nTGXc7")
with open(f'Files/Links(flashscore)(serie-a).pkl', 'wb') as file:
    pickle.dump(dataset_who,file)
"""
#print(dataset1.describe(include="all"))
#print(dataset1[dataset1["Season_prematch","PredScore_Team1_prematch","PredScore_Team2_prematch","Scheme1_prematch","Scheme2_prematch","Injuries1_prematch","Injuries2_prematch"].isnull()])
# dataset_who.loc[6840,["Season_prematch","PredScore_Team1_prematch","PredScore_Team2_prematch","Scheme1_prematch","Scheme2_prematch","Injuries1_prematch","Injuries2_prematch"]]=[2014,1,1,4231,4231,6,3]
# dataset_who.loc[6841,["Season_prematch","PredScore_Team1_prematch","PredScore_Team2_prematch","Scheme1_prematch","Scheme2_prematch","Injuries1_prematch","Injuries2_prematch"]]=[2014,1,1,4231,4231,3,6]
# with open(f'Files/Dataset(raw)(whoscored)(LaLiga).pkl', 'wb') as file:
#     pickle.dump(dataset_who,file)
#print(dataset_flash[dataset_flash["Goalkeeper Saves_team1_postmatch"].isnull()])
# dataset_flash.loc[8056,["Ball Possession_team1_postmatch", "Ball Possession_team2_postmatch","Free Kicks_team1_postmatch","Free Kicks_team2_postmatch","Goalkeeper Saves_team1_postmatch","Goalkeeper Saves_team2_postmatch","Yellow Cards_team1_postmatch","Yellow Cards_team2_postmatch","Red Cards_team1_postmatch","Red Cards_team2_postmatch"]]=[35,65,14,11,6,2,4,5,1,0]
# dataset_flash.loc[8057,["Ball Possession_team1_postmatch", "Ball Possession_team2_postmatch","Free Kicks_team1_postmatch","Free Kicks_team2_postmatch","Goalkeeper Saves_team1_postmatch","Goalkeeper Saves_team2_postmatch","Yellow Cards_team1_postmatch","Yellow Cards_team2_postmatch","Red Cards_team1_postmatch","Red Cards_team2_postmatch"]]=[35,65,11,14,2,6,5,4,0,1]

# with open(f'Files/Dataset(raw)(flashscore)(laliga).pkl', 'wb') as file:
#     pickle.dump(dataset_flash,file)
#print(dataset1[dataset1["EndMinute1_postmatch"]==0])

"""
dataset_flash["Team1_prematch"] = dataset_flash["Team1_prematch"].replace(
            configuration_data_filt["FlashScoreToWhoScoredDict"], regex=False)
dataset_flash["Team2_prematch"] = dataset_flash["Team2_prematch"].replace(
            configuration_data_filt["FlashScoreToWhoScoredDict"], regex=False)
print(sorted(dataset_flash["Team1_prematch"].unique()))
print(sorted(dataset_who["Team1_prematch"].unique()))
print(dataset_flash.shape)
print(dataset_who.shape)
dataset_flash['Year_prematch'] =dataset_flash['Year_prematch'].astype(int)
dataset_flash['Month_prematch'] =dataset_flash['Month_prematch'].astype(int)
dataset_flash['Score_Team1_postmatch'] =dataset_flash['Score_Team1_postmatch'].astype(int)
dataset_flash['Score_Team2_postmatch'] =dataset_flash['Score_Team2_postmatch'].astype(int)
dataset_flash['House_prematch'] =dataset_flash['House_prematch'].astype(str)
dataset_flash['Team1_prematch'] =dataset_flash['Team1_prematch'].astype(str)
dataset_flash['Team2_prematch'] =dataset_flash['Team2_prematch'].astype(str)
dataset_who['Year_prematch'] =dataset_who['Year_prematch'].astype(int)
dataset_who['Month_prematch'] =dataset_who['Month_prematch'].astype(int)
dataset_who['Score_Team1_postmatch'] =dataset_who['Score_Team1_postmatch'].astype(int)
dataset_who['Score_Team2_postmatch'] =dataset_who['Score_Team2_postmatch'].astype(int)
dataset_who['House_prematch'] =dataset_who['House_prematch'].astype(str)
dataset_who['Team1_prematch'] =dataset_who['Team1_prematch'].astype(str)
dataset_who['Team2_prematch'] =dataset_who['Team2_prematch'].astype(str)
merged_dataset= MergeDatasets(dataset_flash, dataset_who)
print(merged_dataset.shape)
print(dataset_flash[['Year_prematch', 'Month_prematch','House_prematch','Team1_prematch', 'Team2_prematch', 'Score_Team1_postmatch', 'Score_Team2_postmatch']].dtypes)
print(dataset_who[['Year_prematch', 'Month_prematch','House_prematch','Team1_prematch', 'Team2_prematch', 'Score_Team1_postmatch', 'Score_Team2_postmatch']].dtypes)



#strings=list(dataset.columns)
#filtered_strings = [s for s in strings if not re.search(r'_\d+_', s)]
#print(strings)
#print(filtered_strings)
#filtered_df = dataset[dataset['Year_prematch'].isnull() ]
#print(filtered_df[["House_prematch",'Team1_prematch',"Team2_prematch","Season_prematch",'PredScore_Team1_prematch','PredScore_Team2_prematch']])
#print(dataset.shape)
"""
"""
with open(f'Files/Links(flashscore)(serie-a).pkl', 'rb') as file:
    h=pickle.load(file)
print(len(h))
with open(f'Files/Used_Links(whoscored)(Serie A).pkl', 'rb') as file:
    h=pickle.load(file)
print(len(h))
with open(f'Files/Dataset(raw)(flashscore)(serie-a).pkl', 'rb') as file:
    h=pickle.load(file)
print(len(h))

# Создаем исходный датафрейм
data = {'Fruit': ['Apple', 'Banana', 'Apple', 'Orange', 'Pear'],
        'Color': ['Red', 'Yellow', 'Red', 'Orange', 'Green']}
df = pd.DataFrame(data)

# Получаем список уникальных значений из двух столбцов
unique_values = list(set(df[['Fruit', 'Color']].values.ravel()))

# Выводим список уникальных значений
print(unique_values)


# Load the dataset
dataset1=pd.read_pickle("Files/Dataset(raw)(flashscore)(premier-league).pkl")
dataset2=pd.read_pickle("Files/Dataset(raw)(whoscored)(Premier League).pkl")

# Get unique values for a specific column
unique_values1 = sorted(list(dataset1['Team1_prematch'].unique()))
unique_values2 = sorted(list(dataset2['Team1_prematch'].unique()))


print(unique_values1)
print(unique_values2)




import pandas as pd

# Создаем исходный датасет
data = {'ID': [1, 2, 3, 4, 5],
        'Fruit': ['Apple', 'Banana', 'Apple', 'Orange', 'Pear']}
dataset = pd.DataFrame(data)

# Определяем словарь для замены значений
replacement_dict = {'Apple': 'Red Apple', 'Banana': 'Yellow Banana', 'Orange': 'Orange Fruit'}

# Заменяем значения в столбце 'Fruit' с использованием словаря и оставляем значения без изменений
dataset['Fruit'] = dataset['Fruit'].replace(replacement_dict, regex=False)

# Выводим обновленный датасет
print(dataset)

"""

