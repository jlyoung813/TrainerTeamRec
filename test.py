import load_data
import Pokemon
import damage_calc
import State
import Player


pokedex = load_data.loadPokemon()
movedex = load_data.loadMoves()
abilitydex = load_data.loadAbilities()

print(movedex['steelroller'])