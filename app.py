from data import regulars_p
from squad import Squad

my_squad = Squad()

for player in regulars_p:
    if my_squad.can_add(player):
        my_squad.add(player)

my_squad.show()