import streamlit as st
from PIL import Image
from riotwatcher import LolWatcher, ApiError
from io import BytesIO
import pandas as pd
import numpy as np
import requests
import json
import base64
import plotly.express as px

BASE_URL = 'https://d1fodqbtqsx6d3.cloudfront.net'
ICON_URL = 'http://ddragon.leagueoflegends.com/cdn/10.15.1/img/profileicon/'

st.set_page_config(page_title="Nexus")

st.session_state['summoner'] = ''

with open("apikey.txt", "r") as f:
    api_key = f.readlines()[0].strip()
watcher = LolWatcher(api_key)
region = "na1"

watcher = LolWatcher(api_key)
region = "na1"

menu_bar = st.sidebar.selectbox("Menu", ("Search Summoner", "Top Challenger Players", "Check Server Status"))


def getChampionTileImg(champ_name):
    return './champions/tiles/' + champ_name + '_0.jpg'

def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img.thumbnail((60, 60))
    return img

def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, 'png') # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()

def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'

def convert_df(input_df):
     return input_df.to_html(escape=False, formatters=dict(thumbnail=image_formatter))

# Look for a player in team data, if found then gives it his team result and return
def get_player_data(teams_data, player_name):
    for team in teams_data:
        for player in team['players']:
            if player['name'] == player_name:
                player['win'] = team['winner']
                return player
    return None


# Instead of whitelisting a single player, whitelist the whole team if
# the player is in there
def get_player_team(teams_data, player_name):
    for team in teams_data:
        is_team = False
        for player in team['players']:
            player['win'] = 1 if team['winner'] else 0
            if player['name'] == player_name:
                is_team = True

        if is_team:
            return team['players']
    return None

def getChampionNameById(id):
    if id == 1:
        return "Annie"
    elif id == 2:
        return "Olaf"
    elif id == 3:
        return "Galio"
    elif id == 4:
        return "TwistedFate"
    elif id == 5:
        return "XinZhao"
    elif id == 6:
        return "Urgot"
    elif id == 7:
        return "LeBlanc"
    elif id == 8:
        return "Vladimir"
    elif id == 9:
        return "Fiddlesticks"
    elif id == 10:
        return "Kayle"
    elif id == 11:
        return "Master Yi"
    elif id == 12:
        return "Alistar"
    elif id == 13:
        return "Ryze"
    elif id == 14:
        return "Sion"
    elif id == 15:
        return "Sivir"
    elif id == 16:
        return "Soraka"
    elif id == 17:
        return "Teemo"
    elif id == 18:
        return "Tristana"
    elif id == 19:
        return "Warwick"
    elif id == 20:
        return "Nunu"
    elif id == 21:
        return "MissFortune"
    elif id == 22:
        return "Ashe"
    elif id == 23:
        return "Tryndamere"
    elif id == 24:
        return "Jax"
    elif id == 25:
        return "Morgana"
    elif id == 26:
        return "Zilean"
    elif id == 27:
        return "Singed"
    elif id == 28:
        return "Evelynn"
    elif id == 29:
        return "Twitch"
    elif id == 30:
        return "Karthus"
    elif id == 31:
        return "Cho'Gath"
    elif id == 32:
        return "Amumu"
    elif id == 33:
        return "Rammus"
    elif id == 34:
        return "Anivia"
    elif id == 35:
        return "Shaco"
    elif id == 36:
        return "Dr.Mundo"
    elif id == 37:
        return "Sona"
    elif id == 38:
        return "Kassadin"
    elif id == 39:
        return "Irelia"
    elif id == 40:
        return "Janna"
    elif id == 41:
        return "Gangplank"
    elif id == 42:
        return "Corki"
    elif id == 43:
        return "Karma"
    elif id == 44:
        return "Taric"
    elif id == 45:
        return "Veigar"
    elif id == 48:
        return "Trundle"
    elif id == 50:
        return "Swain"
    elif id == 51:
        return "Caitlyn"
    elif id == 53:
        return "Blitzcrank"
    elif id == 54:
        return "Malphite"
    elif id == 55:
        return "Katarina"
    elif id == 56:
        return "Nocturne"
    elif id == 57:
        return "Maokai"
    elif id == 58:
        return "Renekton"
    elif id == 59:
        return "JarvanIV"
    elif id == 60:
        return "Elise"
    elif id == 61:
        return "Orianna"
    elif id == 62:
        return "Wukong"
    elif id == 63:
        return "Brand"
    elif id == 64:
        return "LeeSin"
    elif id == 67:
        return "Vayne"
    elif id == 68:
        return "Rumble"
    elif id == 69:
        return "Cassiopeia"
    elif id == 72:
        return "Skarner"
    elif id == 74:
        return "Heimerdinger"
    elif id == 75:
        return "Nasus"
    elif id == 76:
        return "Nidalee"
    elif id == 77:
        return "Udyr"
    elif id == 78:
        return "Poppy"
    elif id == 79:
        return "Gragas"
    elif id == 80:
        return "Pantheon"
    elif id == 81:
        return "Ezreal"
    elif id == 82:
        return "Mordekaiser"
    elif id == 83:
        return "Yorick"
    elif id == 84:
        return "Akali"
    elif id == 85:
        return "Kennen"
    elif id == 86:
        return "Garen"
    elif id == 89:
        return "Leona"
    elif id == 90:
        return "Malzahar"
    elif id == 91:
        return "Talon"
    elif id == 92:
        return "Riven"
    elif id == 96:
        return "Kog'Maw"
    elif id == 98:
        return "Shen"
    elif id == 99:
        return "Lux"
    elif id == 101:
        return "Xerath"
    elif id == 102:
        return "Shyvana"
    elif id == 103:
        return "Ahri"
    elif id == 104:
        return "Graves"
    elif id == 105:
        return "Fizz"
    elif id == 106:
        return "Volibear"
    elif id == 107:
        return "Rengar"
    elif id == 110:
        return "Varus"
    elif id == 111:
        return "Nautilus"
    elif id == 112:
        return "Viktor"
    elif id == 113:
        return "Sejuani"
    elif id == 114:
        return "Fiora"
    elif id == 115:
        return "Ziggs"
    elif id == 117:
        return "Lulu"
    elif id == 119:
        return "Draven"
    elif id == 120:
        return "Hecarim"
    elif id == 121:
        return "Kha'Zix"
    elif id == 122:
        return "Darius"
    elif id == 126:
        return "Jayce"
    elif id == 127:
        return "Lissandra"
    elif id == 131:
        return "Diana"
    elif id == 133:
        return "Quinn"
    elif id == 134:
        return "Syndra"
    elif id == 136:
        return "AurelionSol"
    elif id == 141:
        return "Kayn"
    elif id == 142:
        return "Zoe"
    elif id == 143:
        return "Zyra"
    elif id == 145:
        return "Kai'sa"
    elif id == 150:
        return "Gnar"
    elif id == 154:
        return "Zac"
    elif id == 157:
        return "Yasuo"
    elif id == 161:
        return "Vel'Koz"
    elif id == 163:
        return "Taliyah"
    elif id == 164:
        return "Camille"
    elif id == 201:
        return "Braum"
    elif id == 202:
        return "Jhin"
    elif id == 203:
        return "Kindred"
    elif id == 222:
        return "Jinx"
    elif id == 223:
        return "TahmKench"
    elif id == 235:
        return "Senna"
    elif id == 236:
        return "Lucian"
    elif id == 238:
        return "Zed"
    elif id == 240:
        return "Kled"
    elif id == 245:
        return "Ekko"
    elif id == 246:
        return "Qiyana"
    elif id == 254:
        return "Vi"
    elif id == 266:
        return "Aatrox"
    elif id == 267:
        return "Nami"
    elif id == 268:
        return "Azir"
    elif id == 350:
        return "Yuumi"
    elif id == 412:
        return "Thresh"
    elif id == 420:
        return "Illaoi"
    elif id == 421:
        return "Rek'Sai"
    elif id == 427:
        return "Ivern"
    elif id == 429:
        return "Kalista"
    elif id == 432:
        return "Bard"
    elif id == 497:
        return "Rakan"
    elif id == 498:
        return "Xayah"
    elif id == 516:
        return "Ornn"
    elif id == 517:
        return "Sylas"
    elif id == 518:
        return "Neeko"
    elif id == 523:
        return "Aphelios"
    elif id == 555:
        return "Pyke"
    elif id == 875:
        return "Sett"
    elif id == 876:
        return "Lillia"
    else:
        return None


if menu_bar == "Search Summoner":
    st.title('Summoner Search')

    col_one, col_two = st.columns(2)

    with col_one:
        summoner_name = st.text_input("Enter your summoner name")
    with col_two:
        searchBtnResult = st.button("Search")

    if len(summoner_name) > 0 and searchBtnResult:
        try:
            summoner = watcher.summoner.by_name(region, summoner_name)

            st.session_state.summoner = summoner_name
            json_str = json.dumps(summoner)
            # st.write(summoner)
            # load the json to a string
            resp = json.loads(json_str)
            st.write(resp['name'])
            puuid = resp['puuid']
            summoner_icon = (ICON_URL + str(resp['profileIconId']) + ".png")
            st.image(summoner_icon, caption='Summoner Icon')
            st.write("Summoner Level: " + str(resp["summonerLevel"]))

            # Ranked Stats
            st.header("Ranked Stats")
            ranked_stats = watcher.league.by_summoner(region, summoner['id'])

            for i in range(0, len(ranked_stats)):
                queue_type_header = ranked_stats[i]["queueType"]
                if queue_type_header == "RANKED_SOLO_5x5":
                    queue_type_header = "Ranked Solo 5v5"
                st.subheader("Queue Type: " + queue_type_header)
                st.write("Tier: " + str(ranked_stats[i]["tier"]).lower().capitalize() + " " + ranked_stats[i]["rank"])
                st.write("LP: " + str(ranked_stats[i]["leaguePoints"]))
                st.write("Wins: " + str(ranked_stats[i]["wins"]) +
                         " | Loss:" + str(ranked_stats[i]["losses"]) +
                         " W/R Ratio: " + str(
                    int((ranked_stats[i]["wins"] / (ranked_stats[i]["wins"] + ranked_stats[i]["losses"])) * 100)))
                # st.write(ranked_stats)

                matches = watcher.match.matchlist_by_puuid(region, puuid)

                # st.write(matches)
                # Example 0: "NA1_4603968039"
                # fetch last match detail
                last_match = matches[0]
                match_detail = watcher.match.by_id(region, last_match)

                participants = []
                for row in match_detail['info']['participants']:
                    participants_row = {}
                    participants_row['thumbnail'] = getChampionTileImg(getChampionNameById(row['championId']))
                    participants_row['champion'] = getChampionNameById(row['championId'])
                    participants_row['spell1'] = row['spell1Casts']
                    participants_row['spell2'] = row['spell2Casts']
                    participants_row['win'] = row['win']
                    participants_row['kills'] = row['kills']
                    participants_row['deaths'] = row['deaths']
                    participants_row['assists'] = row['assists']
                    participants_row['totalDamageDealt'] = row['totalDamageDealt']
                    participants_row['goldEarned'] = row['goldEarned']
                    participants_row['champLevel'] = row['champLevel']
                    participants_row['totalMinionsKilled'] = row['totalMinionsKilled']
                    participants_row['item0'] = row['item0']
                    participants_row['item1'] = row['item1']
                    participants.append(participants_row)
                df = pd.DataFrame(participants)
                html = convert_df(df)

                st.markdown(
                    html,
                    unsafe_allow_html=True
                )

                damage_data = df[['totalDamageDealt']]
                st.write(damage_data)
                champion_index = df[['champion']]
                st.write(champion_index)
                chart_df = pd.DataFrame(data=damage_data, index=champion_index)
                st.write(chart_df)
                st.bar_chart(chart_df)
        except ApiError as err:
            if err.response.status_code == 429:
                st.error('We should retry in {} seconds.'.format(err.response.headers['Retry-After'] +
                                                                 "this retry-after is handled by default by the "
                                                                 "RiotWatcher library future requests wait until the " +
                                                                 "retry-after time passes'"))

            elif err.response.status_code == 404:
                st.error('Invalid Summoner Name.')
elif menu_bar == "Top Challenger Players":
    st.title('Challenger Queue Analysis')
    url = BASE_URL + '/leaderboards.json'
    r = requests.get(url, verify=False)
    leaderboard = r.json()

    leaderboard_df = pd.DataFrame(leaderboard['leaderboards'][0]['lineup'])
    st.write(leaderboard_df)

    player_name = '100 Abbedagge'


    # Look for a player in team data, if found then gives it his team result and return
    def get_player_data(teams_data, player_name):
        for team in teams_data:
            for player in team['players']:
                if player['name'] == player_name:
                    player['win'] = team['winner']
                    return player
        return None


    url = BASE_URL + '/matches.json'
    r = requests.get(url, verify=False)
    matches = r.json()

    matches_df = pd.DataFrame(matches['matches'])

    # go look into each match if the player was present
    matches_df['player_data'] = matches_df['teams'].apply(lambda match_teams: get_player_data(match_teams, player_name))
    player_matches = matches_df[matches_df['player_data'].notnull()]

    # extract the player data from his matches
    player_matches = pd.DataFrame(player_matches['player_data'].tolist())
    st.write("Match history for " + player_name)
    st.write(player_matches)

    # Group the match history by champion to see which ones were played the most
    # Check plotly doc here: https://plotly.com/python/pie-charts/
    fig = px.pie(player_matches, names='championIcon', title="Champions played")
    fig.update_traces(textinfo='value')
    # Once again streamlit has a way to display what we want
    st.plotly_chart(fig)

    #Most played with
    url = BASE_URL + '/matches.json'
    r = requests.get(url, verify=False)
    matches = r.json()

    matches_df = pd.DataFrame(matches['matches'])

    # go look into each match if the player was present
    matches_df['player_data'] = matches_df['teams'].apply(lambda match_teams: get_player_data(match_teams, player_name))
    player_matches = matches_df[matches_df['player_data'].notnull()]

    # gather all of the other players that were in the same team
    player_matches['teammates'] = player_matches['teams'].apply(
        lambda team: get_player_team(team, player_name))

    # reorganize the teammates to have a list of their names
    teammates_list = [element for sublist in player_matches['teammates'].tolist()
                      for element in sublist]
    teammates = pd.DataFrame(teammates_list)
    teammates = teammates[teammates['name'] != player_name]
    teammates['team'] = teammates['name'].apply(
        lambda player_name: player_name.split()[0])

    st.write("All teammates")
    st.write(teammates)

    # let's only return top 10 most played with for more readability
    most_played_with_names = teammates['name'].value_counts().head(
        10).index.tolist()
    most_played_with = teammates[teammates['name'].isin(
        most_played_with_names)]



    fig = px.pie(most_played_with, names='name', title="Played with")
    fig.update_traces(textinfo='value')
    st.plotly_chart(fig)


    fig = px.histogram(most_played_with, x="name", color="team", y="win",
                       histfunc="avg", title="Average winrate with")
    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})
    st.plotly_chart(fig)
elif menu_bar == "Check Server Status":
    st.title('Server Status')
    url = "https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key=" + api_key
    r = requests.get(url, verify=False)
    if r:
        maintenance_status = "No maintenances currently" if not r.json().get("maintenances") else r.json().get(
            "maintenances")
        incidents_status = "there are no incidents currently" if not r.json().get("incidents") else r.json().get(
            "incidents")

        if maintenance_status != "No maintenances currently":
            st.warning("Region: " + r.json().get("name") + " " + maintenance_status + " " + incidents_status)
        elif incidents_status != "there are no incidents currently":
            st.error("Region: " + r.json().get("name") + " " + maintenance_status + " " + incidents_status)
        else:
            st.success("Region: " + r.json().get("name") + " " + maintenance_status + " " + incidents_status)
