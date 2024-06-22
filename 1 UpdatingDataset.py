import json
import sys

sys.path.append('C:\\Users\\san20\\PycharmProjects\\Football\\UpdatingData')
import GettingPlayedMatchesLinks
import AddingPlayedMatchesToDataset


with open('Files/UpdatingDataset(ConfigurationFile).json', 'r') as file:
    configuration_data = json.load(file)

GettingPlayedMatchesLinks.GetPlayedMatchLinks(configuration_data)
AddingPlayedMatchesToDataset.AddPlayedMatchesToDataset(configuration_data)


