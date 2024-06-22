import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import json

def GetPrematchInfo(driver,match,secs):



    driver.get("https://www.whoscored.com/Matches/" + match + "/Preview")
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    zzz=soup.find("div").text.lstrip().rstrip()
    if(zzz=="The page you requested does not exist in WhoScored.com"):
        print("БЕЗ ВКЛАДКИ ПРЕВЬЮ")
        return None,None,None,None,None,None,None,None,None,None

    season = soup.find("div", class_="main-content-column").find("div", id="content-header")
    season = season.find("a").text.split("-")
    tournament = season[0].rstrip().lstrip()
    season=season[1].split("/")[0].rstrip().lstrip()
    schemes_info = soup.find("div", class_="pitch-formation-header")
    schemes = schemes_info.find_all("span", class_="formation-label")
    teams = schemes_info.find_all("a", class_="team-link")
    team1 = teams[0].text.lstrip().rstrip()
    team2 = teams[1].text.lstrip().rstrip()
    scheme1 = schemes[0].text.replace("-", "").rstrip().lstrip()
    scheme2 = schemes[1].text.replace("-", "").rstrip().lstrip()
    prediction = soup.find("div", id="preview-prediction")
    scores = prediction.find_all("span", class_="predicted-score")
    pred_score1 = scores[0].text.lstrip().rstrip()
    pred_score2 = scores[1].text.lstrip().rstrip()
    injuries=soup.find("div",id="missing-players")

    if not injuries:
        num_of_injuries_team1=0
        num_of_injuries_team2 = 0
        return num_of_injuries_team1, num_of_injuries_team2, tournament, season, team1, team2, pred_score1, pred_score2, scheme1, scheme2

    num_of_injuries_team1=injuries.find("div",class_="home").find("tbody")
    num_of_injuries_team2=injuries.find("div", class_="away").find("tbody")

    if (num_of_injuries_team1):
        num_of_injuries_team1=len(num_of_injuries_team1.find_all("tr"))
    else:
        num_of_injuries_team1=0

    if (num_of_injuries_team2):
        num_of_injuries_team2=len(num_of_injuries_team2.find_all("tr"))
    else:
        num_of_injuries_team2=0

    return num_of_injuries_team1,num_of_injuries_team2,tournament,season,team1,team2,pred_score1,pred_score2,scheme1,scheme2
def GetPostmatchStyles(driver,match,secs):
    driver.get("https://www.whoscored.com/Matches/" + match + "/MatchReport")
    time.sleep(secs)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    postmatch_strength_team1 = []
    postmatch_strength_team2 = []
    postmatch_weakness_team1 = []
    postmatch_weakness_team2 = []
    postmatch_style_team1 = []
    postmatch_style_team2 = []

    match_report = soup.find("table", class_="matchstory")
    if not match_report:
        return postmatch_strength_team1,postmatch_strength_team2,postmatch_weakness_team1,postmatch_weakness_team2,postmatch_style_team1, postmatch_style_team2
    match_report =match_report.find_all("tr")

    z = 0
    for tr in match_report:
        if (tr["class"] == ["matchstory-typeheader"]):
            z += 1
        elif z == 1 and tr["class"] == ["matchstory-row"]:
            statements = tr.find_all("td")

            try:

                stat1 = statements[0]["class"]
                stat1 = ""
            except:
                stat1 = statements[0].find("span", class_="matchstory-text").text.lstrip().rstrip()
            try:
                stat2 = statements[1]["class"]
                stat2 = ''
            except:
                stat2 = statements[1].find("span", class_="matchstory-text").text.lstrip().rstrip()

            if stat1 != "":
                postmatch_strength_team1.append(stat1)
            if stat2 != "":
                postmatch_strength_team2.append(stat2)



        elif z == 2 and tr["class"] == ["matchstory-row"]:
            statements = tr.find_all("td")

            try:

                stat1 = statements[0]["class"]
                stat1 = ""
            except:
                stat1 = statements[0].find("span", class_="matchstory-text").text.lstrip().rstrip()
            try:
                stat2 = statements[1]["class"]
                stat2 = ''
            except:
                stat2 = statements[1].find("span", class_="matchstory-text").text.lstrip().rstrip()

            if stat1 != "":
                postmatch_weakness_team1.append(stat1)
            if stat2 != "":
                postmatch_weakness_team2.append(stat2)
        elif z == 3 and tr["class"] == ["matchstory-row"]:
            statements = tr.find_all("td")

            try:

                stat1 = statements[0]["class"]
                stat1 = ""
            except:
                stat1 = statements[0].find("span", class_="matchstory-text").text.lstrip().rstrip()
            try:
                stat2 = statements[1]["class"]
                stat2 = ''
            except:
                stat2 = statements[1].find("span", class_="matchstory-text").text.lstrip().rstrip()

            if stat1 != "":
                postmatch_style_team1.append(stat1)
            if stat2 != "":
                postmatch_style_team2.append(stat2)
    return postmatch_strength_team1,postmatch_strength_team2,postmatch_weakness_team1,postmatch_weakness_team2,postmatch_style_team1, postmatch_style_team2
def GetH2HandPrematchStylesAndForecast(driver,match,secs,govno):
    driver.get("https://www.whoscored.com/Matches/" + match + "/Show")
    time.sleep(secs)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    h2h = soup.find("div", id="previous-meetings-grid")
    h2h_matches = []

    if h2h:
        h2h = h2h.find_all("div", class_='divtable-row')

        for i in range(len(h2h)):
            if i == 3:
                break
            h2h_date = h2h[i].find("div", class_='date-long').find("div").text.lstrip().rstrip()
            h2h_month = h2h_date.split("-")[1].lstrip().rstrip()
            h2h_year = h2h_date.split("-")[2].lstrip().rstrip()
            h2h_day = h2h_date.split("-")[0].lstrip().rstrip()

            team_home = h2h[i].find("div", class_="team").find("a").text.lstrip().rstrip()
            home_score = h2h[i].find("div", class_="home-score").text.lstrip().rstrip().replace("*", "")
            away_score = h2h[i].find("div", class_="away-score").text.lstrip().rstrip().replace("*", "")

            h2h_matches.append([team_home, home_score, away_score, h2h_day, h2h_month, h2h_year])

    characters = soup.find("div", id="team-characters-comparison")

    strength = characters.find("div", class_='strengths')

    prematch_strength_team1 = []
    prematch_strength_team2 = []

    home_strength = strength.find("div", class_="home-content").find_all("tr")
    away_strength = strength.find("div", class_="away-content").find_all("tr")

    for tr in home_strength:
        td = tr.find_all("td")
        if len(td) < 2:
            break

        name = td[0].find("div", class_="iconize").text.lstrip().rstrip()
        likelihood = td[1].find("span")["class"][0].replace("level", "").lstrip().rstrip()

        prematch_strength_team1.append([name, likelihood])

    for tr in away_strength:
        td = tr.find_all("td")
        if len(td) < 2:
            break

        name = td[0].find("div", class_="iconize").text.lstrip().rstrip()
        likelihood = td[1].find("span")["class"][0].replace("level", "").lstrip().rstrip()

        prematch_strength_team2.append([name, likelihood])

    weakness = characters.find("div", class_='weaknesses')

    prematch_weakness_team1 = []
    prematch_weakness_team2 = []

    home_weakness = weakness.find("div", class_="home-content").find_all("tr")
    away_weakness = weakness.find("div", class_="away-content").find_all("tr")

    for tr in home_weakness:
        td = tr.find_all("td")
        if len(td) < 2:
            break

        name = td[0].find("div", class_="iconize").text.lstrip().rstrip()
        likelihood = td[1].find("span")["class"][0].replace("level", "").lstrip().rstrip()

        prematch_weakness_team1.append([name, likelihood])

    for tr in away_weakness:
        td = tr.find_all("td")
        if len(td) < 2:
            break

        name = td[0].find("div", class_="iconize").text.lstrip().rstrip()
        likelihood = td[1].find("span")["class"][0].replace("level", "").lstrip().rstrip()

        prematch_weakness_team2.append([name, likelihood])

    style = characters.find("div", class_='style')

    prematch_style_team1 = []
    prematch_style_team2 = []

    home_style = style.find("div", class_="home-content").find_all("li", class_="iconize")
    away_style = style.find("div", class_="away-content").find_all("li", class_="iconize")

    for li in home_style:
        name = li.text.lstrip().rstrip()

        prematch_style_team1.append(name)

    for li in away_style:
        name = li.text.lstrip().rstrip()

        prematch_style_team2.append(name)



    characters = soup.find("div", id="team-characters-comparison")
    strength = characters.find("div", class_='strengths')
    team111_name = strength.find("div", class_="home-content").find("h3").text.split("'")[0].replace("+",
                                                                                                     "").lstrip().rstrip()
    team222_name = strength.find("div", class_="away-content").find("h3").text.split("'")[0].replace("+",
                                                                                                     "").lstrip().rstrip()
    prematch_forecast = []
    forecast = soup.find("div", id="match-forecast")
    if forecast:
        forecast = forecast.find_all("tr")

        if forecast:
            for tr in forecast:
                td = tr.find_all("td")
                team = td[0].find("b")
                team_name = 0
                if team:
                    team_name = team.text.lstrip().rstrip()
                    name = td[0].find("div").text.replace(team_name, '').lstrip().rstrip()
                    if team_name == team111_name:
                        team_name = 1
                    elif team_name == team222_name:
                        team_name = 2
                else:
                    name = td[0].find("div").text.lstrip().rstrip()
                likelihood = td[1].find("span")["class"][0].replace("level", "").lstrip().rstrip()

                prematch_forecast.append([name, likelihood, team_name])

    if govno:
        season = soup.find("div", class_="main-content-column").find("div", id="content-header")
        season = season.find("a").text.split("-")
        tournament = season[0].rstrip().lstrip()
        season = season[1].split("/")[0].rstrip().lstrip()


        teams=soup.find("div", class_="main-content-column").find("div", id="match-header").find("div",class_="teams-score-info").find_all("a",class_="team-link")
        team1=teams[0].text.lstrip().rstrip()
        team2=teams[2].text.lstrip().rstrip()

        return tournament,season,team1,team2,h2h_matches, prematch_strength_team1, prematch_strength_team2, prematch_weakness_team1, prematch_weakness_team2, prematch_style_team1, prematch_style_team2, prematch_forecast

    else:
        return h2h_matches,prematch_strength_team1,prematch_strength_team2,prematch_weakness_team1,prematch_weakness_team2,prematch_style_team1,prematch_style_team2,prematch_forecast
def GetPostMatchStats(driver,match,secs):
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    driver.get("https://www.whoscored.com/Matches/" + match + "/Live")
    time.sleep(secs)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    script_tags = soup.find_all('script')
    match_stats1 = []
    match_stats2 = []
    shotZones1=[]
    shotZones2 = []
    kkk=0
    for script_tag in script_tags:
        script_content = script_tag.text

        match = re.search(r'matchCentreData:\s*({.*})', script_content)

        if match:
            kkk=1
            # Извлечение значения matchCentreData
            matchCentreData_string = match.group(1)

            # Парсинг значения matchCentreData в объект JSON
            data = json.loads(matchCentreData_string)

            added_time = data["periodEndMinutes"]

            endMinute1 = added_time["1"]
            endMinute2 = added_time["2"]

            for stat in data["home"]["stats"]:
                if stat!="minutesWithStats":
                    for minute_stat in data["home"]["stats"][stat]:
                        if int(minute_stat) < 45 :
                            match_stats1.append([stat + "_" + minute_stat, data["home"]["stats"][stat][minute_stat]])
                        elif int(minute_stat)>=45 and int(minute_stat)<=endMinute1:
                            match_stats1.append([stat+"_44+"+str(int(minute_stat)-44),data["home"]["stats"][stat][minute_stat]])
                        elif int(minute_stat)<=endMinute1+45 and int(minute_stat)>endMinute1 :
                            match_stats1.append([stat + "_" + str(int(minute_stat)-endMinute1 + 44), data["home"]["stats"][stat][minute_stat]])
                        elif int(minute_stat)>endMinute1+45:
                            match_stats1.append([stat + "_89+" + str(int(minute_stat) - 89-endMinute1 + 44), data["home"]["stats"][stat][minute_stat]])

            for stat in data["away"]["stats"]:
                if stat!="minutesWithStats":
                    for minute_stat in data["away"]["stats"][stat]:
                        if int(minute_stat) < 45:
                            match_stats1.append([stat + "_" + minute_stat, data["away"]["stats"][stat][minute_stat]])
                        elif int(minute_stat) >= 45 and int(minute_stat) <= endMinute1:
                            match_stats1.append(
                                [stat + "_44+" + str(int(minute_stat) - 44), data["away"]["stats"][stat][minute_stat]])
                        elif int(minute_stat) <= endMinute1 + 45 and int(minute_stat) > endMinute1:
                            match_stats1.append([stat + "_" + str(int(minute_stat) - endMinute1 + 44),
                                                 data["away"]["stats"][stat][minute_stat]])
                        elif int(minute_stat) > endMinute1 + 45:
                            match_stats1.append([stat + "_89+" + str(int(minute_stat) - 89 - endMinute1 + 44),
                                                 data["away"]["stats"][stat][minute_stat]])

            for zone in data["home"]["shotZones"]:
                shots=0
                goals=0
                for minute_stat in data["home"]["shotZones"][zone]["stats"]:
                    shots+=data["home"]["shotZones"][zone]["stats"][minute_stat]["count"]
                    goals += data["home"]["shotZones"][zone]["stats"][minute_stat]["goalCount"]
                shotZones1.append([zone,shots,goals])

            for zone in data["away"]["shotZones"]:
                shots = 0
                goals = 0
                for minute_stat in data["away"]["shotZones"][zone]["stats"]:
                    shots += data["away"]["shotZones"][zone]["stats"][minute_stat]["count"]
                    goals += data["away"]["shotZones"][zone]["stats"][minute_stat]["goalCount"]
                shotZones2.append([zone, shots, goals])

            scores=data["score"]

            score1=scores.split(":")[0].lstrip().rstrip()
            score2=scores.split(":")[1].lstrip().rstrip()

            ht_scores = data["htScore"]

            if ht_scores:
                ht_score1 = ht_scores.split(":")[0].lstrip().rstrip()
                ht_score2 = ht_scores.split(":")[1].lstrip().rstrip()
            else:
                print("Залуууууупа, с счетом после первого тайма")
                ht_score2=None
                ht_score1=None




            date=data["startDate"].split("T")[0]

            year=int(date.split("-")[0])
            month = int(date.split("-")[1])
            day = int(date.split("-")[2])


    if kkk==0:
        print("БЕЗ СТАТЫ ПОСЛЕМАЧТЕВОЙ")
        info=soup.find("div",id="match-header").find("div",class_="icons-details-container").find_all("div",class_='info-block cleared')

        scores=info[1].find_all("dd")

        ht_scores=scores[0].text
        ht_score1=int(ht_scores.split(":")[0])
        ht_score2=int(ht_scores.split(":")[1])
        scores = scores[1].text
        score1 = int(scores.split(":")[0])
        score2 = int(scores.split(":")[1])

        date=info[2].find_all("dd")[1].text.split(",")[1]

        day=int(date.split("-")[0].rstrip().lstrip())
        month = months[date.split("-")[1].rstrip().lstrip()]
        year = int("20"+date.split("-")[2].rstrip().lstrip())
        return day,month,year, [], [], [], [], score1,score2,ht_score1,ht_score2, 0,0


    return day,month,year,match_stats1,match_stats2,shotZones1,shotZones2,score1,score2,ht_score1,ht_score2,endMinute1,endMinute2
def AddMatchWhoScored( dataset,match, driver):


    secs = 0.2
    injuries_team1,injuries_team2,tournament,season,team1,team2,pred_score1,pred_score2,scheme1,scheme2 = GetPrematchInfo(driver, match, secs)

    day, month, year, match_stats1, match_stats2, shotZones1, shotZones2, score1, score2, ht_score1, ht_score2, endMinute1, endMinute2 = GetPostMatchStats(
        driver, match, secs)

    if team1==None:


        pred_score1=score1
        pred_score2=score2
        injuries_team1=3
        injuries_team2=3
        scheme1="433"
        scheme2="433"
        tournament,season,team1,team2,h2h_matches, prematch_strength_team1, prematch_strength_team2, prematch_weakness_team1, prematch_weakness_team2, prematch_style_team1, prematch_style_team2, prematch_forecast = GetH2HandPrematchStylesAndForecast(
            driver, match, secs,govno=True)

    else:
        h2h_matches, prematch_strength_team1, prematch_strength_team2, prematch_weakness_team1, prematch_weakness_team2, prematch_style_team1, prematch_style_team2, prematch_forecast = GetH2HandPrematchStylesAndForecast(
            driver, match, secs)

    postmatch_strength_team1, postmatch_strength_team2, postmatch_weakness_team1, postmatch_weakness_team2, postmatch_style_team1, postmatch_style_team2 = GetPostmatchStyles(
        driver, match, secs)

    # Комментарии всегда надо пиать в своих проектах чтобы не забыть о ём реь буквально через три дня, а ты даун не написал ни одного комментария за весь этот проект. Ладно, может написал но я этого не видел. Мустанг оказывается нихуёвая машина, не видел её и хз откуда она у меня. Я тренирую скоропечатания,  аэта клавиатура будет попиздатей чем у меня, хз поч так. бляяяяяя. завтра пересдача где меня будут насиловать в анал. Разрушитель очка три тысячи. КИШКИ НАРУЖУ БЛЯТЬ. Сперма в рот летит как будто самолёт. Зачем мне рисковать необходимым ради получения избыточного? Выгу выгу выгу тутутутутутутуттуту. По сути я написал не сильно много текста но ты не прочитаешь потому что ты хуесос. ЛОгично. Ебать ты смешно в поворот въебался, ахахах. БЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯ, ЧТО НА ДОСКЕ НАХУЙ НАПИСАНО??? Способы задания графов, жесть. Ебать у тебя заряда мало, ну ты и лох, а я зарядился дома, хиххихих. Щас бы виски с колой... Я хз что написать кек лол арбидол






    a = {}
    a["Season_prematch"] = [season]
    a["Day_prematch"] = [day]
    a["Month_prematch"] = [month]
    a["Year_prematch"] = [year]
    a["Score_Team1_postmatch"] = [score1]
    a["Score_Team2_postmatch"] = [score2]
    a["HalfScore_Team1_postmatch"] = [ht_score1]
    a["HalfScore_Team2_postmatch"] = [ht_score2]
    a["PredScore_Team1_prematch"] = [pred_score1]
    a["PredScore_Team2_prematch"] = [pred_score2]
    a["Team1_prematch"] = [team1]
    a["Team2_prematch"] = [team2]
    a["Scheme1_prematch"] = [scheme1]
    a["Scheme2_prematch"] = [scheme2]
    a["House_prematch"] = ["h"]
    a["EndMinute1_postmatch"] = [endMinute1]
    a["EndMinute2_postmatch"] = [endMinute2]
    a["Injuries1_prematch"] = [injuries_team1]
    a["Injuries2_prematch"] = [injuries_team2]
    a["Disqualification_postmatch"]=[0]


    for strength in postmatch_strength_team1:
        a[strength + "_strength_team1_postmatch"] = [1]
    for strength in postmatch_strength_team2:
        a[strength + "_strength_team2_postmatch"] = [1]
    for strength in postmatch_weakness_team1:
        a[strength + "_weakness_team1_postmatch"] = [1]
    for strength in postmatch_weakness_team2:
        a[strength + "_weakness_team2_postmatch"] = [1]
    for strength in postmatch_style_team1:
        a[strength + "_style_team1_postmatch"] = [1]
    for strength in postmatch_style_team2:
        a[strength + "_style_team2_postmatch"] = [1]

    for stat in match_stats1:
        a[f'{stat[0]}' + '_team1_postmatch'] = [stat[1]]
    for stat in match_stats2:
        a[f'{stat[0]}' + '_team2_postmatch'] = [stat[1]]
    for stat in shotZones1:
        a[f'{stat[0]}' + '_shots_team1_postmatch'] = [stat[1]]
        a[f'{stat[0]}' + '_goals_team1_postmatch'] = [stat[2]]
    for stat in shotZones2:
        a[f'{stat[0]}' + '_shots_team2_postmatch'] = [stat[1]]
        a[f'{stat[0]}' + '_goals_team2_postmatch'] = [stat[2]]

    for bb in range(1, 4):
        a["h2h_team_order_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_team1_score_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_team2_score_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_day_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_month_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_year_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_flag_match_" + str(bb) + "_prematch"] = [0]

    bb = 1
    for match in h2h_matches:
        if match[0] == team1:
            a["h2h_team_order_match_" + str(bb) + "_prematch"] = [0]
        elif match[0] == team2:
            a["h2h_team_order_match_" + str(bb) + "_prematch"] = [1]
        else:
            a["h2h_team_order_match_" + str(bb) + "_prematch"] = [10]
        a["h2h_team1_score_match_" + str(bb) + "_prematch"] = [match[1]]
        a["h2h_team2_score_match_" + str(bb) + "_prematch"] = [match[2]]
        a["h2h_day_match_" + str(bb) + "_prematch"] = [match[3]]
        a["h2h_month_match_" + str(bb) + "_prematch"] = [match[4]]
        a["h2h_year_match_" + str(bb) + "_prematch"] = [match[5]]
        a["h2h_flag_match_" + str(bb) + "_prematch"] = [1]
        bb += 1

    for strength in prematch_strength_team1:
        a[strength[0] + "_strength_team1_prematch"] = [strength[1]]
    for strength in prematch_strength_team2:
        a[strength[0] + "_strength_team2_prematch"] = [strength[1]]
    for strength in prematch_weakness_team1:
        a[strength[0] + "_weakness_team1_prematch"] = [strength[1]]
    for strength in prematch_weakness_team2:
        a[strength[0] + "_weakness_team2_prematch"] = [strength[1]]
    for strength in prematch_style_team1:
        a[strength + "_style_team1_prematch"] = [1]
    for strength in prematch_style_team2:
        a[strength + "_style_team2_prematch"] = [1]

    for forecast in prematch_forecast:
        if forecast[2] == 0:
            a[forecast[0] + "_forecast_prematch"] = [forecast[1]]
        elif forecast[2] == 1:
            a[forecast[0] + "_forecast_team1_prematch"] = [forecast[1]]
        else:
            a[forecast[0] + "_forecast_team2_prematch"] = [forecast[1]]

    df = pd.DataFrame(a)

    a = {}
    a["Season_prematch"] = [season]
    a["Day_prematch"] = [day]
    a["Month_prematch"] = [month]
    a["Year_prematch"] = [year]
    a["Score_Team1_postmatch"] = [score2]
    a["Score_Team2_postmatch"] = [score1]
    a["HalfScore_Team2_postmatch"] = [ht_score1]
    a["HalfScore_Team1_postmatch"] = [ht_score2]
    a["PredScore_Team1_prematch"] = [pred_score2]
    a["PredScore_Team2_prematch"] = [pred_score1]
    a["Team1_prematch"] = [team2]
    a["Team2_prematch"] = [team1]
    a["Scheme1_prematch"] = [scheme2]
    a["Scheme2_prematch"] = [scheme1]
    a["House_prematch"] = ["a"]
    a["EndMinute1_postmatch"] = [endMinute1]
    a["EndMinute2_postmatch"] = [endMinute2]
    a["Injuries2_prematch"] = [injuries_team1]
    a["Injuries1_prematch"] = [injuries_team2]
    a["Disqualification_postmatch"] = [0]

    for strength in postmatch_strength_team2:
        a[strength + "_strength_team1_postmatch"] = [1]
    for strength in postmatch_strength_team1:
        a[strength + "_strength_team2_postmatch"] = [1]
    for strength in postmatch_weakness_team2:
        a[strength + "_weakness_team1_postmatch"] = [1]
    for strength in postmatch_weakness_team1:
        a[strength + "_weakness_team2_postmatch"] = [1]
    for strength in postmatch_style_team2:
        a[strength + "_style_team1_postmatch"] = [1]
    for strength in postmatch_style_team1:
        a[strength + "_style_team2_postmatch"] = [1]

    for stat in match_stats2:
        a[f'{stat[0]}' + '_team1_postmatch'] = [stat[1]]
    for stat in match_stats1:
        a[f'{stat[0]}' + '_team2_postmatch'] = [stat[1]]
    for stat in shotZones2:
        a[f'{stat[0]}' + '_shots_team1_postmatch'] = [stat[1]]
        a[f'{stat[0]}' + '_goals_team1_postmatch'] = [stat[2]]
    for stat in shotZones1:
        a[f'{stat[0]}' + '_shots_team2_postmatch'] = [stat[1]]
        a[f'{stat[0]}' + '_goals_team2_postmatch'] = [stat[2]]

    for bb in range(1, 4):
        a["h2h_team_order_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_team1_score_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_team2_score_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_day_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_month_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_year_match_" + str(bb) + "_prematch"] = [0]
        a["h2h_flag_match_" + str(bb) + "_prematch"] = [0]

    bb = 1

    for match in h2h_matches:
        if match[0] == team2:
            a["h2h_team_order_match_" + str(bb) + "_prematch"] = [0]
        elif match[0] == team1:
            a["h2h_team_order_match_" + str(bb) + "_prematch"] = [1]
        a["h2h_team2_score_match_" + str(bb) + "_prematch"] = [match[1]]
        a["h2h_team1_score_match_" + str(bb) + "_prematch"] = [match[2]]
        a["h2h_day_match_" + str(bb) + "_prematch"] = [match[3]]
        a["h2h_month_match_" + str(bb) + "_prematch"] = [match[4]]
        a["h2h_year_match_" + str(bb) + "_prematch"] = [match[5]]
        a["h2h_flag_match_" + str(bb) + "_prematch"] = [1]
        bb += 1

    for strength in prematch_strength_team2:
        a[strength[0] + "_strength_team1_prematch"] = [strength[1]]
    for strength in prematch_strength_team1:
        a[strength[0] + "_strength_team2_prematch"] = [strength[1]]
    for strength in prematch_weakness_team2:
        a[strength[0] + "_weakness_team1_prematch"] = [strength[1]]
    for strength in prematch_weakness_team1:
        a[strength[0] + "_weakness_team2_prematch"] = [strength[1]]
    for strength in prematch_style_team2:
        a[strength + "_style_team1_prematch"] = [1]
    for strength in prematch_style_team1:
        a[strength + "_style_team2_prematch"] = [1]

    for forecast in prematch_forecast:
        if forecast[2] == 0:
            a[forecast[0] + "_forecast_prematch"] = [forecast[1]]
        elif forecast[2] == 1:
            a[forecast[0] + "_forecast_team2_prematch"] = [forecast[1]]
        else:
            a[forecast[0] + "_forecast_team1_prematch"] = [forecast[1]]




    dataset = pd.concat([dataset, df, pd.DataFrame(a)], ignore_index=True)

    return dataset
