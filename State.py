import math
from Player import Player
from Pokemon import Pokemon
from load_data import loadPokemon, loadMoves, loadAbilities
pokedex = loadPokemon()
movedex = loadMoves()
abilitydex = loadAbilities()


class State:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.weather = None
        self.weatherCount = 0
        self.terrain = None
        self.terrainCount = 0
        self.trickRoomCount = 0
    
    def setWeather(self, weather, turns):
        if self.weather != weather:
            self.weather = weather
            self.weatherCount = turns
            # return True
            
    def setTerrain(self, terrain, turns):
        if self.terrain != terrain:
            self.terrain = terrain
            self.terrainCount = turns
            if terrain == 'mistyterrain':
                for i in self.players:
                    i.isMisty = True
            else:
                for i in self.players:
                    i.isMisty = False
            # return True
    
    def setTrickRoom(self):
        self.trickRoomCount = 0 if self.trickRoomCount > 0 else 5
    
    def defog(self):
        self.player1.defog()
        self.player2.defog()
        self.terrain = None
        self.terrainCount = 0

    def haze(self):
        self.player1.currentMon.statStages = [0, 0, 0, 0, 0]
        self.player2.currentMon.statStages = [0, 0, 0, 0, 0]
    
    def switch(self, playerIdx, incomingIdx):
        if self.players[playerIdx].switch(incomingIdx):
            abilitydex[self.players[playerIdx].currentMon.ability]['onEntry'](self, self.players[playerIdx], self.players[1-playerIdx])
        else:
            self.players[playerIdx].currentMon = None
    
    def end_of_turn(self):
    #lefties, weather, status, seeds
        self.weatherCount -= 1 if self.weatherCount > 0 else 0
        if self.weatherCount == 0:
            self.weather = None
        self.terrainCount -= 1 if self.terrainCount > 0 else 0
        if self.terrainCount == 0:
            self.terrain = None
            
        if self.weather == 'sandstorm':
            for i in self.players:
                if i.currentMon is not None:
                    if 'Ground' not in i.currentMon.types and \
                    'Rock' not in i.currentMon.types and \
                    'Steel' not in i.currentMon.types and \
                    i.currentMon.ability != 'overcoat' and \
                    i.currentMon.item != 'Safety Goggles':
                        if i.currentMon.applyChip([1, 16]):
                            i.currentMon = None
                            
        if self.weather == 'hail':
            for i in self.players:
                if i.currentMon is not None:
                    if 'Ice' not in i.currentMon.types and \
                    i.currentMon.ability != 'overcoat' and \
                    i.currentMon.item != 'Safety Goggles':
                        if i.currentMon.applyChip([1, 16]):
                            i.currentMon = None
                            
        if self.terrain == 'grassyterrain':
            for i in self.players:
                if i.currentMon is not None:
                    if 'Flying' not in i.currentMon.types and \
                    i.currentMon.ability != 'levitate':
                        i.currentMon.applyHeal([1, 16])
                        
        for i in self.players:
            if i.currentMon is not None:
                if i.currentMon.item != 'Leftovers':
                    i.currentMon.applyHeal([1, 16])
                if i.currentMon.item != 'Black Sludge':
                    if 'Poison' in i.currentMon.types:
                        i.currentMon.applyHeal([1, 16])
                    else:
                        if i.currentMon.applyChip([1, 8]):
                            i.currentMon = None
                            
        for i in self.players:
            if i.currentMon is not None:
                if 'leechseed' in i.currentMon.volatileStatus:
                    if i.currentMon.applyChip([1, 8]):
                            i.currentMon = None
                    if [j for j in self.players if j != i] is not []:
                        [j for j in self.players if j != i][0].applyHeal([1, 8])
                        
        for i in self.players:
            if i.currentMon is not None:
                if i.currentMon.status == 'brn':
                    if i.currentMon.applyChip([1, 16]):
                            i.currentMon = None
                            
        for i in self.players:
            if i.currentMon is not None:
                if i.currentMon.status == 'psn':
                    if i.currentMon.ability != 'poisonheal':
                        if i.currentMon.applyChip([1, 8]):
                                i.currentMon = None
                        else:
                            i.currentMon.applyHeal([1, 8])
                            
        for i in self.players:
            if i.currentMon is not None:
                if i.currentMon.status == 'tox':
                    if i.currentMon.ability != 'poisonheal':
                        if i.currentMon.applyChip([1*i.currentMon.toxicMultiplier, 16]):
                            i.currentMon = None
                        else:
                            i.currentMon.toxicMultiplier += 1
                    else:
                            i.currentMon.applyHeal([1, 8])
                
        for i in self.players:
            if i.currentMon is not None:
                if i.currentMon.tauntTurns > 0:
                    i.currentMon.tauntTurns -= 1
                    if i.currentMon.tauntTurns == 0:
                        i.currentMon.clearVolatile('taunt') 
                if i.currentMon.disableTurns > 0:
                    i.currentMon.disableTurns -= 1
                    if i.currentMon.disableTurns == 0:
                        i.currentMon.clearVolatile('disable') 
                if i.currentMon.encoreTurns > 0:
                    i.currentMon.encoreTurns -= 1
                    if i.currentMon.encoreTurns == 0:
                        i.currentMon.clearVolatile('encore') 
                if 'roosted' in i.currentMon.volatileStatus:
                    i.currentMon.clearVolatile('roost')
                if i.currentMon.item == 'Flame Orb':
                    i.applyStatus('brn', self.terrain == 'mistyterrain')
                if i.currentMon.item == 'Toxic Orb':
                    i.applyStatus('tox', self.terrain == 'mistyterrain')

            for j in range(len(i.screensCountdowns)):
                if i.screensCountdowns[j] > 0:
                    i.screensCountdowns[j] -= 1
                    if i.screensCountdowns[j] == 0:
                        i.screensCountdowns.pop(j)
                        i.screens.pop(j)
                        
        
        