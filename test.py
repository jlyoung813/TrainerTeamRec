import load_data
import Pokemon
import damage_calc
import State
import Player

class field:
    def __init__(self):
        self.weather = None


_, movedex, abilitydex = load_data.loadDicts()
calc = damage_calc.calc(movedex, abilitydex)
mons = Pokemon.BuildSets()
field = State.State(None, None)
for i in range(len(mons) - 1):
    mon1 = mons[i]
    for j in range(i + 1, len(mons)):
        mon2 = mons[j]
        print(mon1)

        for move in mon1.moves:
            dmg = calc.DamageCalc(mon1, mon2, move.lower(), field, 1)
            print(f'move: {move}: {dmg}')
        print(mon2)
        for move in mon2.moves:
            dmg = calc.DamageCalc(mon2, mon1, move.lower(), field, 1)
            print(f'move: {move}: {dmg}')
        print()