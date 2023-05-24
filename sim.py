import math
import random

import Pokemon
#from Pokemon import Pokemon
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
    turns = 0
    # terminate when all mons on 1 team are dead
    while hp1 > 0 and hp2 > 0 and turns < 1000:
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
            act1, act2 = player.act()
            action = []
            action.append(act1)
            action.append(act2)
            actions.append(action)
        # check switches first
        for i in range(len(actions)):
            action = actions[i]
            if action[0] == 'switch':
                # field switch applies switch in effects appropriately
                field.switch(i, action[1])
        for prio in range(6, -6, -1):
            for i in range(len(actions)):
                action = actions[i]
                if action[0] == 'attack':
                    mon1 = players[i].currentMon
                    mon2 = players[1 - i].currentMon
                    if mon1 is not None:
                        move = mon1.moves[action[1]].lower()
                        move_data = movedex[move]
                        if mon1.item in ['Choice Band', 'Choice Specs', 'Choice Scarf']:
                            mon1.applyStatus({'volatileStatus': 'encore'}, False)
                            mon1.encoreTurns = -1
                            mon1.encoredMove = action[1]
                        if prio == move_data['priority']:
                            if move == 'auroraveil' and field.weather == 'hail':
                                players[i].applySideEffect('auroraveil')
                            elif 'sideCondition' in move_data.keys():
                                players[1 - i].applySideEffect(move_data['sideCondition'])
                            mon1.applyEffect(move_data, player1.isMisty)
                            if mon2 is not None:
                                hits = 1
                                if 'multihit' in move_data.keys():
                                    hits = move_data['multihit']
                                j = 0
                                # multi-hit until one mon dies, attack misses or end of hits
                                while j < hits and mon1 is not None and mon2 is not None:
                                    rand = random.randrange(85, 101, 1) / 100
                                    acc = random.randrange(0, 100, 1)
                                    accuracy = move_data['accuracy']
                                    if 'accuracyModifier' in move_data.keys():
                                        accuracy = move_data['accuracyModifier'](field, mon1, mon2)
                                    # do nothing on miss
                                    if acc < accuracy:
                                        damage = dmg_calc.DamageCalc(mon1, mon2, move, field, rand)
                                        surviveOneHit = mon2.surviveOhko()
                                        # break sash on use
                                        if surviveOneHit and damage > mon2.maxHp and mon2.item == 'Focus Sash':
                                            mon2.item = None
                                        # apply survive ohko
                                        damage = min(damage, mon2.maxHp - surviveOneHit)
                                        # break balloon on damage
                                        if damage > 0 and mon2.item == 'Air Balloon':
                                            mon2.item = None
                                        mon2.stats[0] -= damage
                                        effect = move_data['secondary']
                                        if effect is not None:
                                            # status move or hit and not sheer force
                                            if move_data['category'] == 'Status' or (damage > 0 and not mon1.ignoreSecondary):
                                                mon2.applyEffect(effect, player1.isMisty)
                                        if 'self' in move_data.keys() and damage > 0:
                                            self_effect = move_data['self']
                                            mon1.applyEffect(self_effect, player1.isMisty)
                                        if 'drain' in move_data.keys():
                                            mon1.stats[0] += math.floor(damage * move_data['drain'][0] / move_data['drain'][1])
                                        if 'recoil' in move_data.keys():
                                            mon1.stats[0] -= math.floor(
                                                damage * move_data['recoil'][0] / move_data['recoil'][1])
                                        if 'contact' in move_data['flags'].keys() and 'onRecieveHit' in abilitydex[mon2.ability].keys():
                                            mon1.applyEffect(abilitydex[mon2.ability]['onRecieveHit'])
                                        if move == 'KnockOff' and damage > 0:
                                            mon2.item = None
                                        if mon2.stats[0] <= 0:
                                            players[1 - i].currentMon = None
                                            mon2 = None
                                        if mon1.stats[0] <= 0:
                                            players[i].currentMon = None
                                            mon1 = None
                                    j += 1
                                if mon2 is not None and 'onActivate' in abilitydex[mon2.ability].keys():
                                    abilitydex[mon2.ability]['onActivate'](move_data, mon2)
        field.end_of_turn()
        hp1 = 0
        for mon in player1.team:
            hp1 += mon.stats[0]
        hp2 = 0
        for mon in player2.team:
            hp2 += mon.stats[0]
        turns += 1

