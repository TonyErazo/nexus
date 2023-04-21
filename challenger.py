import requests
import pandas as pd
import plotly.express as px
import streamlit as st

BASE_URL = 'https://d1fodqbtqsx6d3.cloudfront.net'

def get_player_team(team, player_name):
    return [player['summonerName'] for player in team['players'] if player['summonerName'] != player_name]


def get_champion_name(champion_id):
    url = BASE_URL + f"/champion/{champion_id}.json"
    r = requests.get(url, verify=False)
    champion = r.json()
    return champion['name']


def get_champion_icon_url(champion_name):
    return BASE_URL + f"/champion-icons/{champion_name}.png"


def get_player_matches(player_name):
    url = BASE_URL + '/matches.json'
    r = requests.get(url, verify=False)
    matches = r.json()

    matches_df = pd.DataFrame(matches['matches'])

    # go look into each match if the player was present
    matches_df['player_data'] = matches_df['teams'].apply(lambda match_teams: get_player_data(match_teams, player_name))
    player_matches = matches_df[matches_df['player_data'].notnull()]

    # extract the player data from his matches
    player_matches = pd.DataFrame(player_matches['player_data'].tolist())
    return player_matches


def display_match_history(player_name, player_matches):
    st.write(f"Match history for {player_name}")
    st.write(player_matches)

    # Group the match history by champion to see which ones were played the most
    # Check plotly doc here: https://plotly.com/python/pie-charts/
    fig = px.pie(player_matches, names='championIcon', title="Champions played")
    fig.update_traces(textinfo='value')
    # Once again streamlit has a way to display what we want
    st.plotly_chart(fig)


# Look for a player in team data, if found then gives it his team result and return
def get_player_data(teams_data, player_name):
    for team in teams_data:
        for player in team['players']:
            if player['name'] == player_name:
                player['win'] = team['winner']
                return player
    return None


def display_leaderboard():
    url = BASE_URL + '/leaderboards.json'
    r = requests.get(url, verify=False)
    leaderboard = r.json()
    leaderboard_df = pd.DataFrame(leaderboard['leaderboards'][0]['lineup'])
    st.write(leaderboard_df)
