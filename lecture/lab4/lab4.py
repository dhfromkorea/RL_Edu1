import gym
import sys
import numpy as np
from gym.envs.registration import register
import random
import matplotlib.pyplot as plt
import matplotlib


def rargmax(vector):
    '''
    input :
        1D vector 
    return :
        one of the max indices
    '''
    m = np.max(vector)
    indices = np.transpose(np.nonzero(vector == m)[0])#Get every max indices
    return indices[np.random.randint(len(indices))]#return one of the value

def random(vector):
    '''
    input :
        1D vector
    return :
        random index
    '''
    return np.random.randint(len(vector))

#Env setting
register(
        id = 'FrozenLake-v3',
        entry_point = 'gym.envs.toy_text:FrozenLakeEnv',
        kwargs = {'map_name' : '4x4', 'is_slippery':False}
)

env = gym.make('FrozenLake-v3')


#Initalization
print("Q space initialized")
print("({} x {} )".format(env.observation_space.n,env.action_space.n))
Q = np.zeros([env.observation_space.n,env.action_space.n])

#Hyper_parameter
n_episodes = 50000
discount_rate = 0.95

reward_per_episode = np.zeros(n_episodes)

for i in range(n_episodes):
    # Start new Episode
    state = env.reset()
    done = False
    total_reward = 0

    e = 1. /((i/10)+1) #decrease as episode increase

    while not done:
        #Choose action by e-greedy
        # with probability e chooe random 
        # with probability 1-e chooe greedy
        action = random(Q[state,:])
        if np.random.rand(1)>e:
            action = rargmax(Q[state,:])
        
        #Get new state and reward from environment
        new_state, reward, done, info =env.step(action)
        
        #Update Q-Table with new knowledge using learning rate
        Q[state, action] = reward + discount_rate*np.max(Q[new_state,:])
        state = new_state
        total_reward+=reward
    
    reward_per_episode[i]=total_reward
    
print("Success rate : "+str(np.sum(reward_per_episode)/n_episodes))
print("Final Q-Table Values")
print("LEFT = 0, DOWN = 1, RIGHT = 2, UP = 3")
print(Q)
plt.figure(figsize=(8,12))
plt.title("Reward_per_episode")
plt.plot(reward_per_episode)
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.savefig("reward_per_episode.png")
