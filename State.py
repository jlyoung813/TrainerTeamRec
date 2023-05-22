from load_data import loadDicts
from Player import Player
from Pokemon import Pokemon
pokedex, movedex, abilitydex = loadDicts

class State:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.weather = None
        self.weatherCount = 0
        self.terrain = None
        self.terrainCount = 0
    
    def setWeather(self, weather, turns):
        if self.weather != weather:
            self.weather = weather
            self.weatherCount = turns
            # return True
            
    def setTerrain(self, terrain, turns):
        if self.terrain != terrain:
            self.terrain = terrain
            self.terrainCount = turns
            # return True
    
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
            abilitydex['self.players[playerIdx].currentMon.ability']['onEntry'](self, self.players[playerIdx], self.players[1-playerIdx])