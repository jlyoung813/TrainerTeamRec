import math

import Pokemon
from load_data import loadPokemon, loadMoves, loadAbilities
pokedex = loadPokemon()
movedex = loadMoves()
abilitydex = loadAbilities()

stats = ["hp", "atk", "def", "spa", "spd", "spe"]

typeChart = {"bug": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 0.5,
			"Fire": 2,
			"Flying": 2,
			"Ghost": 1,
			"Grass": 0.5,
			"Ground": 0.5,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 2,
			"Steel": 1,
			"Water": 1,
		}
    },
	"dark": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 0.5,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 2,
			"Fighting": 2,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 0.5,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 0,
			"Rock": 1,
			"Steel": 1,
			"Water": 1,
		},
	},
	"dragon": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 2,
			"Electric": 0.5,
			"Fairy": 2,
			"Fighting": 1,
			"Fire": 0.5,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 0.5,
			"Ground": 1,
			"Ice": 2,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 1,
			"Water": 0.5,
		}
	},
	"electric": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 0.5,
			"Fairy": 1,
			"Fighting": 1,
			"Fire": 1,
			"Flying": 0.5,
			"Ghost": 1,
			"Grass": 1,
			"Ground": 2,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 0.5,
			"Water": 1,
		}
	},
	"fairy": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 0.5,
			"Dragon": 0,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 0.5,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 1,
			"Poison": 2,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 2,
			"Water": 1,
		}
	},
	"fighting": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 0.5,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 2,
			"Fighting": 1,
			"Fire": 1,
			"Flying": 2,
			"Ghost": 1,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 2,
			"Rock": 0.5,
			"Steel": 1,
			"Water": 1,
		}
	},
	"fire": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 0.5,
			"Fighting": 1,
			"Fire": 0.5,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 0.5,
			"Ground": 2,
			"Ice": 0.5,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 2,
			"Steel": 0.5,
			"Water": 2,
		},
	},
	"flying": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 2,
			"Fairy": 1,
			"Fighting": 0.5,
			"Fire": 1,
			"Flying": 1,
			'Ghost': 1,
			"Grass": 0.5,
			"Ground": 0,
			"Ice": 2,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 2,
			"Steel": 1,
			"Water": 1,
		}
	},
	"ghost": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 2,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 0,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 2,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 0,
			"Poison": 0.5,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 1,
			"Water": 1,
		}
	},
	"grass": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 0.5,
			"Fairy": 1,
			"Fighting": 1,
			"Fire": 2,
			"Flying": 2,
			"Ghost": 2,
			"Grass": 0.5,
			"Ground": 0.5,
			"Ice": 2,
			"Normal": 1,
			"Poison": 2,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 1,
			"Water": 0.5,
		}
	},
	"ground": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 0,
			"Fairy": 1,
			"Fighting": 1,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 2,
			"Ground": 1,
			"Ice": 2,
			"Normal": 1,
			"Poison": 0.5,
			"Psychic": 1,
			"Rock": 0.5,
			"Steel": 1,
			"Water": 2,
		}
	},
	"ice": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			'Fairy': 1,
			"Fighting": 2,
			"Fire": 2,
			'Flying': 1,
			"Ghost": 1,
			"Grass": 1,
			"Ground": 1,
			"Ice": 0.5,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 2,
			"Steel": 2,
			"Water": 1,
		}
	},
	"normal": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 2,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 0,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 1,
			"Water": 1,
		},
	},
	"poison": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 0.5,
			"Fighting": 0.5,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 0.5,
			"Ground": 2,
			"Ice": 1,
			"Normal": 1,
			"Poison": 0.5,
			"Psychic": 2,
			"Rock": 1,
			"Steel": 1,
			"Water": 1,
		}
	},
	"psychic": {
		"damageTaken": {
			"Bug": 2,
			"Dark": 2,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 0.5,
			"Fire": 1,
			"Flying": 1,
			"Ghost": 2,
			"Grass": 1,
			"Ground": 1,
			"Ice": 1,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 0.5,
			"Rock": 1,
			"Steel": 1,
			"Water": 1,
		}
	},
	"rock": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 1,
			"Fairy": 1,
			"Fighting": 2,
			"Fire": 0.5,
			"Flying": 0.5,
			"Ghost": 1,
			"Grass": 2,
			"Ground": 2,
			"Ice": 1,
			"Normal": 0.5,
			"Poison": 0.5,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 2,
			"Water": 2,
		}
	},
	"steel": {
		"damageTaken": {
			"Bug": 0.5,
			"Dark": 1,
			"Dragon": 0.5,
			"Electric": 1,
			"Fairy": 0.5,
			"Fighting": 2,
			"Fire": 2,
			"Flying": 0.5,
			"Ghost": 1,
			"Grass": 0.5,
			"Ground": 2,
			"Ice": 0.5,
			"Normal": 0.5,
			"Poison": 0,
			"Psychic": 0.5,
			"Rock": 0.5,
			"Steel": 0.5,
			"Water": 1,
		}
	},
	"water": {
		"damageTaken": {
			"Bug": 1,
			"Dark": 1,
			"Dragon": 1,
			"Electric": 2,
			"Fairy": 1,
			"Fighting": 1,
			"Fire": 0.5,
			"Flying": 1,
			"Ghost": 1,
			"Grass": 2,
			"Ground": 1,
			"Ice": 0.5,
			"Normal": 1,
			"Poison": 1,
			"Psychic": 1,
			"Rock": 1,
			"Steel": 0.5,
			"Water": 0.5,
		}
	}
}

class calc:
	def __init__(self):
		pass

	def DamageCalc(self, mon1, mon2, move, field, random):
		moves = movedex
		abilities = abilitydex
		if 'overrideDamage' in moves[move].keys():
			return moves[move]['overrideDamage'](field, mon1, mon2)
		move_type = moves[move]["type"]
		if "overrideType" in moves[move].keys():
			move_type = moves[move]['overrideType'](field, mon1, mon2)
		burn = 1
		if moves[move]["category"] == "Status":
			return 0
		atk_stage = 1
		def_stage = 1
		choice = 1
		if moves[move]["category"] == "Physical":
			attack = mon1.stats[1]
			atk_stage = Pokemon.stage(mon1.statStages[0])
			defense = mon2.stats[2]
			def_stage = Pokemon.stage(mon2.statStages[1])
			if mon1.item == "Choice Band":
				choice = 1.5
			if mon1.status == 'brn':
				burn = 0.5

		if moves[move]["category"] == "Special":
			attack = mon1.stats[3]
			atk_stage = Pokemon.stage(mon1.statStages[2])
			defense = mon2.stats[4]
			def_stage = Pokemon.stage(mon2.statStages[3])
			if mon1.item == "Choice Specs":
				choice = 1.5
			if mon2.item == "Assault Vest":
				defense *= 1.5
		if "overrideOffensiveStat" in moves[move].keys():
			for loc, stat in enumerate(stats):
				if stat == moves[move]["overrideOffensiveStat"]:
					attack = mon1.stats[loc]
					atk_stage = Pokemon.stage(mon1.statStages[loc])
		if "overrideDefensiveStat" in moves[move].keys():
			for loc, stat in enumerate(stats):
				if stat == moves[move]["overrideDefensiveStat"]:
					defense = mon2.stats[loc]
					def_stage = Pokemon.stage(mon2.statStages[loc])
		attack = math.floor(attack * atk_stage)
		defense = math.floor(defense * def_stage)
		power = moves[move]["basePower"]
		if "basePowerModifier" in moves[move].keys():
			power = moves[move]["basePowerModifier"](field, mon1, mon2)
		weather = 1
		if field.weather == 'drought':
			if move_type == 'Fire':
				weather = 1.5
			if move_type == 'Water':
				weather = 0.5
		if field.weather == 'raindance':
			if move_type == 'Fire':
				weather = 0.5
			if move_type == 'Water':
				weather = 1.5
		if not (mon1.grounded()):
			if field.terrain == "grassyterrain" and move_type == 'Grass':
				power *= 1.3
			if field.terrain == "electricterrain" and move_type == 'Electric':
				power *= 1.3
			if field.terrain == "psychicterrain" and move_type == 'Psychic':
				power *= 1.3
			if field.terrain == "mistyterrain" and move_type == 'Dragon':
				power *= 0.5
		damage = math.floor((((2 * 100) / 5 + 2) * power * (attack * choice / defense)) / 50 + 2)
		if move_type == "Ground" and mon2.item == "Air Balloon":
			return 0
		if mon1.types.count(move_type) > 0:
			if mon1.ability == "adaptability":
				damage = math.floor(damage * 2)
			else:
				damage = math.floor(damage * 1.5)
		for t in mon2.types:
			val = typeChart[t.lower()]["damageTaken"][move_type]
			damage = math.floor(damage * val)
		lorb = 1 + 0.3 * (mon1.item == "Life Orb")
		ability1 = 1
		ability2 = 1
		if "basePowerModifier" in abilities[mon1.ability].keys():
			ability1 = abilities[mon1.ability]["basePowerModifier"](moves[move], field, mon1, mon2)
		if not mon1.ignoreAbilities and "incomingModifier" in abilities[mon2.ability].keys():
			ability2 = abilities[mon2.ability]["incomingModifier"](moves[move], mon2)
		damage *= lorb * ability1 * ability2 * burn * weather
		return math.floor(damage * random)



