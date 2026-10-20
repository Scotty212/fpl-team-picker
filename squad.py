from data import positions 

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
    
    def show(self):
        for pos in positions.values():
            print(pos)
            for i in self.picks:
                if i['position'] == pos:
                    print(f"   {i['name']}, price: {i['price']:.1f}m, club: {i['team']}")
        print(f"\n Remaining budget: £{self.budget:.1f}m")

