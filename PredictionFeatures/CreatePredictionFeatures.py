from tqdm import tqdm
from tqdm import trange
def CreateTable(new_dataset, configuration_data,league):
    name="Table"
    data=configuration_data["Leagues"][league]["Table"]
    info=data["info"]
    for index in trange(data["count"],len(new_dataset),desc="Table"):
        pass

    configuration_data["Leagues"][league]["Table"]=data
    return new_dataset, configuration_data


def CreateFeatures(new_dataset,configuration_data,league):
    CreateTable(new_dataset,configuration_data,league)