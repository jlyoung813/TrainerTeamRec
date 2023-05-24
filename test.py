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

for i in range(len(mons) - 1):
    team1 = [mons[i]]
    for j in range(1, len(mons)):
        team2 = [mons[j]]
        sim.battle(team1, team2)