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
    if position in squad:
        print(f"\nTop 3: {position} \n")
        for player in squad[position][:3]:
            print(f"{player['name']}, Score: {player['score']:.2f}, Value: {player['value']:.2f}")
    else:
        print(f"Position '{position}' not found in squad.")

        


top_3('Midfielder')











    # if position == 'Defender':
    #     print("\ntop 3 defenders:\n")
    #     for player in squad['Defender'][:3]:
    #         print(f"{player['name']},{player['score']:.2f}, {player['value']:.2f}")

    # if position == 'Midfielder':
    #     print("\ntop 3 midfielders:\n")
    #     for player in squad['Midfielder'][:3]:
    #         print(f"{player['name']},{player['score']:.2f}, {player['value']:.2f}")

    # if position == 'Attacker':
    #     print("\ntop 3 attackers:\n")
    #     for player in squad['Attacker'][:3]:
    #         print(f"{player['name']},{player['score']:.2f}, {player['value']:.2f}")


        








    # print(f"{player['name']}, score {player['score']:.2f}, value {player['value']}, price {player['price']}")

# for n in all_players:
#     all_players[]
# print(est_value)










# for player in regulars_p:
#     squad[player['position']].append(player)
# print(squad['Goalkeeper'])



# print("\ntop 3 defenders:\n")
# for player in squad['defenders'][:3]:
#     print(f"{player['name']},{player['value']:.2f}")


# for player in regulars_p:
#     if player['position'] == 'Goalkeeper':
#      squad['goalkeepers'].append(player)

# for player in regulars_p:
#     if player['position'] == 'Defender':
#      squad['defenders'].append(player)
  

# for player in regulars_p:
#     if player['position'] == 'Midfielder':
#      squad['midfielders'].append(player)

# for player in regulars_p:
# #     if player['position'] == 'Attacker':
# #      squad['attackers'].append(player)
    

# print("\ntop 3 goalies:\n")

# for player in squad['goalkeepers'][:3]:
#     print(f"{player['name']},{player['value']:.2f}")

# print("\ntop 3 defenders:\n")
# for player in squad['defenders'][:3]:
#     print(f"{player['name']},{player['value']:.2f}")

# print("\ntop 3 midfielders:\n")
# for player in squad['midfielders'][:3]:
#     print(f"{player['name']},{player['value']:.2f}")

# print("\ntop 3 attackers:\n")
# for player in squad['attackers'][:3]:
#     print(f"{player['name']},{player['value']:.2f}")





# for defender in defenders[:5]:
    # print(f"{defender['name']}: {defender['value']:.2f} points per £m and is a {defender['position']}")
    
    
#for player in regulars_p[:10]:
    #print(f"{player['name']}: {player['value']:.2f} points per £m and is a {player['position']}")






###for team in teams:
   ### if team['name'] == 'Liverpool':
       ### liverpool_id = team['id']

###liverpool_players = []

###for player in players:
  ###  if player['team'] == liverpool_id:
       ### liverpool_players.append(player)

###player_stats = []

###for i in liverpool_players:
   ### full_name = i['first_name'] + ' ' + i['second_name']
   ### player_stats.append(full_name)

###liv_squad = []

###for i in liverpool_players:
    ###liv_squad.append({
        ###'name': f"{i['first_name']} {i['second_name']}",
        ###'price': i['now_cost'] / 10,
        ###'points': i['total_points'],
        ###'goals_scored': i['goals_scored'],
        ###'minutes': i['minutes']
    ###})

###for player in liv_squad:
    ###player['value'] = player['points'] / player['price']

###regulars = [p for p in liv_squad if p['minutes'] >= 270]
###regulars.sort(key=lambda p: p['value'], reverse=True)





    



#for player in liv_squad:
    #print(f"{player['name']} costs £{player['price']}m, they've scored {player['goals_scored']} goals, and are worth {player['points']} points")
























#store data for first player in a variable
#david_raya = players[0]

#davids most important stats
#stats = [david_raya['first_name'], david_raya['second_name'], david_raya['team'], david_raya['total_points']]
#text = f"{stats[0]} {stats[1]} plays for team Arsenal and has scored {stats[3]} points this season."





