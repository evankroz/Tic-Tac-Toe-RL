import numpy as np
import ttrand as ttrand
import gymnasium as gym
import pygame as pg

env = gym.make("CartPole-v1", render_mode = "human")
env.reset()

class Train(): 
    def __init__(self):
        pass

if __name__ == "__main__":
    for _ in range(100):
        env.render()
        print(env.step(env.action_space.sample()))
        env.close

