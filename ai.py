from dqn import Agent


class AI:
    def __init__(self, fname):
        lr = 0.0005
        self.agent = Agent(gamma=0.99, epsilon=0.0, alpha=lr, input_dims=6,
                  n_actions=2, mem_size=60000, batch_size=64, epsilon_end=0.0, fname=fname)
        self.observation = []
        self.action = 0
        self.n_step = 0
        self.fname = fname.split("/")[-1]

    def episode_start(self, observation):
        self.observation = observation

    def choose_action(self):
        self.action = self.agent.choose_action(self.observation)
        return self.action

    def step(self, observation_, reward, done):
        self.agent.remember(self.observation, self.action, reward, observation_, int(done))
        self.observation = observation_
        if self.n_step % 3 == 0:
            self.agent.learn()
        self.n_step += 1

    def episode_end(self):
        self.agent.save_model()

