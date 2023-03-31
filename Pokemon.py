import math


pokedex = dict({
    "barraskewda": {
        "num": 847,
        "types": ["Water"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 61, "atk": 123, "def": 60, "spa": 60, "spd": 50, "spe": 136},
        "abilities": {"0": "Swift Swim", 'H': "Propeller Tail"},
        "heightm": 1.3,
        "weightkg": 30},
    "bisharp": {
        "num": 625,
        "types": ["Dark", "Steel"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 65, "atk": 125, "def": 100, "spa": 60, "spd": 70, "spe": 70},
        "abilities": {"0": "Defiant", '1': "Inner Focus", 'H': "Pressure"},
        "heightm": 1.6,
        "weightkg": 70},
    "blacephalon": {
        "num": 806,
        "types": ["Fire", "Ghost"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 53, "atk": 127, "def": 53, "spa": 151, "spd": 79, "spe": 107},
        "abilities": {"0": "Swift Swim", 'H': "Propeller Tail"},
        "heightm": 1.8,
        "weightkg": 13},
    "blissey": {
        "num": 242,
        "types": ["Normal"],
        "genderRatio": {"M": 0, "F": 1},
        "baseStats": {"hp": 255, "atk": 10, "def": 10, "spa": 75, "spd": 135, "spe": 55},
        "abilities": {"0": "Natural Cure", '1': "Serene Grace", 'H': "Healer"},
        "heightm": 1.5,
        "weightkg": 46.8},
    "buzzwole": {
        "num": 794,
        "types": ["Bug", "Fighting"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 107, "atk": 139, "def": 139, "spa": 53, "spd": 53, "spe": 79},
        "abilities": {"0": "Beast Boost"},
        "heightm": 2.4,
        "weightkg": 333.6},
    "clefable": {
        "num": 36,
        "types": ["Fairy"],
        "genderRatio": {"M": 0.25, "F": 0.75},
        "baseStats": {"hp": 95, "atk": 70, "def": 73, "spa": 95, "spd": 90, "spe": 60},
        "abilities": {"0": "Cute Charm", "1": "Magic Guard", "H": "Unaware"},
        "heightm": 1.3,
        "weightkg": 40},
    "corviknight": {
        "num": 823,
        "types": ["Flying", "Steel"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 98, "atk": 87, "def": 105, "spa": 53, "spd": 85, "spe": 67},
        "abilities": {"0": "Pressure", "1": "Unnerve", "H": "Mirror Armor"},
        "heightm": 2.2,
        "weightkg": 75},
    "dragapult": {
        "num": 887,
        "types": ["Dragon", "Ghost"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 88, "atk": 120, "def": 75, "spa": 100, "spd": 75, "spe": 142},
        "abilities": {"0": "Clear Body", "1": "Infiltrator", "H": "Cursed Body"},
        "heightm": 3,
        "weightkg": 60},
    "dragonite": {
        "num": 149,
        "types": ["Dragon", "Flying"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 91, "atk": 134, "def": 95, "spa": 100, "spd": 100, "spe": 80},
        "abilities": {"0": "Inner Focus",  "H": "Multiscale"},
        "heightm": 2.2,
        "weightkg": 210},
    "ferrothorn": {
        "num": 598,
        "types": ["Grass", "Steel"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 74, "atk": 94, "def": 131, "spa": 54, "spd": 116, "spe": 20},
        "abilities": {"0": "Iron Barbs",  "H": "Anticipation"},
        "heightm": 1,
        "weightkg": 110},
    "garchomp": {
        "num": 445,
        "types": ["Dragon", "Ground"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 108, "atk": 130, "def": 95, "spa": 80, "spd": 85, "spe": 102},
        "abilities": {"0": "Sand Veil",  "H": "Rough Skin"},
        "heightm": 1.9,
        "weightkg": 95},
    "heatran": {
        "num": 485,
        "types": ["Fire", "Steel"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 91, "atk": 90, "def": 106, "spa": 130, "spd": 106, "spe": 77},
        "abilities": {"0": "Flash Fire",  "H": "Flame Body"},
        "heightm": 1.7,
        "weightkg": 430},
    "kartana": {
        "num": 798,
        "types": ["Grass", "Steel"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 59, "atk": 181, "def": 131, "spa": 59, "spd": 31, "spe": 109},
        "abilities": {"0": "Beast Boost"},
        "heightm": 0.3,
        "weightkg": 0.1},
    "landorus-therian": {
        "num": 645,
        "types": ["Ground", "Flying"],
        "genderRatio": {"M": 1, "F": 0},
        "baseStats": {"hp": 89, "atk": 145, "def": 90, "spa": 105, "spd": 80, "spe": 91},
        "abilities": {"0": "Intimidate"},
        "heightm": 1.3,
        "weightkg": 68},
    "magnezone": {
        "num": 462,
        "types": ["Electric", "Steel"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 70, "atk": 70, "def": 115, "spa": 130, "spd": 90, "spe": 60},
        "abilities": {"0": "Magnet Pull", "1": "Sturdy",  "H": "Multiscale"},
        "heightm": 1.2,
        "weightkg": 180},
    "melmetal": {
        "num": 809,
        "types": ["Steel"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 135, "atk": 143, "def": 143, "spa": 80, "spd": 65, "spe": 34},
        "abilities": {"0": "Iron Fist"},
        "heightm": 2.5,
        "weightkg": 800},
    "mew": {
        "num": 151,
        "types": ["Psychic"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 100, "atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
        "abilities": {"0": "Synchronize"},
        "heightm": 0.4,
        "weightkg": 4},
    "ninetales-alola": {
        "num": 38,
        "types": ["Ice", "Fairy"],
        "genderRatio": {"M": 0.25, "F": 0.75},
        "baseStats": {"hp": 73, "atk": 67, "def": 75, "spa": 81, "spd": 100, "spe": 109},
        "abilities": {"0": "Snow Cloak",  "H": "Snow Warning"},
        "heightm": 1.1,
        "weightkg": 19.9},
    "pelipper": {
        "num": 279,
        "types": ["Water", "Flying"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 60, "atk": 50, "def": 100, "spa": 95, "spd": 70, "spe": 65},
        "abilities": {"0": "Keen Eye", "1": "Drizzle",  "H": "Rain Dish"},
        "heightm": 1.2,
        "weightkg": 28},
    "regieleki": {
        "num": 894,
        "types": ["Electric"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 80, "atk": 100, "def": 50, "spa": 100, "spd": 50, "spe": 200},
        "abilities": {"0": "Transistor"},
        "heightm": 1.2,
        "weightkg": 145},
    "rillaboom": {
        "num": 812,
        "types": ["Grass"],
        "genderRatio": {"M": 0.875, "F": 0.125},
        "baseStats": {"hp": 100, "atk": 125, "def": 90, "spa": 60, "spd": 70, "spe": 85},
        "abilities": {"0": "Overgrow",  "H": "Grassy Surge"},
        "heightm": 2.1,
        "weightkg": 90},
    "slowbro": {
        "num": 80,
        "types": ["Water", "Psychic"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 95, "atk": 75, "def": 110, "spa": 100, "spd": 80, "spe": 30},
        "abilities": {"0": "Oblivious", "1": "Own Tempo",  "H": "Regenerator"},
        "heightm": 1.6,
        "weightkg": 78.5},
    "slowking-galar": {
        "num": 199,
        "types": ["Poison", "Psychic"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 95, "atk": 65, "def": 80, "spa": 110, "spd": 110, "spe": 30},
        "abilities": {"0": "Curious Medicine", "1": "Own Tempo",  "H": "Regenerator"},
        "heightm": 1.8,
        "weightkg": 79.5},
    "tapu fini": {
        "num": 788,
        "types": ["Water", "Fairy"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 70, "atk": 75, "def": 115, "spa": 95, "spd": 130, "spe": 85},
        "abilities": {"0": "Misty Surge", "H": "Telepathy"},
        "heightm": 1.3,
        "weightkg": 21.2},
    "tapu koko": {
        "num": 785,
        "types": ["Electric", "Fairy"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 70, "atk": 115, "def": 85, "spa": 95, "spd": 75, "spe": 130},
        "abilities": {"0": "Electric Surge", "H": "Telepathy"},
        "heightm": 1.8,
        "weightkg": 20.5},
    "tapu lele": {
        "num": 786,
        "types": ["Psychic", "Fairy"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 70, "atk": 85, "def": 75, "spa": 130, "spd": 115, "spe": 95},
        "abilities": {"0": "Misty Surge", "H": "Telepathy"},
        "heightm": 1.2,
        "weightkg": 18.6},
    "tornadus-therian": {
        "num": 641,
        "types": ["Flying"],
        "genderRatio": {"M": 1, "F": 0},
        "baseStats": {"hp": 79, "atk": 100, "def": 80, "spa": 110, "spd": 90, "spe": 121},
        "abilities": {"0": "Regenerator"},
        "heightm": 1.4,
        "weightkg": 63},
    "toxapex": {
        "num": 748,
        "types": ["Poison", "Water"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 50, "atk": 63, "def": 152, "spa": 53, "spd": 142, "spe": 35},
        "abilities": {"0": "Merciless", "1": "Limber", "H": "Regenerator"},
        "heightm": 0.7,
        "weightkg": 14.5},
    "tyranitar": {
        "num": 248,
        "types": ["Rock", "Dark"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 100, "atk": 134, "def": 110, "spa": 95, "spd": 100, "spe": 61},
        "abilities": {"0": "Sand Stream", "H": "Unnerve"},
        "heightm": 2,
        "weightkg": 202},
    "urshifu-rapid-strike": {
        "num": 892,
        "types": ["Fighting", "Water"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 100, "atk": 130, "def": 100, "spa": 63, "spd": 60, "spe": 97},
        "abilities": {"0": "Unseen Fist"},
        "heightm": 1.9,
        "weightkg": 105},
    "victini": {
        "num": 494,
        "types": ["Psychic", "Fire"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 100, "atk": 100, "def": 100, "spa": 100, "spd": 100, "spe": 100},
        "abilities": {"0": "Victory Star"},
        "heightm": 0.4,
        "weightkg": 4},
    "volcanion": {
        "num": 721,
        "types": ["Fire", "Water"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 80, "atk": 110, "def": 120, "spa": 130, "spd": 90, "spe": 70},
        "abilities": {"0": "Water Absorb"},
        "heightm": 1.7,
        "weightkg": 195},
    "volcarona": {
        "num": 637,
        "types": ["Bug", "Fire"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 85, "atk": 60, "def": 65, "spa": 135, "spd": 105, "spe": 100},
        "abilities": {"0": "Flame Body", "H": "Swarm"},
        "heightm": 1.6,
        "weightkg": 46},
    "weavile": {
        "num": 461,
        "types": ["Dark", "Ice"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 70, "atk": 120, "def": 65, "spa": 45, "spd": 85, "spe": 125},
        "abilities": {"0": "Pressure", "H": "Pickpocket"},
        "heightm": 1.1,
        "weightkg": 34},
    "zapdos": {
        "num": 145,
        "types": ["Electric", "Flying"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 90, "atk": 90, "def": 85, "spa": 125, "spd": 90, "spe": 100},
        "abilities": {"0": "Pressure", "H": "Static"},
        "heightm": 1.3,
        "weightkg": 52.6},
    "zapdos-galar": {
        "num": 145,
        "types": ["Fighting", "Flying"],
        "genderRatio": {"M": 0.5, "F": 0.5},
        "baseStats": {"hp": 90, "atk": 125, "def": 90, "spa": 85, "spd": 90, "spe": 100},
        "abilities": {"0": "Defiant"},
        "heightm": 1.6,
        "weightkg": 58.2},
    "zeraora": {
        "num": 807,
        "types": ["Electric"],
        "genderRatio": {"M": 0, "F": 0},
        "baseStats": {"hp": 88, "atk": 112, "def": 75, "spa": 102, "spd": 80, "spe": 143},
        "abilities": {"0": "Volt Absorb"},
        "heightm": 1.5,
        "weightkg": 44.5},
      })


moves = {"Aqua Jet": {"accuracy": 100, "basePower": 40, "category": "Physical", "pp": 20, "priority": 1,
                      "flags": {"contact":1}, "type":"Water"},
         "Assurance": {"accuracy": 100, "basePower": 60, "category": "Physical", "pp": 10, "priority": 0,
                       "flags": {"contact":1}, "type": "Dark"},
         "Body Press": {"accuracy": 100, "basePower": 80, "category": "Physical", "pp": 10, "priority": 0,
                        "flags": {"contact":1, "offensiveOverride":"def"}, "type": "Fighting"},
         "Bolt Strike": {"accuracy": 85, "basePower": 130, "category": "Physical", "pp": 5, "priority": 0,
                        "flags": {"contact": 1}, "type": "Electric"},
         "Close Combat": {"accuracy": 100, "basePower": 120, "category": "Physical", "pp": 5, "priority": 0,
                        "flags": {"contact":1, "boosts":{"def":-1, "spd":-1}}, "type": "Fighting"},
         "Crunch": {"accuracy": 100, "basePower": 80, "category": "Physical", "pp": 15, "priority": 0,
                        "flags": {"contact":1, "bite":1, "drop":{"chance":20,"def":-1}}, "type": "Dark"},
         "Dazzling Gleam": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 10, "priority": 0,
                        "flags": {}, "type": "Fairy"},
         "Double Iron Bash": {"accuracy": 100, "basePower": 60, "category": "Physical", "pp": 5, "priority": 0,
                        "flags": {"contact":1, "punch":1, "multihit":2, "flinch":{"chance":30}}, "type": "Steel"},
         "Draco Meteor": {"accuracy": 90, "basePower": 130, "category": "Special", "pp": 5, "priority": 0,
                        "flags": {"boosts":{"spa":-2}}, "type": "Dragon"},
         "Dragon Claw": {"accuracy": 100, "basePower": 80, "category": "Physical", "pp": 15, "priority": 0,
                        "flags": {"contact":1}, "type": "Dragon"},
         "Earth Power": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 10, "priority": 0,
                        "flags": {"drop":{"chance":10,"spd":-1}}, "type": "Ground"},
         "Earthquake": {"accuracy": 100, "basePower": 100, "category": "Physical", "pp": 10, "priority": 0,
                        "flags": {}, "type": "Ground"},
         "Fire Blast": {"accuracy": 85, "basePower": 110, "category": "Special", "pp": 5, "priority": 0,
                        "flags": {"burn":{"chance":10}}, "type": "Fire"},
         "Flamethrower": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 15, "priority": 0,
                        "flags": {"burn":{"chance":10}}, "type": "Fire"},
         "Flash Cannon": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 10, "priority": 0,
                        "flags": {"drop":{"chance":10,"spd":-1}}, "type": "Steel"},
        "Fire Punch": {"accuracy": 100, "basePower": 75, "category": "Physical", "pp": 15, "priority": 0,
                    "flags": {"contact":1, "punch":1, "burn":{"chance":10}}, "type": "Fire"},
         "Fire Fang": {"accuracy": 95, "basePower": 65, "category": "Physical", "pp": 15, "priority": 0,
                    "flags": {"contact":1, "bite":1, "flinch":{"chance":10}, "burn":{"chance":10}}, "type": "Fire"},
         "Flip Turn": {"accuracy": 100, "basePower": 60, "category": "Physical", "pp": 20, "priority": 0,
                       "flags": {"contact": 1, "selfSwitch":1}, "type": "Water"},
         "Focus Blast": {"accuracy": 70, "basePower": 120, "category": "Special", "pp": 5, "priority": 0,
                       "flags": {"bullet": 1, "drop":{"chance":10,"spd":-1}}, "type": "Fighting"},
         "Glaciate": {"accuracy": 95, "basePower": 65, "category": "Special", "pp": 10, "priority": 0,
                       "flags": {"drop":{"chance":100,"spe":-1}}, "type": "Ice"},
         "Grassy Glide": {"accuracy": 100, "basePower": 70, "category": "Physical", "pp": 20, "priority": 0,
                       "flags": {"contact": 1, "priorityOn":"Grassy Terrain"}, "type": "Grass"},
         "Grass Knot": {"accuracy": 100, "basePower": 60, "category": "Special", "pp": 20, "priority": 0,
                          "flags": {"contact": 1, "weightBased": 1}, "type": "Grass"},
         "Heat Wave": {"accuracy": 90, "basePower": 95, "category": "Special", "pp": 10, "priority": 0,
                          "flags": {"burn":{"chance":10}}, "type": "Fire"},
         "Hurricane": {"accuracy": 70, "basePower": 110, "category": "Special", "pp": 10, "priority": 0,
                          "flags": {"weatherAcc": "Rain"}, "type": "Flying"},
         "Ice Beam": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 10, "priority": 0,
                       "flags": {"freeze":{"chance":10}}, "type": "Ice"},
         "Ice Punch": {"accuracy": 100, "basePower": 75, "category": "Physical", "pp": 15, "priority": 0,
                       "flags": {"freeze":{"chance":10}}, "type": "Ice"},
         "Ice Shard": {"accuracy": 100, "basePower": 40, "category": "Physical", "pp": 30, "priority": 1,
                       "flags": {}, "type": "Ice"},
         "Icicle Crash": {"accuracy": 90, "basePower": 85, "category": "Physical", "pp": 10, "priority": 0,
                       "flags": {"flinch":{"chance":30}}, "type": "Ice"},
         "Iron Head": {"accuracy": 100, "basePower": 80, "category": "Physical", "pp": 15, "priority": 0,
                       "flags": {"contact":1, "flinch":{"chance":30}}, "type": "Steel"},
         "Knock Off": {"accuracy": 100, "basePower": 65, "category": "Physical", "pp": 20, "priority": 0,
                       "flags": {"contact":1,"removeItem":1}, "type": "Dark"},

         "Lava Plume": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 15, "priority": 0,
                       "flags": {"burn":{"chance":30}}, "type": "Fire"},
         "Leaf Blade": {"accuracy": 100, "basePower": 90, "category": "Physical", "pp": 15, "priority": 0,
                       "flags": {"contact":1, "highCrit":1}, "type": "Grass"},
         "Leech Life": {"accuracy": 100, "basePower": 80, "category": "Physical", "pp": 10, "priority": 0,
                       "flags": {"contact":1, "drain":1}, "type": "Bug"},
         "Liquidation": {"accuracy": 100, "basePower": 85, "category": "Physical", "pp": 10, "priority": 0,
                       "flags": {"drop":{"chance":10,"def":-1}}, "type": "Water"},
         "Low Kick": {"accuracy": 100, "basePower": 60, "category": "Physical", "pp": 20, "priority": 0,
                       "flags": {"contact": 1, "weightBased": 1}, "type": "Fighting"},
         "Moonblast": {"accuracy": 100, "basePower": 95, "category": "Special", "pp": 15, "priority": 0,
                         "flags": {"drop": {"chance": 30, "spa": -1}}, "type": "Fairy"},
         "Plasma Fists": {"accuracy": 100, "basePower": 100, "category": "Physical", "pp": 15, "priority": 0,
                       "flags": {"contact":1,"punch":1}, "type": "Electric"},
         "Psychic": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 10, "priority": 0,
                       "flags": {"drop": {"chance": 10, "spd": -1}}, "type": "Psychic"},
         "Psyshock": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 10, "priority": 0,
                       "flags": {"defensiveOverride":"def"}, "type": "Psychic"},
         "Sacred Sword": {"accuracy": 100, "basePower": 90, "category": "Physical", "pp": 15, "priority": 0,
                       "flags": {"contact":1}, "type": "Fighting"},
         "Scald": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 15, "priority": 0,
                       "flags": {"burn":{"chance":30}, "defrost":1}, "type": "Water"},
         "Shadow Ball": {"accuracy": 100, "basePower": 80, "category": "Special", "pp": 15, "priority": 0,
                   "flags": {"drop": {"chance": 20, "spd": -1}}, "type": "Ghost"},
         "Sludge Bomb": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 10, "priority": 0,
                         "flags": {"poison":{"chance":30}}, "type": "Poison"},
         "Sludge Wave": {"accuracy": 100, "basePower": 95, "category": "Special", "pp": 10, "priority": 0,
                         "flags": {"poison": {"chance": 10}}, "type": "Poison"},
         "Steam Eruption": {"accuracy": 95, "basePower": 110, "category": "Special", "pp": 5, "priority": 0,
                   "flags": {"burn": {"chance": 30}, "defrost": 1}, "type": "Water"},
         "Surging Strikes": {"accuracy": 100, "basePower": 25, "category": "Physical", "pp": 5, "priority": 0,
                   "flags": {"contact":1,"punch":1,"multihit":3,"alwaysCrit":1}, "type": "Water"},
         "Smart Strike": {"accuracy": 101, "basePower": 70, "category": "Physical", "pp": 10, "priority": 0,
                   "flags": {"contact":1}, "type": "Steel"},
         "Stone Edge": {"accuracy": 80, "basePower": 100, "category": "Physical", "pp": 5, "priority": 0,
                   "flags": {"highCrit":1}, "type": "Rock"},
         "Sucker Punch": {"accuracy": 100, "basePower": 70, "category": "Physical", "pp": 5, "priority": 1,
                        "flags": {"enemyAttacking": 1}, "type": "Dark"},
         "Thunder Punch": {"accuracy": 100, "basePower": 75, "category": "Physical", "pp": 15, "priority": 0,
                        "flags": {"contact": 1, "punch":1, "paralysis": {"chance": 10}}, "type": "Electric"},
         "Thunderbolt": {"accuracy": 100, "basePower": 90, "category": "Special", "pp": 15, "priority": 0,
                        "flags": {"paralysis": {"chance": 10}}, "type": "Electric"},
         "Uturn": {"accuracy": 100, "basePower": 70, "category": "Physical", "pp": 15, "priority": 0,
                        "flags": {"contact": 1, "selfSwitch":1}, "type": "Bug"},
         "Vcreate": {"accuracy": 95, "basePower": 180, "category": "Physical", "pp": 5, "priority": 0,
                        "flags": {"contact": 1, "boosts":{"def":-1, "spd":-1, "spe":-1}}, "type": "Fire"},
         "Volt Switch": {"accuracy": 100, "basePower": 70, "category": "Special", "pp": 20, "priority": 0,
                         "flags": {"selfSwitch":1}, "type": "Electric"},
         "Weather Ball": {"accuracy": 100, "basePower": 50, "category": "Special", "pp": 10, "priority": 0,
                         "flags": {"weatherBall":1}, "type": "Normal"},
         "Wood Hammer": {"accuracy": 100, "basePower": 120, "category": "Special", "pp": 15, "priority": 0,
                         "flags": {"contact":1}, "type": "Grass"}
         }


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
           "Timid": ["spe", "atk"]}


typeChart = {"bug": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 2,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 2,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 1,
			"Steel": 0,
			"Water": 0,
		}
    },
	"dark": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 2,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 1,
			"Fighting": 1,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 2,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 3,
			"Rock": 0,
			"Steel": 0,
			"Water": 0,
		},
	},
	"dragon": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 1,
			"Electric": 2,
			"Fairy": 1,
			"Fighting": 0,
			"Fire": 2,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 0,
			"Ice": 1,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 0,
			"Water": 2,
		}
	},
	"electric": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 2,
			"Fairy": 0,
			"Fighting": 0,
			"Fire": 0,
			"Flying": 2,
			"Ghost": 0,
			"Grass": 0,
			"Ground": 1,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 2,
			"Water": 0,
		}
	},
	"fairy": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 2,
			"Dragon": 3,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 2,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 0,
			"Poison": 1,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 1,
			"Water": 0,
		}
	},
	"fighting": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 2,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 1,
			"Fighting": 0,
			"Fire": 0,
			"Flying": 1,
			"Ghost": 0,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 1,
			"Rock": 2,
			"Steel": 0,
			"Water": 0,
		}
	},
	"fire": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 2,
			"Fighting": 0,
			"Fire": 2,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 1,
			"Ice": 2,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 1,
			"Steel": 2,
			"Water": 1,
		},
	},
	"flying": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 1,
			"Fairy": 0,
			"Fighting": 2,
			"Fire": 0,
			"Flying": 0,
			'Ghost': 0,
			"Grass": 2,
			"Ground": 3,
			"Ice": 1,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 1,
			"Steel": 0,
			"Water": 0,
		}
	},
	"ghost": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 1,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 3,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 1,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 3,
			"Poison": 2,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 0,
			"Water": 0,
		}
	},
	"grass": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 2,
			"Fairy": 0,
			"Fighting": 0,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 2,
			"Ice": 1,
			"Normal": 0,
			"Poison": 1,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 0,
			"Water": 2,
		}
	},
	"ground": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 3,
			"Fairy": 0,
			"Fighting": 0,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 1,
			"Ground": 0,
			"Ice": 1,
			"Normal": 0,
			"Poison": 2,
			"Psychic": 0,
			"Rock": 2,
			"Steel": 0,
			"Water": 1,
		}
	},
	"ice": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			'Fairy': 0,
			"Fighting": 1,
			"Fire": 1,
			'Flying': 0,
			"Ghost": 0,
			"Grass": 0,
			"Ground": 0,
			"Ice": 2,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 1,
			"Steel": 1,
			"Water": 0,
		}
	},
	"normal": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 1,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 3,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 0,
			"Water": 0,
		},
	},
	"poison": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 2,
			"Fighting": 2,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 1,
			"Ice": 0,
			"Normal": 0,
			"Poison": 2,
			"Psychic": 1,
			"Rock": 0,
			"Steel": 0,
			"Water": 0,
		}
	},
	"psychic": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 2,
			"Fire": 0,
			"Flying": 0,
			"Ghost": 1,
			"Grass": 0,
			"Ground": 0,
			"Ice": 0,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 2,
			"Rock": 0,
			"Steel": 0,
			"Water": 0,
		}
	},
	"rock": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 0,
			"Fairy": 0,
			"Fighting": 1,
			"Fire": 2,
			"Flying": 2,
			"Ghost": 0,
			"Grass": 1,
			"Ground": 1,
			"Ice": 0,
			"Normal": 2,
			"Poison": 2,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 1,
			"Water": 1,
		}
	},
	"steel": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 0,
			"Dragon": 2,
			"Electric": 0,
			"Fairy": 2,
			"Fighting": 1,
			"Fire": 1,
			"Flying": 2,
			"Ghost": 0,
			"Grass": 2,
			"Ground": 1,
			"Ice": 2,
			"Normal": 2,
			"Poison": 3,
			"Psychic": 2,
			"Rock": 2,
			"Steel": 2,
			"Water": 0,
		}
	},
	"water": {
		"damageTaken": {
			"Bug": 0,
			"Dark": 0,
			"Dragon": 0,
			"Electric": 1,
			"Fairy": 0,
			"Fighting": 0,
			"Fire": 2,
			"Flying": 0,
			"Ghost": 0,
			"Grass": 1,
			"Ground": 0,
			"Ice": 2,
			"Normal": 0,
			"Poison": 0,
			"Psychic": 0,
			"Rock": 0,
			"Steel": 2,
			"Water": 2,
		}
	}
}

def DamageCalc(mon1, mon2, move):
    if moves[move]["category"] == "Physical":
        attack = mon1.stats[1]
        defense = mon2.stats[2]
    if moves[move]["category"] == "Special":
        attack = mon1.stats[3]
        defense = mon2.stats[4]
    if "offensiveOverride" in moves[move]["flags"].keys():
        for loc, stat in enumerate(stats):
            if stat == moves[move]["flags"]["offensiveOverride"]:
                attack = mon1.stats[loc]
    if "defensiveOverride" in moves[move]["flags"].keys():
        for loc, stat in enumerate(stats):
            if stat == moves[move]["flags"]["defensiveOverride"]:
                defense = mon2.stats[loc]
    power = moves[move]["basePower"]
    damage = math.floor((((2*100)/5+2) * power * (attack / defense))/50+2)
    moveType = moves[move]["type"]
    if mon1.types.count(moveType) > 0:
       damage = math.floor(damage * 1.5)
    for type in mon2.types:
        val = typeChart[type.lower()]["damageTaken"][moveType]
        if val == 1:
            damage = math.floor(damage * 2)
        if val == 2:
            damage = math.floor(damage / 2)
        if val == 3:
            damage = 0
    return damage

def HpCalc(base,iv=0,ev=0):
    hp = math.floor(((2 * base + iv + math.floor(ev / 4)) * 100) / 100) + 100 + 10
    return hp


def StatCalc(base,iv=0,ev=0, nature=1):
    stat = math.floor((math.floor(((2 * base + iv + math.floor(ev / 4)) * 100)/100) + 5) * nature)
    return stat


class Pokemon:
    def __init__(self, name, ability, moves, evs = [0,0,0,0,0,0], ivs=[31,31,31,31,31,31], nature="Hardy", item = ""):
        self.name = name
        self.types = pokedex[name]["types"]
        self.ability = ability
        self.evs = evs
        self.ivs = ivs
        self.nature = nature
        self.stats = [0,0,0,0,0,0]
        self.stats[0] = HpCalc(pokedex[name]["baseStats"]["hp"], ivs[0], evs[0])
        for loc, stat in enumerate(stats):
            if loc >= 1 and stat in pokedex[name]["baseStats"].keys():
                natureval = 1
                if nature in natures.keys():
                    if natures[nature][0] == stat:
                        natureval = 1.1
                    if natures[nature][1] == stat:
                        natureval = 0.9
                self.stats[loc] = StatCalc(pokedex[name]["baseStats"][stat], ivs[loc], evs[loc], natureval)
        self.moves = moves
        self.item = item

    def __str__(self):
        return "%s @ %s\nAbility: %s\n%s Nature" % (self.name, self.item, self.ability, self.nature)


def LoadSet(monSet):
    line1 = monSet[0].split('@')
    name = line1[0].lower().strip()
    line2 = monSet[1].split(':')
    ability = line2[1].strip()
    line3 = monSet[2].split(':')
    evread = line3[1].strip().split('/')
    evlist =[]
    for e in evread:
        e = e.strip().split()
        e.reverse()
        e[0] = e[0].lower()
        evlist.append(e)
    evdict = dict(evlist)
    evs = [0,0,0,0,0,0]
    for loc, stat in enumerate(stats):
        if stat in evdict.keys():
            evs[loc] = (int)(evdict[stat])
    line4 = monSet[3].split()
    nature = line4[0]
    line5 = monSet[4]
    moves = []
    for line in line5:
        moves.append(line.split('-')[1].strip())
    mon = Pokemon(name, ability, moves, evs, nature=nature)
    return mon


def CompareTeams(team1, team2):
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
    return wins/rounds


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
