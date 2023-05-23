
from Pokemon import Pokemon
from damage_calc import typeChart
import math

class Player:
    def __init__(self, id, team=[Pokemon]):
        self.id = id
        self.team = team
        self.currentMon = self.team[0]
        self.hazards = []
        self.screens = []
        self.screensCountdowns = []  #screencountdowns should be popped when hitting 0
      
    # incoming is the Pokemon object, may need to change ot index
    def switch(self, incomingIdx):
        if self.currentMon.stats[0] <= 0:
            print("shouldnt try to switch to KOed Pokemon")
            return False
        incoming = self.team[incomingIdx]
        self.currentMon.volatileStatus = []
        self.applyHazards(self, incoming)
        self.currentMon = incoming
        if self.currentMon.stats[0] <= 0:
            # this is reached if a Pokemon is KOed to hazards, only return false to not apply switchin effects
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
        if 'stealthrock' in self.hazards:
            incoming.stats[0] -= math.floor(incoming.maxHp * 0.12 * math.prod(typeChart[t.lower()]["damageTaken"]['Rock']) for t in incoming.types)
        if 'spikes' in self.hazards:
            if 'Flying' not in incoming.types or incoming.ability == 'Levitate':
                damage = 0.12
                if self.hazards.count('spikes') == 2:
                    damage = 0.18
                elif self.hazards.count('spikes') == 3:
                    damage = 0.25
            incoming.stats[0] -= math.floor(incoming.maxHp * damage)
        if 'toxicspikes' in self.hazards:
            if 'Flying' not in incoming.types or incoming.ability == 'Levitate':
                if 'Poison' not in incoming.types:
                    sts = {'status': 'psn'}
                    if self.hazards.count('toxicspikes') == 2:
                        sts = {'status': 'tox'}
                    incoming.applyStatus(sts)
                else:
                    self.hazards = list(filter(lambda a: a != 'toxicspikes', self.hazards))
        
    def defog(self):
        self.hazards = []
        self.screens = []
