from dqn_keras import Agent
import numpy as np


class AI:
    def __init__(self, fname):
        lr = 0.0005
        self.episode = 0
        self.agent = Agent(gamma=0.99, epsilon=0.0, alpha=lr, input_dims=6,
                  n_actions=3, mem_size=1000000, batch_size=64, epsilon_end=0.0, fname=fname)
        self.scores = []
        self.eps_history = []
        self.score = 0
        self.done = False
        self.observation = []
        self.action = 0
        self.n_step = 0
        self.fname = fname.split("/")[-1]

    def episode_start(self, observation):
        self.done = False
        self.score = 0
        self.observation = observation

    def choose_action(self):
        self.action = self.agent.choose_action(self.observation)
        return self.action

    def step(self, observation_, reward, done):
        self.score += reward
        self.agent.remember(self.observation, self.action, reward, observation_, int(done))
        self.observation = observation_
        if self.n_step % 3 == 0:
            self.agent.learn()
        self.n_step += 1

    def episode_end(self):
        self.eps_history.append(self.agent.epsilon)
        self.scores.append(self.score)

        avg_score = np.mean(self.scores[max(0, self.episode-100):(self.episode+1)])
        print('episode: ', self.episode,'score: %.2f' % self.score,
                ' average score %.2f' % avg_score)
        if self.episode > 0:
            self.agent.save_model()

        self.episode += 1

