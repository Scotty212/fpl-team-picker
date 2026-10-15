import requests, json
from pprint import pprint

# base url for all FPL API endpoints
base_url = "https://fantasy.premierleague.com/api/"

# get data from bootstrap-static endpoint
r = requests.get(base_url + "bootstrap-static/").json()

# get player data
players = r['elements']
teams = r['teams']

all_players = []

for i in players:
    all_players.append({
        'name': f"{i['first_name']} {i['second_name']}",
        'price': i['now_cost'] / 10,
        'points': i['total_points'],
        'goals_scored': i['goals_scored'],
        'minutes': i['minutes'],
        'position': i['element_type'],
        'form': float(i['form']) ,
        'starts': i["starts"]
    }) 

for player in all_players:
    if player['position'] == 1:
        player['position'] = 'Goalkeeper'
    elif player['position'] == 2:
        player['position'] = 'Defender'
    elif player['position'] == 3:
        player['position'] = 'Midfielder'
    else:
        player['position'] = 'Attacker'

for player in all_players:
    player['value'] = player['points'] / player['price']

squad = {
    'Goalkeeper': [],
    'Defender': [],
    'Midfielder': [],
    'Attacker': [] 
}

counter = 0

for game in (r['events']):
    if game['finished'] or game['is_current']:
        counter += 1


for player in all_players:
    if counter > 0:
        player['starts_frac'] = player['starts'] / counter
    else:
        player['starts_frac'] = 0

for player in all_players:
    player['score'] = player['form'] * player['starts_frac']

regulars_p = [p for p in all_players if p['minutes'] >= 270]
regulars_p.sort(key=lambda p: p['score'], reverse=True)

for player in regulars_p:
    squad[player['position']].append(player)

def top_3(position):
    print(f"\nTop 3: {position} \n")
    print_players(get_top(position, 3))

def get_top(position, n):
    result = []
    if position in squad:
        for player in squad[position][:n]:
            result.append(player)
    return result

def print_players(player_list):
    for player in player_list:
        print(f"{player['name']}, Score: {player['score']:.2f}, Value: {player['value']:.2f}")

def get_player(name):
    for player in all_players:
        if player['name'] == name:
            return (f"{player['name']}, Score: {player['score']:.2f}, Value: {player['value']:.2f}")
    return 'Player not found'

            
        



# print_players(get_top('Defender', 5))

# for position in squad:
#     top_3(position)exit()