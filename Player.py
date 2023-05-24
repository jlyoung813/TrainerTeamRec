
from Pokemon import Pokemon
from damage_calc import typeChart
import math
from load_data import loadPokemon, loadMoves, loadAbilities
pokedex = loadPokemon()
movedex = loadMoves()
abilitydex = loadAbilities()

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
            self.currentMon.volatileStatus = []
            self.currentMon.statStages = [0, 0, 0, 0, 0]
            ability = abilitydex[self.currentMon.ability]
            if 'onExit' in ability.keys():
                heal = ability['onExit']
                self.currentMon.applyHeal(heal)
        self.applyHazardsDmg(self, incoming)
        self.currentMon = incoming
        if self.currentMon.stats[0] <= 0:
            # this is reached if a Pokemon is KOed to hazards, only return false so switchin effects arent applied
            return False
        return True
    
    def applySideEffect(self, sideEffect):
        if sideEffect == 'reflect' and 'reflect' not in self.hazards:
            self.screens.append('reflect')
            self.screensCountdown.append(8 if self.currentMon.item == 'Light Clay' else 5)
            return True
        if sideEffect == 'lightscreen' and 'lightscreen' not in self.hazards:
            self.screens.append('lightscreen')
            self.screensCountdown.append(8 if self.currentMon.item == 'Light Clay' else 5)
            return True
        if sideEffect == 'auroraveil' and 'auroraveil' not in self.hazards:
            self.screens.append('auroraveil')
            self.screensCountdown.append(8 if self.currentMon.item == 'Light Clay' else 5)
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
            incoming.applyChip([(math.prod(typeChart[t.lower()]["damageTaken"]['Rock']) for t in incoming.types), 8])
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
