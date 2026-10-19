import requests

# base url for all FPL API endpoints
base_url = "https://fantasy.premierleague.com/api/"

# get data from bootstrap-static endpoint
try:
    r = requests.get(base_url + "bootstrap-static/").json()
except Exception:
    print("Couldn't get data from API")
    raise SystemExit

# get player data
players = r['elements']
teams = r['teams']

clubs = {}

for i in teams:
    clubs[i['id']] = i['name']

games = 0

for game in r['events']:
    if game['finished'] or game['is_current']:
        games += 1

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

    if games > 0:
        starts_frac = i['starts'] / games
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

squad = {
    'Goalkeeper': [],
    'Defender': [],
    'Midfielder': [],
    'Attacker': [] 
}

regulars_p = [p for p in all_players if p['starts_frac'] >= 0.5]
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

def print_squad(player_list):
    for pos in positions.values():       
        print(pos)
        for i in player_list:
            if i['position'] == pos:
                print(f"  {i['name']}, club: {i['team']}, price: £{i['price']:.1f}m")

    money = 100
    for i in player_list:
        money -= i['price']
    print(f" Remaining budget: £{money:.1f}m")

class Squad:
    def __init__(self):
        self.picks = []

        self.slots = {
            'Goalkeeper': 2,
            'Defender': 5,
            'Midfielder': 5,
            'Attacker': 3}

        self.budget = 100
        self.club_count = {}

    def can_add(self, player):
        if self.slots[player['position']] == 0:
            return False
        if self.budget < player['price']:
            return False
        if self.club_count.get(player['team_id'], 0) >= 3:
            return False
        else:
            return True
        
    def add(self, player):  
        self.picks.append(player)
        self.slots[player['position']] -= 1
        self.budget -= player['price']
        self.club_count[player['team_id']] = self.club_count.get(player['team_id'], 0) + 1

my_squad = Squad()

for player in regulars_p:
    if my_squad.can_add(player):
        my_squad.add(player)

