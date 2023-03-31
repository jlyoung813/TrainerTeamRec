import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

import numpy as np
import random
import os

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

import Pokemon
from Pokemon import Pokemon, CompareTeams, LoadSet, BuildSets

import time

class TeamRecEnv(Env):
    def __init__(self):
        self.pokemon = BuildSets()
        self.action_space = MultiDiscrete([6, 20])
        self.observation_space = MultiDiscrete([25, 25, 25, 25, 25, 25])
        self.state = random.sample(range(25), 6)
        self.ep_length = 6

    def step(self, action):
        problem = []
        for s in self.state:
            problem.append(self.pokemon[s])
        candidates = []
        for i in range(25):
            add = True
            for s in self.state:
                if i == s:
                    add = False
            if add:
                candidates.append(i)
        candidates.append(self.state[action[0]])
        self.state[action[0]] = candidates[action[1]]
        self.ep_length -= 1
        team = []
        for s in self.state:
            team.append(self.pokemon[s])
        winrate1 = CompareTeams(team, problem)
        winrate2 = CompareTeams(problem, team)
        if winrate1 > winrate2:
            reward = 1
        else:
            if winrate1 == winrate2:
                reward = 0
            else:
                reward = -1
        if self.ep_length <= 0:
            done = True
        else:
            done = False
        info = {}
        return self.state, reward, done, info

    def render(self):
        pass

    def reset(self):
        self.state = random.sample(range(25), 6)
        self.ep_length = 6
        return self.state

"""
env = TeamRecEnv()
episodes = 5
for episode in range(episodes):
    obs = env.reset()
    done = False
    score = 0
    while not done:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        score += reward
    print("Episode:{} Score:{}".format(episode, score))
env.close()
"""




"""
env = TeamRecEnv()
log_path = os.path.join('Training', 'Logs')
model = PPO('MlpPolicy', env, verbose=1,tensorboard_log=log_path)
model.learn(total_timesteps=1000000)

teamrec_path = os.path.join('Training', 'Saved Models', 'Team_Rec_Model_PPO')
model.save(teamrec_path)

del model
model = PPO.load(teamrec_path, env)

print(evaluate_policy(model, env, n_eval_episodes=10))
"""


env = TeamRecEnv()
teamrec_path = os.path.join('Training', 'Saved Models', 'Team_Rec_Model_PPO')
model = PPO.load(teamrec_path, env)

start = time.time()
sumscore = 0
episodes = 5
pokemon = BuildSets()
for episode in range(1, episodes +1):
    obs = env.reset()
    for o in obs:
        print(pokemon[o])
    done = False
    score = 0
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        score += reward
    print("Episode:{} Score:{}".format(episode, score))
    for o in obs:
        print(pokemon[o])
    print('\n')
    sumscore += score
end = time.time()
print(sumscore/(episodes))
time = end - start
print(time)
print(time/episodes)
# print(evaluate_policy(model, env, n_eval_episodes=5000))
env.close()
