from captureAgents import CaptureAgent
from captureAgents import AgentFactory
import distanceCalculator
import random, time, util
from game import Directions
import keyboardAgents
import game
from util import nearestPoint

class DJ(AgentFactory):
  def __init__(self, isRed, first='offense', second='defense', rest='offense'):
    AgentFactory.__init__(self, isRed)
    self.agents = [first, second]
    self.rest = rest

  def getAgent(self, index):
    if len(self.agents) > 0:
      return self.choose(self.agents.pop(0), index)
    else:
      return self.choose(self.rest, index)

  def choose(self, agentStr, index):
    if agentStr == 'keys':
      global NUM_KEYBOARD_AGENTS
      NUM_KEYBOARD_AGENTS += 1
      if NUM_KEYBOARD_AGENTS == 1:
        return keyboardAgents.KeyboardAgent(index)
      elif NUM_KEYBOARD_AGENTS == 2:
        return keyboardAgents.KeyboardAgent2(index)
      else:
        raise Exception('Max of two keyboard agents supported')
    elif agentStr == 'offense':
      return OffensiveAgent(index)
    elif agentStr == 'defense':
      return DefensiveAgent(index)
    else:
      raise Exception("No staff agent identified by " + agentStr)

# This is from the baselineAgent class. We did not write this!
class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveAgent(ReflexCaptureAgent):
  def chooseAction(self, gameState):
    self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] >= 1]   
    self.observe(gameState)
    
    actions = gameState.getLegalActions(self.index)

    values = [self.evaluate(gameState, a) for a in actions]
    print values
    print actions
    maxValue = max(values)
    
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)


  def evaluate(self, gameState, action):
    successor_state = self.getSuccessor(gameState, action)
    return self.evaluateState(successor_state, self.getGhostLocations())
  
  def observe(self, gameState):
    distances = gameState.getAgentDistances()
    isRed = self.red
    actual_distances = {}
    for i in range(len(distances)):
      if not isRed and i in gameState.getRedTeamIndices():
        actual_distances[i] = distances[i]
      elif isRed and i in gameState.getBlueTeamIndices():
        actual_distances[i] = distances[i]
    pos = gameState.getAgentState(self.index)
    pos = pos.getPosition()
    new_distributions = {}
    for key in actual_distances:
        new_distributions[key] = util.Counter()
        for position in self.legalPositions:
            dist = distanceCalculator.manhattanDistance(position, pos)
            new_distributions[key][position] = gameState.getDistanceProb(dist, actual_distances[key])
        
    if hasattr(self, 'distributions'): 
        for key in actual_distances:
            for entry in new_distributions[key]:
                self.distributions[key][entry] *= new_distributions[key][entry]
    else:
        self.distributions = new_distributions
    
    for key in actual_distances:
        new_d = util.Counter()
        for position in self.legalPositions:
            val = self.distributions[key][position]
            left = (position[0]-1, position[1])
            right = (position[0]+1, position[1])
            top = (position[0], position[1]-1)
            bot = (position[0], position[1]+1)
            new_d[position] += val
            if left in self.legalPositions:
                new_d[left] += val
            if right in self.legalPositions:
                new_d[right] += val
            if top in self.legalPositions:
                new_d[top] += val
            if bot in self.legalPositions:
                new_d[bot] += val
        new_d.normalize()
        self.distributions[key] = new_d

    # Printing distribution routine for debugging 
    """
    for key in self.distributions:
        best_positions = []
        best_prob = 0
        d = self.distributions[key]
        for entry in self.distributions[key]:
            if d[entry] > best_prob:
                best_prob = d[entry]
                best_positions = [entry]
            elif d[entry] == best_prob:
                best_positions.append(entry)
        predicted = random.choice(best_positions)
        print predicted
        arr = [[0 for x in range(31)] for y in range(15)]
        for element in self.distributions[key]:
            arr[element[1]][element[0]] = self.distributions[key][element]
        for r in range(15,0,-1):
            for c in range(31):
              if (c,r) == predicted:
                print '@',
              elif (c, r) in self.legalPositions:
                print '-' if arr[r][c] else ' ', 
              else:
                print "#",
            print
    """ 
    for key in self.distributions:
        allZero = True
        for entry in self.distributions[key]:
            if self.distributions[key][entry]:
                allZero = False
        if allZero:
            self.distributions = new_distributions
            return

  def getGhostLocations(self):
    ghost_states = []
    
    for dist in self.distributions:
        best_positions = []
        best_prob = 0
        d = self.distributions[dist]
        for entry in self.distributions[dist]:
            if d[entry] > best_prob:
                best_prob = d[entry]
                best_positions = [entry]
            elif d[entry] == best_prob:
                best_positions.append(entry)
        ghost_states.append(random.choice(best_positions))
    return ghost_states

  def evaluateState(self, gameState, ghostStates):  
    state = gameState
    position = state.getAgentPosition(self.index)
    foodGrid = self.getFood(state) 
    walls = state.getWalls()
    food_list = foodGrid.asList()
    distance_sum = 0
    newPos = position
   
    min_food_dist = 99999
    max_food_dist = 0
    min_ghost_dist = 99999
    max_ghost_dist = 0
    kill_score = 0
    for food in food_list:
      dx, dy = abs(food[0]-newPos[0]), abs(food[1]-newPos[1])
      #dist = dx + dy
      dist = self.distancer.getDistance(food, newPos)
      if dist < min_food_dist:
          min_food_dist = dist
      if dist > max_food_dist:
          max_food_dist = dist
    
    for state in ghostStates:
      pos = state
      dx, dy = abs(pos[0] - newPos[0]), abs(pos[1] - newPos[1])
      #dist = dx + dy
      dist = self.distancer.getDistance(pos, newPos)
      if dist < min_ghost_dist:
        min_ghost_dist = dist
      if dist > max_ghost_dist:
        max_ghost_dist = dist
    count = foodGrid.count()
    if count == 2:
      count = -2000000000 #if win, win
    if min_ghost_dist == 0:
      min_ghost_dist = .001 
    if max_ghost_dist == 0:
      max_ghost_dist = 1
    if max_food_dist == 0:
      max_food_dist = 1
    return - 2*min_food_dist \
         - 20*count \
         + 1.5/max_food_dist \
         + 1.5/max_ghost_dist \
         - 2.2/(min_ghost_dist**2) \

class DefensiveAgent(ReflexCaptureAgent):
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}


