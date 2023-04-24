import streamlit as st
from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import champs
import challenger
import smtplib
from email.mime.multipart import MIMEMultipart

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

menu_bar = st.sidebar.selectbox("Menu", ("Search Summoner", "Top Challenger Players", "Check Server Status", "Contact Us"))


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
                    participants_row['thumbnail'] = champs.getChampionTileImg(
                        champs.getChampionNameById(row['championId']))
                    participants_row['champion'] = champs.getChampionNameById(row['championId'])

                    if (participants_row['champion'] == 'None'):
                        st.error("Champ ID: " + str(row['championId']) + " please report this error to dev@nexus.io")

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
                html = champs.convert_df(df)

                st.markdown(
                    html,
                    unsafe_allow_html=True
                )

                damage_data = df[['totalDamageDealt']]

                champion_index = df[['champion']]
                st.write(champion_index)


                st.bar_chart(data = damage_data)

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

    challenger.display_leaderboard()
    player_name = 'C9 Destiny'
    player_games = challenger.get_player_matches(player_name)

    challenger.display_match_history(player_name, player_games)


elif menu_bar == "Check Server Status":
    st.title('Server Status')
    url = "https://na1.api.riotgames.com/lol/status/v4/platform-data?api_key=" + api_key
    r = requests.get(url, verify=False)

    maintenance_json = json.loads(r.text)

    incident_json = json.loads(r.text)['incidents'][0]['updates'][0]['translations'][0]['content']

    #incidents_status = "there are no incidents currently" if not incident_json else incident_json

    if r:
        #maintenance_status = "No maintenances currently" if not maintenance_json else maintenance_json
        #incidents_status = "there are no incidents currently" if not incident_json else incident_json

        if not 'maintenances' in maintenance_json or len(maintenance_json['maintenances']) == 0:
            maintenance_status = "No maintenances currently"
            st.success(maintenance_status)
        else:
            maintenance_json = json.loads(r.text)['maintenances'][0]['updates'][0]['translations'][0]['content']
            maintenance_status = maintenance_json
            st.error(maintenance_status)
        if not 'incidents' in incident_json or len(incident_json['incidents']) == 0:
            incidents_status = "there are no incidents currently"
            st.success(incidents_status)
        else:
            incidents_status = incident_json
            st.error(incidents_status)
        st.info("Region: " + r.json().get("name"))

        df = pd.DataFrame(
            np.random.randn(500, 2) / [500, 300] + [34.02, -118.4],
            columns=['lat', 'lon'])

        st.subheader("Map Zoom")
        zoom_val = st.slider("Zoom value", min_value = 1, max_value = 7, value = 3)
        st.map(df,zoom=zoom_val)
elif menu_bar == "Contact Us":
    st.header("Contact Form")
    contact_email = st.text_input("Enter an e-mail we can reach you at")
    age = st.number_input("Please enter your age")
    description = st.text_area("Please describe what you would like to contact us about")
    date_occurred = st.date_input("Please select the date this occurred")
    category = st.radio("Select the contact category", ("Contact", "Bug Report", "Affiliation"))
    submit_btn = st.button("Submit")

    if submit_btn:
        #msg = MIMEMultipart()
        #msg['Subject'] = str(category) + " date: " + str(date_occurred)
        #dev_email = "admin@nexus.io"
        #msg['Subject'] = 'The contents of %s' % description
        #msg['From'] = contact_email
        #msg['To'] = ",".join(dev_email)

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        #s = smtplib.SMTP('localhost')
        #s.sendmail(contact_email, [dev_email], msg.as_string())
        #s.quit()
        st.success("Email sent!")