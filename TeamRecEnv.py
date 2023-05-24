import random

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import pickle
import Pokemon
import sim
import TrainerTeamRec
from TrainerTeamRec import TeamRecAgent
from TrainerTeamRec import TrainerTeamRec

mons = Pokemon.BuildSets()
max_actions = 94
timestep = 0

def make_vector(team, step):
    vec = torch.zeros(len(mons) + 1)
    for mon in team:
        vec[mon.index] = 1
    vec[len(mons)] = step
    return vec


def make_action(team, step, act):
    mon = team[step]
    names = [m.name for m in team if m.name != mon.name]
    names2 = [m.name for m in team]
    print(names, names2)
    indices = [p.index for p in team if p.name != mon.name]
    it = [x for x in range(len(mons)) if mons[x].name not in names]
    for x in range(len(it), max_actions):
        it.append(mon.index)
    newteam = [mons[j].copy() for j in indices]
    if step >= len(newteam):
        newteam.append(mons[it[act]].copy())
    else:
        newteam.insert(step, mons[it[act]].copy())
    names = [m.name for m in team]
    return newteam


def reset():
    count = 1
    while count > 0:
        count = 0
        team = random.sample(range(len(mons)), 6)
        for x in range(len(team) -1):
            for y in range(x+1, len(team)):
                count += mons[team[x]].name == mons[team[y]].name
    return [mons[k].copy() for k in team]


def reward_val(actteam, cur_team):
    winrate = 0
    indices1 = [m.index for m in cur_team]
    indices2 = [m.index for m in actteam]
    if indices1 == indices2:
        return 0.5
    for x in range(10):
        winrate += sim.battle(actteam, cur_team)
    return winrate/10

agent = TeamRecAgent(0.99, 1.0, lr=0.003, num_input_dims=len(mons) + 1, batch_size=64, num_actions=max_actions)
scores, eps_history = [], []
n_games = 50

for i in range(n_games):
    score = 0
    cur_team = reset()
    timestep = 0
    done = False
    observation = make_vector(cur_team, timestep)
    while not done:
        action = agent.choose_action(observation)
        actteam = make_action(cur_team, timestep, action)
        observation_ = make_vector(actteam, timestep)
        reward = reward_val(actteam, cur_team)
        score += reward
        cur_team = actteam
        timestep += 1
        done = timestep == 6
        agent.store_transition(observation, action, reward, observation_, done)
        agent.learn()
        observation = observation_
    print("score:", score)
