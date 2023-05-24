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
        if player1.currentMon is None:
            switch_idx = -1
            if player2.currentMon is None:
                for i in range(len(player1.team)):
                    mon = player1.team[i]
                    if switch_idx == -1 and mon.stats[0] > 0:
                        switch_idx = i
            else:
                switch_idx = player1.evaluate_switches(field, player2.currentMon)[1]
            field.switch(player1.id, switch_idx)
        if player2.currentMon is None:
            switch_idx = player2.evaluate_switches(field, player1.currentMon)
            field.switch(player2.id, switch_idx[1])
        # calc speed order
        if player1.currentMon is not None and player2.currentMon is not None:
            speed1 = math.floor(player1.currentMon.stats[5] * Pokemon.stage(player1.currentMon.statStages[4]))
            if player1.currentMon.item == 'Choice Scarf':
                speed1 *= 1.5
            if player1.currentMon.status == 'par':
                speed1 = speed1 // 2
            speed2 = math.floor(player2.currentMon.stats[5] * Pokemon.stage(player2.currentMon.statStages[4]))
            if player2.currentMon.item == 'Choice Scarf':
                speed2 *= 1.5
            if player2.currentMon.status == 'par':
                speed2 = speed1 // 2
            # if speed tied player 1 goes first
            if speed1 >= speed2:
                players = [player1, player2]
            else:
                players = [player2, player1]
            actions = []
            for p in range(len(players)):
                player = players[p]
                act1, act2 = player.act(field, players[1-p].currentMon)
                action = [act1, act2]
                actions.append(action)
            # check switches first
            for i in range(len(actions)):
                action = actions[i]
                if action[0] == 'switch':
                    # field switch applies switch in effects appropriately
                    field.switch(players[i].id, action[1])
                    print(f'{players[i].currentMon}, turn: {turns}, slot: {action[1]}')
            for prio in range(6, -6, -1):
                for i in range(len(actions)):
                    action = actions[i]
                    if action[0] == 'attack':
                        mon1 = players[i].currentMon
                        mon2 = players[1 - i].currentMon
                        if mon1 is not None and 'flinch' not in mon1.volatileStatus:
                            move = mon1.moves[action[1]].lower()
                            move_data = movedex[move]
                            chance = 101
                            if mon1.status == 'par':
                                chance = 50
                            if mon1.status == 'slp' or mon1.status == 'frz':
                                chance = -1
                            full_para = random.randrange(0, 100, 1)
                            if prio == move_data['priority'] and full_para < chance:
                                if mon1.item in ['Choice Band', 'Choice Specs', 'Choice Scarf']:
                                    mon1.applyStatus({'volatileStatus': 'encore'}, False)
                                    mon1.encoreTurns = -1
                                    mon1.encoredMove = action[1]
                                if move == 'defog':
                                    field.defog()
                                if move == 'haze':
                                    field.haze()
                                if move == 'auroraveil' and field.weather == 'hail':
                                    players[i].applySideEffect('auroraveil')
                                elif 'sideCondition' in move_data.keys():
                                    if move_data['target'] == 'foeSide':
                                        players[i].applySideEffect(move_data['sideCondition'])
                                    else:
                                        players[1 - action[3]].applySideEffect(move_data['sideCondition'])
                                if move_data['target'] == 'self':
                                    mon1.applyEffect(move_data, player1.isMisty)
                                elif mon2 is not None:
                                    if move == 'trick':
                                        item = mon1.item
                                        mon1.item = mon2.item
                                        mon2.item = mon1.item
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
                                            effect = None
                                            if 'status' in move_data.keys():
                                                mon2.applyStatus(move_data, player1.isMisty)
                                            if 'secondary' in move_data.keys():
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
                                                mon1.stats[0] = min(mon1.stats[0], mon1.maxHp)
                                            if 'recoil' in move_data.keys():
                                                mon1.stats[0] -= math.floor(
                                                    damage * move_data['recoil'][0] / move_data['recoil'][1])
                                            if 'contact' in move_data['flags'].keys() and 'onRecieveHit' in abilitydex[mon2.ability].keys():
                                                mon1.applyEffect(abilitydex[mon2.ability]['onRecieveHit'])
                                            if move == 'knockoff' and damage > 0:
                                                mon2.item = None
                                            print(f'{mon1.name}, {move} : {damage}, {mon2.stats[0]}, turn: {turns}, {players[i].id}')
                                            if mon2.stats[0] <= 0:
                                                players[1 - i].currentMon = None
                                                mon2 = None
                                            if mon1.stats[0] <= 0:
                                                players[i].currentMon = None
                                                mon1 = None
                                        else:
                                            print(f'{mon1.name}, {move} : missed, turn: {turns}, {players[i].id}')
                                        j += 1
                                    if mon2 is not None and 'onActivate' in abilitydex[mon2.ability].keys():
                                        abilitydex[mon2.ability]['onActivate'](move_data, mon2)
            field.end_of_turn()
        hp1 = 0
        for mon in player1.team:
            hp1 += max(mon.stats[0], 0)
        hp2 = 0
        for mon in player2.team:
            hp2 += max(mon.stats[0], 0)
        turns += 1

