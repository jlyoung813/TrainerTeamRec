import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
import pickle
import Pokemon
import sim


class TrainerTeamRec(nn.Module):
    def __init__(self, num_input_dims, l1_dims, l2_dims, num_actions, lr):
        super(TrainerTeamRec, self).__init__()
        self.layer1 = nn.Linear(num_input_dims, l1_dims)
        self.layer2 = nn.Linear(l1_dims, l2_dims)
        self.output = nn.Linear(l2_dims, num_actions)
        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.f1 = nn.ReLU
        self.f1 = self.f1()
        self.f2 = nn.ReLU
        self.f2 = self.f2()

    def forward(self, state):
        x = self.f1(self.layer1(state))
        x = self.f2(self.layer2(x))
        out = self.output(x)
        return out

class TeamRecAgent():
    def __init__(self, gamma, epsilon, lr, num_input_dims, batch_size, num_actions, max_mem=100000, eps_min=0.01, eps_dec=5e-4):
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.lr = lr
        self.action_space = [i for i in range(num_actions)]
        self.mem_size = max_mem
        self.batch_size = batch_size
        self.mem_idx = 0
        self.TeamRec = TrainerTeamRec(num_input_dims, l1_dims=128, l2_dims=128, num_actions=num_actions, lr=lr)
        self.state_memory = np.zeros((self.mem_size, num_input_dims), dtype=np.int32)
        self.new_state_memory = np.zeros((self.mem_size, num_input_dims), dtype=np.int32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.rewards_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=bool)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_idx % self.mem_size
        self.state_memory[index] = state
        self.action_memory[index] = action
        self.rewards_memory[index] = reward
        self.new_state_memory[index] = state_
        self.terminal_memory[index] = done
        self.mem_idx += 1

    def choose_action(self, observation):
        if np.random.random() > self.epsilon:
            state = observation
            actions = self.TeamRec.forward(state)
            action = torch.argmax(actions)
        else:
            action = np.random.choice(self.action_space)
        return action

    def learn(self):
        if self.mem_idx < self.batch_size:
            return
        self.TeamRec.optimizer.zero_grad()
        max_mem = min(self.mem_idx, self.mem_size)
        batch = np.random.choice(max_mem, self.batch_size, replace=False)
        batch_index = np.arange(self.batch_size, dtype=np.int32)
        state_batch = torch.Tensor(self.state_memory[batch])
        new_state_batch = torch.Tensor(self.new_state_memory[batch])
        reward_batch = torch.Tensor(self.rewards_memory[batch])
        terminal_batch = torch.Tensor(self.terminal_memory[batch])
        action_batch = self.action_memory[batch]
        Team_eval = self.TeamRec.forward(state_batch)[batch_index, action_batch]
        Team_next = self.TeamRec.forward(new_state_batch)
        for i in range(len(terminal_batch)):
            if terminal_batch[i] == 1.0:
                Team_next[i] = 0.0
        Team_target = reward_batch + self.gamma * torch.max(Team_next, dim=1)[0]
        loss = self.TeamRec.loss(Team_target, Team_eval)
        loss.backward()
        self.TeamRec.optimizer.step()
        self.epsilon = max(self.epsilon - self.eps_dec, self.eps_min)
