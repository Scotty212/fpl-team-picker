import requests, json

# base url for all FPL API endpoints
base_url = "https://fantasy.premierleague.com/api/"

# get data from bootstrap-static endpoint
r = requests.get(base_url + "bootstrap-static/").json()

# get player data
players = r['elements']
teams = r['teams']

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
        'starts': i["starts"]
    }) 

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



# check the position is in squad
# if it is, return the slice
# if it isn’t, return something sensible (an empty list is a good choice)






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
#     top_3(position)