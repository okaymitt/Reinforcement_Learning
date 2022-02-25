from turtle import clear
import numpy as np
import grid_world

import tkinter as tk

FPS = 30

class Sarsa():
    def __init__(self, env, alpha=0.25, gamma=0.9,  eps=0.01, episodes=1000):
        self.env=env
        self.observation_size = self.env.get_observation_size()
        self.state_size = self.env.get_state_size()
        self.action_size = self.env.get_action_size()

        #param
        self.alpha= alpha
        self.gamma = gamma
        self.epsilon = eps
        self.episodes = episodes
        # self.q_values = np.random.uniform(size=(self.state_size, self.action_size))
        self.q_values = np.zeros((self.state_size, self.action_size))


    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.randint(self.action_size)
        else:
            q_value = self.q_values[state]
            return np.argmax(q_value)

    def compute(self, episode=0):
        done = False
        if episode != 0:
                sarsa.env.reset()   # initialize state
                
            
        current_state_idx = self.env.get_current_state_idx()
        action_idx = self.get_action(current_state_idx)

        def compute_episode(done, current_state_idx, action_idx):
            if not done:
                new_state_idx, reward, done = self.env.step(action_idx)
                new_action_idx = self.get_action(new_state_idx)
                self.q_values[current_state_idx][action_idx] += self.alpha*( reward + self.gamma * self.q_values[new_state_idx][new_action_idx] - self.q_values[current_state_idx][action_idx])
                current_state_idx = new_state_idx
                action_idx = new_action_idx
                self.env.canvas.after(int(1000/FPS), compute_episode, done, current_state_idx, action_idx)
            elif episode < self.episodes:
                # self.env.update_stats()
                self.env.canvas.after(int(1000/FPS), self.compute, episode)

        episode += 1
        self.env.canvas.after(int(1000/FPS), compute_episode, done, current_state_idx, action_idx)
        


     # passing a argument in a recursive loop is discussed here: https://stackoverflow.com/questions/11040098/cannot-pass-arguments-from-the-tkinter-widget-after-function                    
            





if __name__ == '__main__':
    gridworld = grid_world.Gridworld(move='cross', modus='RL')
    sarsa = Sarsa(gridworld, episodes=1000^)
    sarsa.compute()

    tk.mainloop()