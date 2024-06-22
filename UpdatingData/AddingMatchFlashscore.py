import time
from bs4 import BeautifulSoup
import pandas as pd


def GetMatchStats(soup):
    stat_groups = soup.find_all('div', {'data-testid': 'wcl-statistics'})
    stats = []
    for group in stat_groups:
        ss = group.find_all("strong")
        stat1 = ss[0].text.lstrip().rstrip().replace("%", "")
        name_stat = ss[1].text.lstrip().rstrip()
        stat2 = ss[2].text.lstrip().rstrip().replace("%", "")
        stats.append([stat1, stat2, name_stat])
    return stats

def GetDate(soup):

    date = soup.find("div", class_="duelParticipant__startTime").find("div").text.lstrip().rstrip().split(" ")[0]
    day = int(date.split(".")[0])
    month = int(date.split(".")[1])
    year = int(date.split(".")[2])

    return day,month,year

def GetScore(soup):
    score = soup.find("div", class_="duelParticipant").find("div", class_="detailScore__wrapper").find_all("span")

    score_home = score[0].text.lstrip().rstrip()
    score_away = score[2].text.lstrip().rstrip()

    return score_home,score_away

def GetTeamNames(soup):
    teams_info = soup.find("div", class_="duelParticipant")
    team_home = teams_info.find("div", class_="duelParticipant__home").find("a",
                                                                            class_='participant__participantName').text.lstrip().rstrip()

    team_away = teams_info.find("div", class_="duelParticipant__away").find("a",
                                                                            class_='participant__participantName').text.lstrip().rstrip()

    return team_home,team_away

def GetTournamentAndRound(soup):
    tourn1 = soup.find("div", class_="tournamentHeader").find("span", class_='tournamentHeader__country').find(
        "a").text.rstrip().lstrip()
    tournament = tourn1.split("-")[0].rstrip().lstrip()
    round = tourn1.split("-")[1].replace("Round", "").rstrip().lstrip()
    return tournament,round

def GetOdds(soup):
    odds_info = soup.find("div", class_="odds")
    odds = odds_info.find_all("span", class_="oddsValueInner")

    for i in range(len(odds)):
        odds[i] = odds[i].text.lstrip().rstrip()

    return odds

def AddMatchFlashscore(dataset,link,driver):
    driver.get(link+"/#/match-summary/match-statistics/0")
    driver.execute_script("window.scrollBy(0, 700);")
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    postmatch_stats=GetMatchStats(soup)
    day,month,year=GetDate(soup)
    score_home,score_away=GetScore(soup)
    team_home,team_away = GetTeamNames(soup)
    tournament,round=GetTournamentAndRound(soup)
    odds=GetOdds(soup)


    a = {}
    for stat in postmatch_stats:
        a[stat[2] + "_team1_postmatch"] = [stat[0]]
        a[stat[2] + "_team2_postmatch"] = [stat[1]]
    a["Tournament_prematch"] = [tournament]
    a["Round_prematch"] = [round]
    a["Day_prematch"] = [day]
    a["Month_prematch"] = [month]
    a["Year_prematch"] = [year]
    a["Score_Team1_postmatch"] = [score_home]
    a["Score_Team2_postmatch"] = [score_away]
    a["Team1_prematch"] = [team_home]
    a["Team2_prematch"] = [team_away]
    a["House_prematch"] = ["h"]
    a["OddTeam1_prematch"] = [odds[0]]
    a["OddTeam2_prematch"] = [odds[2]]
    a["OddDraw_prematch"] = [odds[1]]
    if(score_home>score_away):
        a["Result_postmatch"]=[2]
    elif (score_home == score_away):
        a["Result_postmatch"] = [1]
    else:
        a["Result_postmatch"] = [0]
    df = pd.DataFrame(a)

    a = {}
    for stat in postmatch_stats:
        a[stat[2] + "_team2_postmatch"] = [stat[0]]
        a[stat[2] + "_team1_postmatch"] = [stat[1]]
    a["Tournament_prematch"] = [tournament]
    a["Round_prematch"] = [round]
    a["Day_prematch"] = [day]
    a["Month_prematch"] = [month]
    a["Year_prematch"] = [year]
    a["Score_Team1_postmatch"] = [score_away]
    a["Score_Team2_postmatch"] = [score_home]
    a["Team1_prematch"] = [team_away]
    a["Team2_prematch"] = [team_home]
    a["House_prematch"] = ["a"]
    a["OddTeam1_prematch"] = [odds[2]]
    a["OddTeam2_prematch"] = [odds[0]]
    a["OddDraw_prematch"] = [odds[1]]
    if (score_home > score_away):
        a["Result_postmatch"] = [0]
    elif (score_home == score_away):
        a["Result_postmatch"] = [1]
    else:
        a["Result_postmatch"] = [2]

    try:
        zzzxsdsdgsg=int(round)
    except:
        print("Non-League MATCH")
        return dataset
    dataset = pd.concat([dataset, df, pd.DataFrame(a)], ignore_index=True)
   
    return dataset
