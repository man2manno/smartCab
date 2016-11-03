import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.successes = []
        self.Q = {}
        self.time = 0.0
        self.alpha = 1.0
        self.gamma = 0.9
        self.eplison = 1.0
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
	self.state = (inputs['light'], self.next_waypoint, inputs['left'], inputs['oncoming'])
        
        # TODO: Select action according to your policy
        #action = random.choice([None,'forward','left','right'])

	actions = [None,'left','right','forward']
	if self.state not in self.Q.keys():
		actions_dict = {}
		for a in actions:
			actions_dict[a] = 0.0
		self.Q[self.state] = actions_dict
    
        # Implement Choose best action here, reward comes after
        def choose_best_action(self,state):
            # Find max value for all actions
            maxQ = max(self.Q[state].values())
            count = self.Q[state].values().count(maxQ)
            rand = random.random()
            if rand < self.eplison:
                best_action = random.choice([None,'left','right','forward'])
            elif count > 1 and rand >= self.eplison:
                # Choose randomly between best actions
                options = [i for i in self.Q[state].keys() if self.Q[state][i] == maxQ]
                best_action = random.choice(options)
            else:
                best_action = max(self.Q[state], key=self.Q[state].get)

            return best_action

        action = choose_best_action(self,self.state)
	
        """
        if (self.state[0] == 'red' and (self.state[1] == 'forward' or self.state[1] == 'left')) or \
                (self.state[0] == 'red' and self.state[1] == 'right' and self.state[2] == 'forward') or \
                (self.state[0] == 'green' and self.state[1] == 'left' and self.state[3] == 'forward') or \
                (self.state[0] == 'green' and self.state[1] == 'left' and self.state[3] == 'right'):
            action = None
        else:
            action = self.state[1]
        """
        # Execute action and get reward
        reward = self.env.act(self, action)
        # Check if destination was reached
        _location = self.env.agent_states[self]["location"]
        _destination = self.env.agent_states[self]["destination"]
        if _location == _destination:
            self.successes.append(True)
            print len(self.successes)/100.0 * 100.0

        # TODO: Learn policy based on state, action, reward
        # Update Learning Decay Rate -- Alpha
        self.time += 1.0
        self.alpha = 1.0 / math.log(self.time + 1)
        self.eplison = 1.0 / self.time
        if self.alpha > 1.0:
            self.alpha = 1.0
   
	# Updated Q-Table
	self.Q[self.state][action] = (1 - self.alpha) * self.Q[self.state][action] + self.alpha*(reward + self.gamma * max(self.Q[self.state].values()))
        #print self.Q[self.state].values()

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.1, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
