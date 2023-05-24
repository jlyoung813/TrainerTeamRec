import json
def loadPokemon():
    with open('pokemon_data/pokedex.json', 'r') as file:
        pokedex = json.load(file)
    return pokedex

def loadMoves():
    with open('pokemon_data/moves.json', 'r') as file:
        movedex = json.load(file)
    #==========================shorthand list of properties to implment==========================
    
    #state is an object which contains the two states of the pokemon and field on both sides
    #self and opponent are instances of Pokemon
    #status moves should attempt to apply 'status', 'volitileStatus','sideEffect'
    #status applies a status effect, volitileStatus applies a volitileStatus, sideEffect applies a hazard or screen or something
    
    #basePowerModifier is a multiplier to basePower. inputs some combination of state, user, opponent
    #accuracyModifier replaces the accuracy of the move under certain conditions
    #priorityModifier is added to the priority value. inputs state
    #multihitModifier is added to subsequent hits of moves with the multiaccuracy tag
    #futureTurns returns the number of turns until it hits. logic to delay hit should be added to correct fieldside
    #conditional returns a boolean for moves that require a condition to use (veil, poltergeist)
    #overrideOffesive/DefensiveStat replaced the normally used stat with the value in the field
    #overrideType should override the type
    #override damage should override the entire damage formula and have the damage be fixed to the returned value
    
    WEIGHT_MOVE_THRESHOLDS = [(120, 200.0), (100, 100.0), (80, 50.0), (60, 25.0), (40, 10.0), (20, 0.1)] #lowkick and grassknot moment

    movedex['grassknot']['basePowerModifier'] = lambda state, user, opponent : WEIGHT_MOVE_THRESHOLDS[([opponent.weightkgs >= i[1] for i in WEIGHT_MOVE_THRESHOLDS]).index(True)][0]
    movedex['lowkick']['basePowerModifier'] = lambda state, user, opponent : WEIGHT_MOVE_THRESHOLDS[([opponent.weightkgs >= i[1] for i in WEIGHT_MOVE_THRESHOLDS]).index(True)][0]
    movedex['eruption']['basePowerModifier'] = lambda state, user, opponent : user.stats[0] * 150 // user.maxHp
    movedex['waterspout']['basePowerModifier'] = lambda state, user, opponent : user.stats[0] * 150 // user.maxHp
    movedex['gyroball']['basePowerModifier'] = lambda state, user, opponent : min(25 * opponent.stats[5] // user.stats[5] + 1, 150)
    movedex['knockoff']['basePowerModifier'] = lambda state, user, opponent : 97.5 if opponent.removeItem() else 60 #removeItem is a function to remove item. should fail if target lacks item or is holding unremovable item
    movedex['poltergeist']['conditional'] = lambda state, user, opponent : True if opponent.item != None else False
    movedex['hex']['basePowerModifier'] = lambda state, user, opponent : 130 if opponent.status != None else 65
    movedex['weatherball']['basePowerModifier'] = lambda state, user, opponent : 100 if state.weather != None else 50
    movedex['auroraveil']['conditional'] = lambda state, user, opponent : True if state.weather == 'hail' or state.weather == 'snow' else False
    
    
    movedex['weatherball']['overrideType'] = lambda state, user, opponent : 'Water' if state.weather == 'raindance' else \
                                                                            'Fire' if state.weather == 'sunnyday' else \
                                                                            'Rock' if state.weather == 'sandstorm' else \
                                                                            'Ice' if state.weather == 'hail' or state.weather == 'snow' else \
                                                                            'Normal'
    #insert terrain pulse here
    movedex['finalgambit']['overrideDamage'] = lambda state, user, opponent : user.stats[0]
    
    #can be changed to multipliers by turning ints into acc/70 fractions
    movedex['hurricane']['accuracyModifier'] = lambda state, user, opponent : 101 if state.weather == 'raindance' else 50 if state.weather == 'sunnyday' else 70
    movedex['thunder']['accuracyModifier'] = lambda state, user, opponent : 101 if state.weather == 'raindance' else 50 if state.weather == 'sunnyday' else 70
    movedex['blizzard']['accuracyModifier'] = lambda state, user, opponent : 101 if state.weather == 'hail' or state.weather == 'snow' else 70
    
    movedex['grassyglide']['priorityModifier'] = lambda state, user, opponent: 1 if state.terrain == 'grassyterrain' else 0 
    movedex['futuresight']['futureTurns'] = 3
    movedex['populationbomb']['multihitModifier'] = 0
    movedex['tripleaxel']['multihitModifier'] = 20
    movedex['triplekick']['multihitModifier'] = 20
    
    #TODO: figure out on which side we should implment: haze, defog, rapid spin, trick
    # movedex['clearsmog']['effect'] = 'clearStats
    movedex['defog']['boosts'] = {'boosts': {'evasion': -1}} #defog lost the evasion drop in conversion
    # movedex['defog']['effect'] = 'defog'
    # movedex['haze']['effect'] = 'clearStats' #haze targets all, so should apply this effect to both sidescondition
    # movedex['trick']['effect'] = 'swapItems'
    return movedex

def loadAbilities():
    
    with open('pokemon_data/abilities.json', 'r') as file:
        abilitydex = json.load(file)
    
    #==============================================================abilities============================================================================
    #basePowerModifiers are applied to the base damage
    abilitydex['ironfist']['basePowerModifier'] = lambda move, state, user, opponent: 1.2 if 'punch' in move['flags'].keys() else 1
    abilitydex['sheerforce']['basePowerModifier'] = lambda move, state, user, opponent : 1.3 if move['secondary'] is not None else 1
    abilitydex['strongjaw']['basePowerModifier'] = lambda move, state, user, opponent : 1.5 if 'bite' in move['flags'].keys() else 1
    abilitydex['sandforce']['basePowerModifier'] = lambda move, state, user, opponent : 1.3 if (move['type'] == 'Ground' or move['type'] == 'Rock' or move['type'] == 'Steel') and state.weather == 'sandstorm' else 1
    abilitydex['technician']['basePowerModifier'] = lambda move, state, user, opponent : 1.5 if move['basePower'] <= 60 else 1
    #damageModifiers are applied at the  end of the damage formula
    abilitydex['adaptability']['damageModifier'] = 4/3 #adaptability changes 1.5 -> 2, so 4/3 multiplier
    # abilitydex['analytic']['damageModifier'] = lambda move, state, user, opponent : 1.3
    
    abilitydex['victorystar']['accuracyModifier'] = 1.1

    #stat modifying abilities
    abilitydex['swiftswim']['statModifier'] = lambda state, user, opponent : {'spe': 2} if state.weather == 'raindance' else None
    abilitydex['chlorophyll']['statModifier'] = lambda state, user, opponent : {'spe': 2} if state.weather == 'sunnyday' else None
    abilitydex['solarpower']['statModifier'] = lambda state, user, opponent : {'spa': 1.5} if state.weather == 'sunnyday' else None
    abilitydex['sandrush']['statModifier'] = lambda state, user, opponent : {'spe': 2} if state.weather == 'sandstorm' else None
    abilitydex['slushrush']['statModifier'] = lambda state, user, opponent : {'spe': 2} if state.weather == 'hail' or state.weather == 'snow' else None
    
    #immunity abilities
    abilitydex['levitate']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Ground' else 1
    abilitydex['eartheater']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Ground' else 1
    abilitydex['voltabsorb']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Electric' else 1
    abilitydex['motordrive']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Electric' else 1
    abilitydex['stormdrain']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Water' else 1
    abilitydex['waterabsorb']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Water' else 1
    abilitydex['dryskin']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Water' else 1.25 if move['type'] == 'Fire' else 1
    abilitydex['flashfire']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Fire' else 1
    abilitydex['sapsipper']['incomingModifier'] = lambda move, user : 0 if move['type'] == 'Grass' else 1
    abilitydex['windrider']['incomingModifier'] = lambda move, user : 0 if move['flags']['wind'] == 1 else 1
    abilitydex['sturdy']['incomingModifier'] = lambda move, user : 0 if 'ohko' in move.keys() else 1 #not sure how ohko moves are calced, may move this
    abilitydex['multiscale']['incomingModifier'] = lambda move, user : 0.5 if user.stats[0] == user.maxHp else 1
    
    abilitydex['eartheater']['onActivate'] = lambda move, user : user.applyHeal([1, 4], user.maxHP) if move['type'] == 'Ground' else None
    abilitydex['voltabsorb']['onActivate'] = lambda move, user : user.applyHeal([1, 4], user.maxHP) if move['type'] == 'Electric' else None
    abilitydex['motordrive']['onActivate'] = lambda move, user : user.applyBoost({'spe': 1}) if move['type'] == 'Electric' else None
    abilitydex['stormdrain']['onActivate'] = lambda move, user : user.applyBoost({'spa': 1}) if move['type'] == 'Water' else None
    abilitydex['waterabsorb']['onActivate'] = lambda move, user : user.applyHeal([1, 4], user.maxHP) if move['type'] == 'Water' else None
    abilitydex['dryskin']['onActivate'] = lambda move, user : user.applyHeal([1, 4], user.maxHP) if move['type'] == 'Water' else None
    abilitydex['flashfire']['onActivate'] = lambda move, user : user.applyStatus({'volatileStatus' : 'flashfire'}) if move['type'] == 'Fire' else None
    abilitydex['sapsipper']['onActivate'] = lambda move, user : user.applyBoost({'atk': 1}) if move['type'] == 'Grass' else None
    abilitydex['windrider']['onActivate'] = lambda move, user : user.applyBoost({'atk': 1}) if move['flags']['wind'] == 1 else None
    abilitydex['windpower']['onActivate'] = lambda move, user : user.applyStatus({'volatileStatus' : 'charge'}) if move['flags']['wind'] == 1 else None
    
    # #recoil moves need some way to deal the recoil to the attacker. probably just logic at end of attack
    abilitydex['ironbarbs']['onRecieveHit'] = lambda move : {'chance' : 100, 'chip' : [1, 8]} if 'contact' in move['flags'].keys() else None
    abilitydex['roughskin']['onRecieveHit'] = lambda move : {'chance' : 100, 'chip' : [1, 8]} if 'contact' in move['flags'].keys() else None
    abilitydex['static']['onRecieveHit'] = lambda move : {'chance' : 30, 'status' : 'par'} if 'contact' in move['flags'].keys() else None
    abilitydex['flamebody']['onRecieveHit'] = lambda move : {'chance' : 30, 'status' : 'brn'} if 'contact' in move['flags'].keys() else None
    
    #logic for these properties should be included in the pokemon objects themselves and checked as needed
    abilitydex['sheerforce']['onEntry'] = lambda state, user, opponent : user.ignoreSecondary == True
    abilitydex['infiltrator']['onEntry'] = lambda state, user, opponent : user.ignoreScreens == True
    abilitydex['moldbreaker']['onEntry'] = lambda state, user, opponent : user.ignoreAbilities == True
    abilitydex['intimidate']['onEntry'] = lambda state, user, opponent : opponent.applyBoost({'atk': -1}) if opponent.ability['blockIntimidate'] is None else None
    abilitydex['magnetpull']['onEntry'] = lambda state, user, opponent : opponent.trapped == True if 'Steel' in opponent.types else False
    abilitydex['grassysurge']['onEntry'] = lambda state, user, opponent : state.setTerrain('grassyterrain', 8 if user.item == 'Terrain Extender' else 5)
    abilitydex['electricsurge']['onEntry'] = lambda state, user, opponent : state.setTerrain('electricterrain', 8 if user.item == 'Terrain Extender' else 5)
    abilitydex['psychicsurge']['onEntry'] = lambda state, user, opponent : state.setTerrain('psychicterrain', 8 if user.item == 'Terrain Extender' else 5)
    abilitydex['mistysurge']['onEntry'] = lambda state, user, opponent : state.setTerrain('mistyterrain', 8 if user.item == 'Terrain Extender' else 5)
    abilitydex['drizzle']['onEntry'] = lambda state, user, opponent : state.setWeather('raindance', 8 if user.item == 'Damp Rock' else 5)
    abilitydex['drought']['onEntry'] = lambda state, user, opponent : state.setWeather('drought', 8 if user.item == 'Heat Rock' else 5)
    abilitydex['sandstream']['onEntry'] = lambda state, user, opponent : state.setWeather('sandstorm', 8 if user.item == 'Smooth Rock' else 5)
    abilitydex['snowwarning']['onEntry'] = lambda state, user, opponent : state.setWeather('hail', 8 if user.item == 'Icy Rock' else 5)
    
    abilitydex['speedboost']['onTurnEnd'] = lambda user : user.applyBoost({'spe': 1})
    abilitydex['sturdy']['onTurnEnd'] = lambda user : user.setSurviveOneHit(True) if user.stats.hp == user.stats.maxHp else user.setSurviveOneHit(False)
    
    abilitydex['regenerator']['onExit'] = lambda user: user.applyHeal({'heal' : [1, 3]}, user.maxHP) #this might be moved to a different property
    
    abilitydex['moxie']['onKO'] = lambda user : user.applyBoost({'boosts' : {'atk': 1}})
    abilitydex['chillingneigh']['onKO'] = lambda user : user.applyBoost({'boosts' : {'atk': 1}})
    abilitydex['grimneigh']['onKO'] = lambda user : user.applyBoost({'boosts' : {'spa': 1}})
    abilitydex['beastboost']['onKO'] = lambda user : user.applyBoost({'boosts' : {user.highestStat() : 1}})

    return abilitydex