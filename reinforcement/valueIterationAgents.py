# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    # for storing the policy:
    self.policy = util.Counter()

    # for storing the Q values:
    self.Q_values = util.Counter()

    all_states = mdp.getStates()
    for i in range(iterations):
        new_values = util.Counter()
        for state in all_states:
            if mdp.isTerminal(state):
                continue
            actions = mdp.getPossibleActions(state)
            max = -2000000000
            for action in actions:
                sum = 0
                states = mdp.getTransitionStatesAndProbs(state, action)
                for state_pair in states:
                    sum += state_pair[1]*(mdp.getReward(state, action, state_pair[0]) + discount*self.values[state_pair[0]])
                if sum > max:
                    max = sum
            new_values[state] = max
        self.values = new_values;

    # Calculate best policy
    for state in all_states:
        if mdp.isTerminal(state):
            continue
        best = None
        max = -2000000000
        actions = mdp.getPossibleActions(state)
        for action in actions:
            new_states = mdp.getTransitionStatesAndProbs(state, action)
            sum = 0
            for state_pair in new_states:
                sum += state_pair[1]*self.values[state_pair[0]]
            if sum > max:
                max = sum
                best = action
        self.policy[state] = best

    # Calculate all Q Values (Q Value iteration)
    for i in range(iterations):
        new_q_values = util.Counter()
        for state in all_states:
            if mdp.isTerminal(state):
                continue
            actions = mdp.getPossibleActions(state)
            for action in actions:
                states = mdp.getTransitionStatesAndProbs(state, action)
                sum = 0
                for state_pair in states:
                    new_actions = mdp.getPossibleActions(state_pair[0])
                    max_action = -2000000000
                    if len(new_actions) == 0:
                        max_action = 0
                    for a in new_actions:
                        v = self.Q_values[(state_pair[0], a)]
                        if v > max_action:
                            max_action = v
                    sum += state_pair[1] * (mdp.getReward(state, action, state_pair[0]) + discount*max_action)
                new_q_values[(state, action)] = sum
        self.Q_values = new_q_values
         
    
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    return self.Q_values[(state,action)]

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    return self.policy[state]

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
