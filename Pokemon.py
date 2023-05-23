import math

from load_data import loadPokemon, loadMoves, loadAbilities
pokedex = loadPokemon()
movedex = loadMoves()
abilitydex = loadAbilities()
print(type(pokedex))

def HpCalc(base,iv=0,ev=0):
    hp = math.floor(((2 * base + iv + math.floor(ev / 4)) * 100) / 100) + 100 + 10
    return hp

def StatCalc(base,iv=0,ev=0, nature=1):
    stat = math.floor((math.floor(((2 * base + iv + math.floor(ev / 4)) * 100)/100) + 5) * nature)
    return stat

stats = ["hp", "atk", "def", "spa", "spd", "spe"]


natures = {"Adamant": ["atk", "spa"],
           "Bashful": ["",""],
           "Bold": ["def", "atk"],
           "Brave": ["atk", "spe"],
           "Calm": ["spd", "atk"],
           "Careful": ["spd", "spa"],
           "Docile": ["",""],
           "Gentle": ["spd", "def"],
           "Hardy": ["",""],
           "Hasty": ["spe", "def"],
           "Impish": ["def", "spa"],
           "Jolly": ["spe", "spa"],
           "Lax": ["def", "spa"],
           "Lonely": ["atk", "def"],
           "Mild": ["spa", "def"],
           "Modest": ["spa", "atk"],
           "Naive": ["spe", "spd"],
           "Naughty": ["atk", "spd"],
           "Quiet": ["spa", "spe"],
           "Quirky": ["",""],
           "Rash": ["spa", "spd"],
           "Relaxed": ["def", "spe"],
           "Sassy": ["spd", "spe"],
           "Serious": ["",""],
           "Timid": ["spe", "atk"]
           }

class Pokemon:
    def __init__(self, name, ability, moves, evs=[0, 0, 0, 0, 0, 0], ivs=[31, 31, 31, 31, 31, 31], nature="Hardy",
                 item=""):
        dex = pokedex.copy()
        self.name = name
        self.types = dex[name]["types"]
        self.ability = ability
        self.evs = evs
        self.ivs = ivs
        self.nature = nature
        self.stats = [0, 0, 0, 0, 0, 0]
        self.stats[0] = HpCalc(dex[name]["baseStats"]["hp"], ivs[0], evs[0])
        self.highestStat = ""
        maxStat = -1
        for loc, stat in enumerate(stats):
            if loc >= 1 and stat in dex[name]["baseStats"].keys():
                natureval = 1
                if nature in natures.keys():
                    if natures[nature][0] == stat:
                        natureval = 1.1
                    if natures[nature][1] == stat:
                        natureval = 0.9
                self.stats[loc] = StatCalc(dex[name]["baseStats"][stat], ivs[loc], evs[loc], natureval)
                if self.stats[loc] > maxStat:
                    maxStat = self.stats[loc]
                    self.highestStat = stat
        self.moves = moves
        self.item = item
        self.maxHp = self.stats[0]
        self.statStages = [0, 0, 0, 0, 0]
        self.removeItem = True
        self.weightkgs = dex[name]["weightkg"]
        self.status = None
        self.volatileStatus = []
        self.lastUsedMove = -1

        self.toxicMultiplier = 1
        self.trapped = False
        self.tauntTurns = 0
        self.disableTurns = 0
        self.encoreTurns = 0
        self.disabledMove = -1
        self.encoredMove = -1
        self.ignoreSecondary = False
        self.surviveOneHit = False
        self.ignoreScreens = False
        self.ignoreAbilities = False

    def __str__(self):
        return f"{self.name} @ {self.item}\nAbility: {self.ability}\n{self.nature} Nature"


        return "%s @ %s\nAbility: %s\n%s Nature" % (self.name, self.item, self.ability, self.nature)

    def removeItem(self):
        if self.item == None:
            return False
        else:
            self.item = None
            return True


    # def applyEffect(effect):
    #     return

    #this function should parse various effects(recoil, stat modifications, healing)
    def applyBoost(self, boost):
        if 'atk' in boost:
            self.statStages[0] += boost['atk']
        if 'def' in boost:
            self.statStages[1] += boost['def']
        if 'spa' in boost:
            self.statStages[2] += boost['spa']
        if 'spd' in boost:
            self.statStages[3] += boost['spd']
        if 'spe' in boost:
            self.statStages[4] += boost['spe']

    def applyHeal(self, heal):
        self.stats[0] += math.floor(self.maxHP / (heal[0] / heal[1]))
        if self.stats[0] > self.maxHP:
            self.stats[0] = self.maxHP

    #misty terrain check moved here
    def applyStatus(self, status, isMisty):
        if status['status'] is not None:
            if not (isMisty == False and 'Flying' not in self.types and self.ability != 'levitate' and 'roost' not in self.volatileStatus):
                if self.status is not None:
                    if (status == 'psn' or status == 'tox') and ('Steel' in self.types or 'Poison' in self.types):
                        status = None
                    if (status == 'brn') and ('Fire' in self.types):
                        status = None
                    if (status == 'par') and ('Electric' in self.types):
                        status = None
                    if (status == 'frz') and ('Ice' in self.types):
                        status = None
                    self.status = status['status']
        if status['volatileStatus'] is not None:
            if status['volatileStatus'] not in self.volatileStatus:
                if status['volatileStatus'] == 'confusion':
                    if isMisty == True and 'Flying' not in self.types and self.ability != 'levitate' and 'roost' not in self.volatileStatus:
                        status = None
                if status['volatileStatus'] == 'leechseed':    
                    if 'Grass' not in self.types:
                        status = None
                self.volatileStatus.append(status['volatileStatus'])
                if status['volatileStatus'] == 'taunt':
                    self.tauntTurns = 3
                if status['volatileStatus'] == 'disable':
                    self.disableTurns = 3
                    self.disabledMove = self.lastUsedMove
                if status['volatileStatus'] == 'encore':
                    self.encoreTurns = 3
                    self.encoredMove = self.lastUsedMove
    
    def clearVolatile(self, volatileStatus):
        if volatileStatus == 'all':
            self.volatileStatus = []
            self.tauntTurns = 0
            self.disableTurns = 0
            self.encoreTurns = 0
            self.disabledMove = -1
            self.encoredMove = -1
        if volatileStatus in self.volatileStatus:
            self.volatileStatus.pop(volatileStatus)
            if volatileStatus == 'taunt':
                self.tauntTurns = 0
            if volatileStatus == 'disable':
                self.disableTurns = 0
                self.disabledMove = -1
            if volatileStatus == 'encore':
                self.encoreTurns = 0
                self.encoredMove = -1
    
    #chip is going to encompass all % max hp damage. return True if the mon is Koed
    def applyChip(self, chip):
        if self.ability != 'magicguard':
            self.stats[0] -= math.floor(self.maxHP / (chip[0] / chip[1]))
            return self.stats[0] <= 0
    
def LoadSet(monSet):
    line1 = monSet[0].split('@')
    name = line1[0].lower().strip().replace('-', '').replace(' ', '')
    item = line1[1].strip()
    line2 = monSet[1].split(':')
    ability = line2[1].lower().replace(' ', '')
    line3 = monSet[2].split(':')
    evread = line3[1].strip().split('/')
    evlist =[]
    for e in evread:
        e = e.strip().split()
        e.reverse()
        e[0] = e[0].lower()
        evlist.append(e)
    evdict = dict(evlist)
    evs = [0, 0, 0, 0, 0, 0]
    for loc, stat in enumerate(stats):
        if stat in evdict.keys():
            evs[loc] = (int) (evdict[stat])
    line4 = monSet[3].split()
    nature = line4[0]
    line5 = monSet[4]
    moves = []
    for line in line5:
        moves.append(line.replace('-', '').replace(' ', ''))
    mon = Pokemon(name, ability, moves, evs, nature=nature, item=item)
    return mon


"""def CompareTeams(team1, team2):
    wins = 0
    rounds = 0
    for mon1 in team1:
        for mon2 in team2:
            rolls = []
            for move in mon1.moves:
                rolls.append(DamageCalc(mon1,mon2,move))
            maxRoll = max(rolls)
            ttk1 = math.ceil(mon2.stats[0]/maxRoll)
            rolls = []
            moves = []
            for move in mon2.moves:
                rolls.append(DamageCalc(mon2, mon1, move))
                moves.append(move)
            maxRoll = max(rolls)
            ttk2 = math.ceil(mon1.stats[0] / maxRoll)
            if ttk1 < ttk2 or (mon1.stats[5] > mon2.stats[5] and ttk1 == ttk2):
                wins += 1
            else:
                bestMove = moves[rolls.index(maxRoll)]
                for mon in team1:
                    if mon != mon1:
                        for move in mon.moves:
                            rolls.append(DamageCalc(mon, mon2, move))
                        maxRoll = max(rolls)
                        ttk1 = math.ceil(mon2.stats[0] / maxRoll)
                        rolls = []
                        for move in mon2.moves:
                            rolls.append(DamageCalc(mon2, mon, move))
                        maxRoll = max(rolls)
                        ttk2 = math.ceil((mon.stats[0] - DamageCalc(mon2, mon, bestMove)) / maxRoll)
                        if ttk1 < ttk2 or (mon.stats[5] > mon2.stats[5] and ttk1 == ttk2):
                            wins += 1
                            break
            rounds += 1
    return wins/rounds"""


def BuildSets():
    file = open('sets.txt', 'r')
    lines = file.read()
    lines = lines.split('#')
    mons = []
    for line in lines:
        line = line.strip().split('\n')
        sets = [line[0], line[1], line[2], line[3], line[4:]]
        mon = LoadSet(sets)
        mons.append(mon)
    file.close()
    return mons

mons = BuildSets()
print(mons[0])