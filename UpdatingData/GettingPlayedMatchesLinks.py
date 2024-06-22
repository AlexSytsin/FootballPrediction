import GettingPlayedMatchLinksFromFlashScore
import GettingPlayedMatchLinksFromWhoScored
import pickle

def FileIsEmpty(path):
    try:
        with open(path, 'rb') as file:
            listt = pickle.load(file)
            if len(listt) == 0:
                return True
            return False
    except FileNotFoundError:
        return True
def AllMatchFilesAreEmpty(configuration_data):
    for liga in configuration_data["leagues_flashscore"]:
        if not FileIsEmpty(f'Links(flashscore)({liga}).pkl') and configuration_data["leagues_flashscore"][liga]["update_need"]==1:
            return False
    for liga in configuration_data["leagues_whoscored"] :
        if not FileIsEmpty(f'Links(whoscored)({liga}).pkl') and configuration_data["leagues_whoscored"][liga]["update_need"]==1:
            return False
    return True

def GetPlayedMatchLinks(configuration_data):
    if AllMatchFilesAreEmpty(configuration_data):
        GettingPlayedMatchLinksFromFlashScore.GetPlayedMatchLinksFromFlashScore(configuration_data)
        GettingPlayedMatchLinksFromWhoScored.GetPlayedMatchLinksFromWhoScored(configuration_data)
