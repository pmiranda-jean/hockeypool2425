#!/usr/bin/env python
# coding: utf-8

# In[66]:


import requests
from requests.exceptions import RequestException

# Dictionaries to store player stats (skaters and goalies)
skaters_stats = {}
goalies_stats = {}

# Dictionary to store participants and their selected player IDs (skaters and goalies)
participants = {
    "Philippe": {
        "skaters": ['8476453','8477934','8478420','8480023','8478483','8474600','8477493','8480018','8477504'], 
        "goalies": ['8478048']
    },
     "George": {
        "skaters": ['8477492','8479318','8480023','8477933','8474600','8475786','8479323','8475754','8480018'],
        "goalies": ['8476945']
    },
     "Matthew": {
        "skaters": ['8478402', '8479318', '8478420','8480023','8474600','8477404','8480018','8479323','8484144'],
        "goalies": ['8479979']
    }
}

# Function to get player statistics from the API
def get_player_stats(player_id):
#this is how you get information from an API
    url = f'https://api-web.nhle.com/v1/player/{player_id}/landing'
    try: #to allow for exception in case their is an error in the code. 
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

#here is how you can access the required information in the API. 
        player_id = data.get("playerId")
        team = data.get("currentTeamAbbrev")
        first_name = data["firstName"]["default"]
        last_name = data["lastName"]["default"]
                
        featured_stats = data.get("featuredStats", {})
        regular_season = featured_stats.get("regularSeason", {})
        sub_season = regular_season.get("subSeason", {})
        goals = sub_season.get('goals', 0)
        assists = sub_season.get('assists', 0)
        wins = sub_season.get('wins', 0)
        shutouts = sub_season.get('shutouts', 0)

#for each player i want to store all of this information in a dictionary. 
        return {
            "Player ID": player_id,
            "Team": team,
            "First Name": first_name,
            "Last Name": last_name,
            "Goals": goals,
            "Assists": assists,
            "Wins": wins,
            "Shutouts": shutouts
        }
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
# Function to calculate points for skaters and goalies
def calculate_points(player_id, player_type):
    if player_type == "skater": #based on which dictionary they are being added to. 
        stats = skaters_stats.get(player_id, {}) #you use the playerID and retrieve the info with the formula. 
        goals = stats.get("Goals", 0)
        assists = stats.get("Assists", 0)
        return (goals * 2) + (assists * 1)
    
    elif player_type == "goalie":
        stats = goalies_stats.get(player_id, {})
        wins = stats.get("Wins", 0)
        shutouts = stats.get("Shutouts", 0)
        return (wins * 2) + (shutouts * 3)

# Function to gather and store player stats
def update_player_stats():
    for participant, players in participants.items():
        for skater_id in players['skaters']:
            if skater_id not in skaters_stats:
                skaters_stats[skater_id] = get_player_stats(skater_id)
                
        for goalie_id in players['goalies']:
            if goalie_id not in goalies_stats:
                goalies_stats[goalie_id] = get_player_stats(goalie_id)

# Function to calculate total points for participants
def calculate_participant_points():
    participant_points = {}
    for participant, players in participants.items():
        total_points = 0
        
        for skater_id in players['skaters']:
            total_points += calculate_points(skater_id, "skater")
        
        for goalie_id in players['goalies']:
            total_points += calculate_points(goalie_id, "goalie")
        
        participant_points[participant] = total_points
    
    return participant_points

# Function to rank participants by points
def rank_participants():
    participant_points = calculate_participant_points()
    sorted_participants = sorted(participant_points.items(), key=lambda x: x[1], reverse=True)
    
    print("Participant Rankings:\n")
    print(f"{'Rank':<5} {'Participant':<15} {'Points':<6}")
    print("-" * 30)  # Separator
    for rank, (participant, points) in enumerate(sorted_participants, start=1):
        print(f"{rank:<5} {participant:<15} {points:<6}")
        
# Function to display player stats by participants and their points
def display_participant_players():
    for participant, players in participants.items():
        print(f"\n{participant}'s Players:")
        print(f"{'Player':<30} {'G':<5} {'A':<5} {'W':<5} {'S':<5} {'Pts':<5}")
        print("-" * 80)
        
        for skater_id in players['skaters']:
            stats = skaters_stats.get(skater_id, {})
            points = calculate_points(skater_id, "skater")
            print(f"{stats.get('First Name', 'N/A') + ' ' + stats.get('Last Name', 'N/A') + ' (' + stats.get('Team','N/A') + ')':<30} "
                  f"{stats.get('Goals', 0):<5} {stats.get('Assists', 0):<5} {stats.get('Wins', 0):<5} {stats.get('Shutouts', 0):<5} {points:<5}")
        
        for goalie_id in players['goalies']:
            stats = goalies_stats.get(goalie_id, {})
            points = calculate_points(goalie_id, "goalie")
            print(f"{stats.get('First Name', 'N/A') + ' ' + stats.get('Last Name', 'N/A') + ' (' + stats.get('Team','N/A') + ')':<30} "
                  f"{stats.get('Goals', 0):<5} {stats.get('Assists', 0):<5} {stats.get('Wins', 0):<5} {stats.get('Shutouts', 0):<5} {points:<5}")

# Function to rank players by points and show who selected them
def rank_players():
    # Create a dictionary to store points for all players (skaters and goalies)
    player_points = {}

    # Add skaters and their points
    for player_id, stats in skaters_stats.items():
        player_points[player_id] = calculate_points(player_id, "skater")

    # Add goalies and their points
    for player_id, stats in goalies_stats.items():
        player_points[player_id] = calculate_points(player_id, "goalie")

    # Sort players by points in descending order
    sorted_players = sorted(player_points.items(), key=lambda x: x[1], reverse=True)
            
    # Print player rankings and who chose them
    print("\nPlayer Rankings:")
    print(f"{'Rank':<5} {'Player':<30} {'Points':<5} {'Chosen by':<30}")
    print("-" * 80)  # Adjusted separator for better table width

    for rank, (player_id, points) in enumerate(sorted_players, start=1):
        # Get the player selectors (list of participants who selected this player)
        selected_by = player_selectors.get(player_id, [])
        selectors_list = ", ".join(selected_by)  # Join list of participants

        if player_id in skaters_stats:
            stats = skaters_stats[player_id]
            print(f"{rank:<5} {stats.get('First Name', 'N/A') + ' ' + stats.get('Last Name', 'N/A')+ ' (' + stats.get('Team','N/A') + ')':<30} "
                  f"{points:<5} {selectors_list:<30}")
        else:
            stats = goalies_stats[player_id]
            print(f"{rank:<5} {stats.get('First Name', 'N/A') + ' ' + stats.get('Last Name', 'N/A')+ ' (' + stats.get('Team','N/A') + ')':<30} "
                  f"{points:<5} {selectors_list:<30}")
            
# Updating the player_selectors dictionary
player_selectors = {}

# Updating player_selectors for each participant
for participant, players in participants.items():
    for skater_id in players['skaters']:
        if skater_id not in player_selectors:
            player_selectors[skater_id] = []
        player_selectors[skater_id].append(participant)
    
    for goalie_id in players['goalies']:
        if goalie_id not in player_selectors:
            player_selectors[goalie_id] = []
        player_selectors[goalie_id].append(participant)

# Run the updates and display rankings
update_player_stats()
rank_participants()
rank_players()
display_participant_players()


# In[77]:


import requests
from datetime import datetime

# Function to populate players_dict based on participants' selections
def populate_players_dict(participants):
    players_dict = {}
    for participant, players in participants.items():
        for skater_id in players['skaters']:
            if skater_id not in players_dict:
                player_info = get_player_info(skater_id)
                if player_info:
                    players_dict[skater_id] = player_info
        
        for goalie_id in players['goalies']:
            if goalie_id not in players_dict:
                player_info = get_player_info(goalie_id)
                if player_info:
                    players_dict[goalie_id] = player_info
    
    return players_dict

# Function to get schedule by date
def get_schedule_by_date(date):
    url = f'https://api-web.nhle.com/v1/schedule/{date}'
    response = requests.get(url)
    data = response.json()
    playing_teams = []

    for game_week in data['gameWeek']:
        if game_week["date"] == date:
            for game in game_week['games']:
                away_team_abbrev = game['awayTeam']['abbrev']
                home_team_abbrev = game['homeTeam']['abbrev']
                playing_teams.append(home_team_abbrev)
                playing_teams.append(away_team_abbrev)
    
    return playing_teams

# Function to get players playing today for each participant
def get_participant_players_playing_today(participants, players_dict, playing_teams):
    players_playing_today = {}

    # Loop through each participant
    for participant, players in participants.items():
        players_playing_today[participant] = []
        
        # Check skaters
        for skater_id in players['skaters']:
            if skater_id in players_dict and players_dict[skater_id]['team_abbrev'] in playing_teams:
                players_playing_today[participant].append(players_dict[skater_id]['name'])
        
        # Check goalies
        for goalie_id in players['goalies']:
            if goalie_id in players_dict and players_dict[goalie_id]['team_abbrev'] in playing_teams:
                players_playing_today[participant].append(players_dict[goalie_id]['name'])

    return players_playing_today

# Main logic
today = datetime.now().strftime('%Y-%m-%d')
playing_teams = get_schedule_by_date(today)

# Populate players_dict dynamically
players_dict = populate_players_dict(participants)

# Get and print players playing tonight by participant
players_playing_today = get_participant_players_playing_today(participants, players_dict, playing_teams)

# Print out the result
print(playing_teams)
for participant, players in players_playing_today.items():
    print(f"{participant}'s players playing tonight:")
    if players:
        for player in players:
            print(f"- {player}")
    else:
        print("No players are playing tonight.")
    print()  # For spacing


# In[ ]:




