# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    newGhostStates = successorGameState.getGhostPositions()

    "*** YOUR CODE HERE ***"
    # Min distance to food is good, distance to ghost is bad
    food_list = oldFood.asList()
    min_food_dist = 99999
    max_food_dist = 0
    min_ghost_dist = 99999
    max_ghost_dist = 0
    for food in food_list:
        dx, dy = abs(food[0]-newPos[0]), abs(food[1]-newPos[1])
        if dx + dy < min_food_dist:
            min_food_dist = dx + dy
        if dx + dy > max_food_dist:
            max_food_dist = dx + dy
    for state in newGhostStates:
        dx, dy = abs(state[0] - newPos[0]), abs(state[1] - newPos[1])
        if dx + dy < min_ghost_dist:
            min_ghost_dist = dx + dy
        if dx + dy > max_ghost_dist:
            max_ghost_dist = dx + dy
    #print min_food_dist, max_food_dist, min_ghost_dist, max_ghost_dist
    #print successorGameState.getScore()
    if min_ghost_dist == 0:
        min_ghost_dist = 1
    return successorGameState.getScore() - min_food_dist - 5/min_ghost_dist
    #return min_food_dist - 5/min_ghost_dist

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    initial_state = gameState
    target_depth = self.depth
    num_agents = gameState.getNumAgents()

    def getMax(state, agentIndex, depth):
      if depth == target_depth:
        return (self.evaluationFunction(state), Directions.STOP)
      max_val = -2000000000 
      best_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        val = getMin(newState, agentIndex + 1, depth)[0]
        if val > max_val:
          max_val = val
          best_action = action
      if max_val == -2000000000:
        max_val = self.evaluationFunction(state)
      return (max_val, best_action)

    def getMin(state, agentIndex, depth):
      min_val = 2000000000 
      worst_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        val = 0
        if agentIndex + 1 ==  num_agents:
          val = getMax(newState, 0, depth + 1)[0]
        else:
          val = getMin(newState, agentIndex + 1, depth)[0]
        if val < min_val:
          min_val = val
          worst_action = action
      if min_val == 2000000000:
        min_val = self.evaluationFunction(state)
      return (min_val, worst_action)
    
    pair = getMax(initial_state, 0, 0)
    return pair[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    initial_state = gameState
    target_depth = self.depth
    num_agents = gameState.getNumAgents()

    def getMax(state, agentIndex, depth, best_for_min):
      if depth == target_depth:
        return (self.evaluationFunction(state), Directions.STOP)
      max_val = -2000000000 
      best_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        val = getMin(newState, agentIndex + 1, depth, max_val, True)[0]
        if val > max_val:
          max_val = val
          best_action = action
        if max_val > best_for_min:
          break
      if max_val == -2000000000:
        max_val = self.evaluationFunction(state)
      return (max_val, best_action)

    def getMin(state, agentIndex, depth, best_for_max, maximizing):
      min_val = 2000000000 
      worst_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        val = 0
        if agentIndex + 1 ==  num_agents:
          val = getMax(newState, 0, depth + 1, min_val)[0]
        else:
          val = getMin(newState, agentIndex + 1, depth, min_val, False)[0]
        if val < min_val:
          min_val = val
          worst_action = action
        if maximizing:
          if min_val < best_for_max:
            break
      if min_val == 20000000000:
        min_val = self.evaluationFunction(state)
      return (min_val, worst_action)
    
    pair = getMax(initial_state, 0, 0, 2000000000)
    return pair[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    initial_state = gameState
    target_depth = self.depth
    num_agents = gameState.getNumAgents()

    def getMax(state, agentIndex, depth):
      if depth == target_depth:
        return (self.evaluationFunction(state), Directions.STOP)
      max_val = -2000000000 
      best_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        val = getMin(newState, agentIndex + 1, depth)[0]
        if val > max_val:
          max_val = val
          best_action = action
      if max_val == -200000000:
        max_val = self.evaluationFunction(state)
      return (max_val, best_action)

    def getMin(state, agentIndex, depth):
      min_val = 2000000000 
      sum = 0
      worst_action = Directions.STOP
      actionList = state.getLegalActions(agentIndex)
      for action in actionList:
        newState = state.generateSuccessor(agentIndex, action)
        if agentIndex + 1 ==  num_agents:
          sum += getMax(newState, 0, depth + 1)[0]
        else:
          sum += getMin(newState, agentIndex + 1, depth)[0]
      if sum == 0:
        return (self.evaluationFunction(state), worst_action)
      sum /= float(len(actionList))
      return (sum, worst_action)
    
    pair = getMax(initial_state, 0, 0)
    return pair[1]


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  state = currentGameState
  position = state.getPacmanPosition()
  foodGrid = state.getFood() 
  walls = state.getWalls()
  food_list = foodGrid.asList()
  # Create a minimum spanning tree with the remaining food being the nodes
  # After this the size of the tree + the distance to the closest node in the
  # MST will be our heuristic

  # Put all nodes in singleton sets in a list of sets
  #can add these to heuristic somehow. Doesn't need to eat them to win though, so just adding to food list might not be best idea.
  # Find the average distance between us and all of the ghosts
  ghostStates = state.getGhostStates()
  distance_sum = 0
  newPos = position
  #for state in ghostStates:
  #  dx, dy = abs(state[0] - newPos[0]), abs(state[1] - newPos[1])
  #  distance_sum += dx + dy

  #ghost_score = distance_sum / float(len(ghostStates))
 
  min_food_dist = 99999
  max_food_dist = 0
  min_ghost_dist = 99999
  max_ghost_dist = 0
  kill_score = 0
  for food in food_list:
      dx, dy = abs(food[0]-newPos[0]), abs(food[1]-newPos[1])
      if dx + dy < min_food_dist:
          min_food_dist = dx + dy
      if dx + dy > max_food_dist:
          max_food_dist = dx + dy
  
  for state in ghostStates:
      pos = state.getPosition()
      dx, dy = abs(pos[0] - newPos[0]), abs(pos[1] - newPos[1])
      dist = dx + dy
      if state.scaredTimer > 0:
        if dist == 0:
          kill_score += 100000
        else:  
          kill_score += 1.7*state.scaredTimer / dist
      else:
        if dist < min_ghost_dist:
          min_ghost_dist = dist
        if dist > max_ghost_dist:
          max_ghost_dist = dist
  
  # food_score = the approximate distance left to travel to eat all of the food    - We want this to decrease
  # ghost_score = the average distance between you and all of the ghosts           - We want this to be high
  # min_ghost_dist = the minimum distance between you and a ghost                  - We want this to be high
  # max_food_dist = the maximum distance to any food                               - We want this to go down
#  return 10/food_score - 0/(ghost_score*ghost_score) - 10/min_ghost_dist - 0*max_food_dist - 100*min_food_dist
  count = foodGrid.count()
  if count == 0:
    count = -2000000000 #if win, win
    #return 2000000000
  if min_ghost_dist == 0:
    min_ghost_dist = .0001 
    #return -2000000000 #Don't die pacman!
  if max_ghost_dist == 0:
    max_ghost_dist = 1
  if max_food_dist == 0:
    max_food_dist = 1
  #ghosts are either "scared" or not, so maybe have separate min/max distances for scared ghosts and not scared, and then minimize distance to scared ones instead of maximizing or something
  #i think it's ghostState.scaredTimer > 0 or somethin like that
  return - 2.2/(min_ghost_dist) \
         - 1.5*min_food_dist \
         - 20*count \
         + kill_score \
         + 1.5/max_food_dist \
         - 1.5/max_ghost_dist \
         + currentGameState.getScore() \
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


