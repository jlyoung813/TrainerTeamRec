import math
import random

import Pokemon
from Pokemon import Pokemon
import Player
from Player import Player
import State
from State import State
import damage_calc
from damage_calc import calc
import load_data

def battle(team1, team2):
    # initialize dictionaries
    pokedex = load_data.loadPokemon()
    movedex = load_data.loadMoves()
    abilitydex = load_data.loadAbilities()

    # initialize classes
    player1 = Player(0, team1)
    player2 = Player(1, team2)
    field = State(player1, player2)
    dmg_calc = calc()

    # pick leads
    p1_idx = player1.lead(player2)
    p2_idx = player2.lead(player1)
    player1.currentMon = player1.team[p1_idx]
    player2.currentMon = player2.team[p2_idx]

    # apply abilities, not in speed order but its fine
    ability = abilitydex[player1.currentMon.ability]
    if 'onEntry' in ability.keys():
        ability['onEntry'](field, player1.currentMon, player2.currentMon)
    ability = abilitydex[player2.currentMon.ability]
    if 'onEntry' in ability.keys():
        ability['onEntry'](field, player2.currentMon, player1.currentMon)

    hp1 = 1
    hp2 = 1
    # terminate when all mons on 1 team are dead
    while hp1 > 0 and hp2 > 0:
        # calc speed order
        speed1 = math.floor(player1.currentMon.stats[5] * Pokemon.stage(player1.currentMon.statStages[4]))
        if player1.currentMon.status == 'par':
            speed1 = speed1 // 2
        speed2 = math.floor(player2.currentMon.stats[5] * Pokemon.stage(player2.currentMon.statStages[4]))
        if player2.currentMon.status == 'par':
            speed2 = speed1 // 2
        # if speed tied player 1 goes first
        if speed1 >= speed2:
            players = [player1, player2]
        else:
            players = [player2, player1]
        actions = []
        for player in players:
            actions.append(player.act())
        # check switches first
        for i in range(len(actions)):
            action = actions[i]
            if action[0] == 'switch':
                # field switch applies switch in effects appropriately
                field.switch(i, action[1])
        for i in range(len(actions)):
            action = actions[i]
            if action[0] == 'attack':
                mon1 = players[i].currentMon
                mon2 = players[1 - i].currentMon
                move = mon1.moves[action[1]]
                rand = random.randrange(0.85, 1.01, 0.01)
                damage = dmg_calc.DamageCalc(mon1, mon2, move, field, rand)

