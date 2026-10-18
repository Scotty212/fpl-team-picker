import requests, json

# base url for all FPL API endpoints
base_url = "https://fantasy.premierleague.com/api/"

# get data from bootstrap-static endpoint
r = requests.get(base_url + "bootstrap-static/").json()

# get player data
players = r['elements']
teams = r['teams']

clubs = {}

for i in teams:
    clubs[i['id']] = i['name']

counter = 0

for game in r['events']:
    if game['finished'] or game['is_current']:
        counter += 1

positions = { 
    1:'Goalkeeper',
    2:'Defender',
    3:'Midfielder',
    4:'Attacker'
}

all_players = []

for i in players:
    price = i['now_cost'] / 10
    value = i['total_points'] / price

    if counter > 0:
        starts_frac = i['starts'] / counter
    else:
        starts_frac = 0
    
    score = float(i['form']) * starts_frac

    all_players.append({
        'price': price,
        'value': value,
        'starts_frac': starts_frac,
        'score': score,
        'name': f"{i['first_name']} {i['second_name']}",
        'points': i['total_points'],
        'goals_scored': i['goals_scored'],
        'minutes': i['minutes'],
        'position': positions[i['element_type']],
        'form': float(i['form']) ,
        'starts': i["starts"],
        'team_id': i['team'],
        'team': clubs[i['team']],
        }) 

print(all_players[1])

squad = {
    'Goalkeeper': [],
    'Defender': [],
    'Midfielder': [],
    'Attacker': [] 
}

regulars_p = [p for p in all_players if p['minutes'] >= 270]
regulars_p.sort(key=lambda p: p['score'], reverse=True)

for player in regulars_p:
    squad[player['position']].append(player)

def top_3(position):
    print(f"\nTop 3: {position} \n")
    print_players(get_top(position, 3))

def get_top(position, n):
    if position in squad:
        return squad[position][:n]
    return []

def print_players(player_list):
    for player in player_list:
        print(f"{player['name']}, Score: {player['score']:.2f}, Value: {player['value']:.2f}")

def get_player(name):
    for player in all_players:
        if player['name'] == name:
            return (f"{player['name']}, Score: {player['score']:.2f}, Value: {player['value']:.2f}, Club: {player['team']}")
    return 'Player not found'






# 1. Create an empty list, 2. For loop 


# Then Phase 4. No code yet. Write comments at the bottom of your file explaining, in plain English, how you’d pick 15 players under these rules:

# 2 GK, 5 DEF, 5 MID, 3 FWD
# £100m total
# maximum 3 from any one club

# Start by printing one raw player from the API with players[0] and look for which key tells you their club. Send me the plan when you’ve got it.