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

"""for i in range(len(mons) - 1):
    team1 = [mons[i]]
    for j in range(1, len(mons)):
        team2 = [mons[j]]
        print(team1[0], team2[0])
        sim.battle(team1, team2)"""
team1 = [mons[0]]
team2 = [mons[1]]
sim.battle(team1, team2)