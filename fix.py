import pickle
import time

import pandas as pd

pd.set_option('display.max_columns', None)

z=f'Files/Dataset(raw)(whoscored)(LaLiga).pkl'
z1=f'Files/Dataset(raw)(whoscored)(LaLiga)(dup).pkl'
columns=[
        "shotsTotal",
        "shotsOffTarget",
        "shotsOnTarget",
        "clearances",
        "interceptions",
        "possession",
        "touches",
        "passesTotal",
        "passesAccurate",
        "passesKey",
        "aerialsTotal",
        "aerialsWon",
        "offensiveAerials",
        "defensiveAerials",
        "cornersTotal",
        "cornersAccurate",
        "throwInsTotal",
        "throwInsAccurate",
        "foulsCommited",
        "tacklesTotal",
        "tackleSuccessful",
        "dribbledPast",
        "dribblesWon",
        "dribblesAttempted",
        "dispossessed",
        "ratings"
        ]

with open(z, 'rb') as file:
    dataset=pickle.load(file)

new_dataset=pd.DataFrame()
pos_cols=dataset.columns
new_dataset=[]
for index, row in dataset.iterrows():
    print(index)
    minute1=int(row["EndMinute1_postmatch"])
    minute2 = int(row["EndMinute2_postmatch"])
    for column in columns:
        for i in range(1,3):
            for j in range(minute1-44):
                col=f"{column}_{j+45}_team{i}_postmatch"
                if col in pos_cols:
                    row[f"{column}_44+{j+1}_team{i}_postmatch"]=row[col]
            for j in range(45):
                col=f"{column}_{minute1+j+1}_team{i}_postmatch"
                if col in pos_cols:
                    row[f"{column}_{j+45}_team{i}_postmatch"]=row[col]
            for j in range(minute2-89):
                col=f"{column}_{j+46+minute1}_team{i}_postmatch"
                if col in pos_cols:
                    row[f"{column}_89+{j+1}_team{i}_postmatch"]=row[col]
    new_dataset.append(row)
new_dataset=pd.concat(new_dataset,axis=1).T

with open(z, 'wb') as file:
    pickle.dump(new_dataset,file)
with open(z1, 'wb') as file:
    pickle.dump(dataset,file)