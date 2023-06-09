
from Pokemon import Pokemon
import damage_calc
from damage_calc import typeChart
import math
from load_data import loadPokemon, loadMoves, loadAbilities
pokedex = loadPokemon()
movedex = loadMoves()
abilitydex = loadAbilities()
dmg_calc = damage_calc.calc()

class Player:
    def __init__(self, id, team=[Pokemon]):
        self.id = id
        self.team = team
        self.currentMon = self.team[0]
        self.hazards = []
        self.screens = []
        self.screensCountdowns = []  #screencountdowns should be popped when hitting 0
        self.isMisty = False
      
    # incoming is the Pokemon object, may need to change ot index
    def switch(self, incomingIdx):
        if self.team[incomingIdx].stats[0] <= 0:
            print("shouldnt try to switch to KOed Pokemon")
            return False
        incoming = self.team[incomingIdx]
        if self.currentMon is not None:
            self.currentMon.clearVolatile('all')
            self.currentMon.statStages = [0, 0, 0, 0, 0]
            ability = abilitydex[self.currentMon.ability]
            if 'onExit' in ability.keys():
                heal = ability['onExit']
                self.currentMon.applyHeal(heal, self.currentMon.maxHp)
        self.applyHazardsDmg(incoming)
        self.currentMon = incoming
        if self.currentMon.stats[0] <= 0:
            # this is reached if a Pokemon is KOed to hazards, only return false so switchin effects arent applied
            return False
        return True
    
    def applySideEffect(self, sideEffect):
        if sideEffect == 'reflect' and 'reflect' not in self.screens:
            self.screens.append('reflect')
            self.screensCountdowns.append(8 if self.currentMon.item == 'Light Clay' else 5)
            return True
        if sideEffect == 'lightscreen' and 'lightscreen' not in self.screens:
            self.screens.append('lightscreen')
            self.screensCountdowns.append(8 if self.currentMon.item == 'Light Clay' else 5)
            return True
        if sideEffect == 'auroraveil' and 'auroraveil' not in self.screens:
            self.screens.append('auroraveil')
            self.screensCountdowns.append(8 if self.currentMon.item == 'Light Clay' else 5)
            return True
        if sideEffect == 'stealthrock' and 'stealthrock' not in self.hazards:
            self.hazards.append('stealthrock')
            return True
        if sideEffect == 'spikes' and self.hazards.count('spikes') <= 3:
            self.hazards.append('spikes')
            return True
        if sideEffect == 'toxicspikes' and self.hazards.count('toxicspikes') <= 2:
            self.hazards.append('spikes')
            return True
            
    def applyHazardsDmg(self, incoming):
        #apply hazards
        if incoming.item == "Heavy-Duty Boots":
            return False
        if 'stealthrock' in self.hazards:
            weak = 1
            for t in incoming.types:
                weak *= typeChart[t.lower()]['damageTaken']['Rock']
            incoming.applyChip([weak, 8])
        if 'spikes' in self.hazards:
            if incoming.grounded():
                damage = [1, 8]
                if self.hazards.count('spikes') == 2:
                    damage = [1, 6]
                elif self.hazards.count('spikes') == 3:
                    damage = [1, 4]
                incoming.applyChip(damage)
        if 'toxicspikes' in self.hazards:
            if 'Flying' not in incoming.types and incoming.ability != 'Levitate':
                if 'Poison' not in incoming.types:
                    incoming.applyStatus({'status': 'tox'} if self.hazards.count('toxicspikes') == 2 else {'status': 'psn'},  self.isMisty)
                else:
                    self.hazards = list(filter(lambda a: a != 'toxicspikes', self.hazards))
        
    def defog(self):
        self.hazards = []
        self.screens = []
        self.screensCountdowns = []

    def lead(self, other_player):
        return 0
        #pick mon to lead with based on other player team
        #need to write ai logic for this

    def act(self, field, opponent):
        max_self = 0
        max_self_idx = 0
        if self.currentMon is not None and opponent:
            moves = self.currentMon.moves
            if 'encore' in self.currentMon.volatileStatus:
                moves = [self.currentMon.moves[self.currentMon.encoredMove]]
            if 'taunt' in self.currentMon.volatileStatus:
                for move in moves:
                    move_data = movedex[move.lower()]
                    if move_data['category'] == 'Status':
                        moves.pop(move)
            for i, move in enumerate(moves):
                score = self.evaluate_move(self.currentMon, opponent, move.lower(), field)
                if score > max_self:
                    max_self = score
                    max_self_idx = i
        max_opp = 0
        if opponent is not None:
            moves = opponent.moves
            if 'encore' in opponent.volatileStatus:
                moves = [opponent.moves[opponent.encoredMove]]
            if 'taunt' in opponent.volatileStatus:
                for move in moves:
                    move_data = movedex[move.lower()]
                    if move_data['category'] == 'Status':
                        moves.pop(move)
            for i, move in enumerate(moves):
                score = self.evaluate_move(opponent, self.currentMon, move.lower(), field)
                if score > max_self:
                    max_opp = score
        max_self = max_self / max(max_opp, 1)
        max_switch, max_switch_idx = self.evaluate_switches(field, opponent)
        if max_switch > max_self:
            return 'switch', max_switch_idx
        return 'attack', max_self_idx

    def evaluate_switches(self, field, opponent):
        max_switch = -1
        max_self_idx = 0
        for i, mon in enumerate(self.team):
            if mon.stats[0] > 0 and (self.currentMon is None or mon.name != self.currentMon.name):
                moves = mon.moves
                max_self = 0
                for move in moves:
                    score = self.evaluate_move(mon, opponent, move.lower(), field)
                    if score > max_self:
                        max_self = score
                max_opp = 0
                if opponent is not None:
                    moves = opponent.moves
                    if 'encore' in opponent.volatileStatus:
                        moves = [opponent.moves[opponent.encoredMove]]
                    if 'taunt' in opponent.volatileStatus:
                        for move in moves:
                            move_data = movedex[move.lower()]
                            if move_data['category'] == 'Status':
                                moves.pop(move)
                    for move in moves:
                        score = self.evaluate_move(opponent, mon, move.lower(), field)
                        if score > max_self:
                            max_opp = score
                max_self = max_self / max(max_opp, 1)
                if max_self > max_switch:
                    max_switch = max_self
                    max_self_idx = i
        return max_switch, max_self_idx


    def evaluate_move(self, mon, opponent, move, field):
        damage = 0
        if opponent is not None:
            damage = dmg_calc.DamageCalc(mon, opponent, move, field, 0.92)
        else:
            return 1
        if damage == 0:
            move_data = movedex[move]
            accuracy = move_data['accuracy'] / 100
            if move == "stealthrock":
                return 49 * "stealthrock" not in field.players[1 - self.id].hazards
            if move == 'spikes':
                return 16 * (3 - field.players[1 - self.id].hazards.count('spikes'))
            if move == 'toxicspikes':
                return 23 * (2 - field.players[1 - self.id].hazards.count('toxicspikes'))
            if move == 'auroraveil':
                return 49 * "auroraveil" not in self.screens
            if move == 'taunt':
                count_status = 0
                for m in opponent.moves:
                    count_status += movedex[m.lower()]['category'] == 'Status'
                return 20 * count_status * 'taunt' not in opponent.volatileStatus
            if move == 'trick':
                count_status = 0
                for m in opponent.moves:
                    count_status += movedex[m.lower()]['category'] == 'Status'
                return 20 * count_status * (mon.item is not None and 'Choice' in mon.item)
            if move == 'defog':
                return 25 * self.hazards.count('stealthrock') + 8 * self.hazards.count('spikes') + 12.5 * self.hazards.count('toxicspikes')
            if move == 'haze':
                sum = 0
                for i in range(len(opponent.statStages)):
                    sum += opponent.statStages[i]
                for i in range(len(mon.statStages)):
                    sum -= mon.statStages[i]
                return min(sum * 25, 99)
            if 'status' in move_data.keys():
                if opponent.status is not None:
                    return 0
                if move_data['status'] == 'tox':
                    return 49 * (not ('Poison' in opponent.types or 'Steel' in opponent.types)) * accuracy
                if move_data['status'] == 'par':
                    return 49 * (not ('Electric' in opponent.types or 'Ground' in opponent.types)) * accuracy
                if move_data['status'] == 'brn':
                    count_phys = 0
                    for m in opponent.moves:
                        count_phys += movedex[m.lower()]['category'] == 'Physical'
                    return (12 * count_phys * 'Fire' not in opponent.types) * accuracy
                if move_data['status'] == 'slp':
                    return 51 * (not (self.isMisty or field.terrain == 'electricterrain')) * accuracy
            if 'heal' in move_data.keys():
                return min(move_data['heal'][0] / move_data['heal'][1], (1 - mon.stats[0] / mon.maxHp)) * 100
            if 'boost' in move_data.keys():
                sum = 0
                for stat in move_data['boost'].keys():
                    loc = stats = ["atk", "def", "spa", "spd", "spe"].index(stat)
                    stage = mon.statStages[loc]
                    if move_data['boost'][stat] < 0:
                        sum += move_data['boost'][stat]
                    elif stage < 2:
                        sum += move_data['boost'][stat]
                return min(sum * 25.5, 99)
            return 0
        return (1 / max(1, math.ceil(opponent.stats[0] / damage))) * 100
