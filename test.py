import load_data
import Pokemon
import damage_calc
import State
import Player
import sim

pokedex = load_data.loadPokemon()
movedex = load_data.loadMoves()
abilitydex = load_data.loadAbilities()

mons = Pokemon.BuildSets()

for i in range(len(mons) - 3):
    for j in range(i + 2, len(mons) -1):
        team1 = [mons[i].copy(), mons[i + 1].copy()]
        team2 = [mons[j].copy(), mons[j + 1].copy()]
        """print(team1[0], team1[1])
        print(team2[0], team2[1])"""
        sim.battle(team1, team2)
        """print()"""