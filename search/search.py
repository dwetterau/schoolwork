# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  print s
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
 
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  
  """
  "*** YOUR CODE HERE ***"  
  best_cost = [2000000000]        # Worst possible?
  best_actions = []
  actions = []                    # Holds current list of actions
  visited = []                    # Nodes that have been visited
  if problem.isGoalState(problem.getStartState()):
    return actions
  # initial setup  
  stack = util.Stack()
  for succ in problem.getSuccessors(problem.getStartState()):
    stack.push(succ)
  visited.append(problem.getStartState())
  def depthFirstHelper():
    next = stack.pop()
    if next[0] in visited and not problem.isGoalState(next[0]):
      return
    visited.append(next[0])
    actions.append(next[1])
    if problem.isGoalState(next[0]):
      cost = problem.getCostOfActions(actions)
      if cost < best_cost[0]:
        del best_actions[:]          # Clear the old best list
        for o in actions:
          best_actions.append(o)
        best_cost[0] = cost
    else:
      # call the method recursively on all successors
      for succ in problem.getSuccessors(next[0]):
        stack.push(succ)
      for succ in problem.getSuccessors(next[0]):
        depthFirstHelper()
      # After processing all children, return
      actions.pop()
  while not stack.isEmpty():
    depthFirstHelper()  # call the helper method initially
  return best_actions

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  backtrackmap = {}
  actions = []
  queue = util.Queue()
  queue.push(problem.getStartState())

  backtrackmap[problem.getStartState()] = []   

  endpoint = None
  while not queue.isEmpty():
    cur = queue.pop()
    if problem.isGoalState(cur):
      endpoint = cur
      break
    previous_path = backtrackmap[cur]
    for succ_tuple in problem.getSuccessors(cur):
      succ = succ_tuple[0]
      if succ not in backtrackmap:
        list = []
        for ele in previous_path:
          list.append(ele)
        list.append(succ_tuple[1])
        backtrackmap[succ] = list
        queue.push(succ)
    # Erase previous list to save some space
    # The map will only store paths to the fringe
    backtrackmap[cur] = []
  return backtrackmap[endpoint]

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  backtrackmap = {}
  costmap = {}
  actions = []
  queue = util.PriorityQueue()
  queue.push(problem.getStartState(),0)

  backtrackmap[problem.getStartState()] = []   
  costmap[problem.getStartState()] = 0 
  visited = set()
  
  endpoint = None
  while not queue.isEmpty():
    cur = queue.pop()
    if problem.isGoalState(cur):
      endpoint = cur
      break;
    visited.add(cur)
    previous_path = backtrackmap[cur]
    old_cost = costmap[cur]
    for succ_tuple in problem.getSuccessors(cur):
      succ = succ_tuple[0]
      if succ not in visited:
        list = []
        for ele in previous_path:
          list.append(ele)
        list.append(succ_tuple[1])
        cost = succ_tuple[2] + old_cost
        if (not succ in costmap) or cost < costmap[succ]:
          backtrackmap[succ] = list
          costmap[succ] = cost
          queue.push(succ, cost)
    # Erase previous list to save some space
    # The map will only store paths to the fringe
    backtrackmap[cur] = []
  return backtrackmap[endpoint]
 
 
def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  backtrackmap = {}
  costmap = {}
  actions = []
  queue = util.PriorityQueue()

  backtrackmap[problem.getStartState()] = []   
  costmap[problem.getStartState()] = heuristic(problem.getStartState(), problem)
  queue.push(problem.getStartState(),heuristic(problem.getStartState(), problem))
  visited = set()
  
  endpoint = None
  while not queue.isEmpty():
    cur = queue.pop()
    if problem.isGoalState(cur):
      endpoint = cur
      break;
    visited.add(cur)
    previous_path = backtrackmap[cur]
    old_cost = costmap[cur]
    for succ_tuple in problem.getSuccessors(cur):
      succ = succ_tuple[0]
      if succ not in visited:
        cost = succ_tuple[2] + old_cost
        if (not succ in costmap) or cost < costmap[succ]:
          costmap[succ] = cost
          cost = succ_tuple[2] + old_cost + heuristic(succ, problem)
          list = []
          for ele in previous_path:
            list.append(ele)
          list.append(succ_tuple[1])
          backtrackmap[succ] = list
          queue.push(succ, cost)
    # Erase previous list to save some space
    # The map will only store paths to the fringe
    backtrackmap[cur] = []
  return backtrackmap[endpoint]
 
  
  """backtrackmap = {}
  actions = []
  queue = util.PriorityQueue()
  queue.push(problem.getStartState(), 0)

  backtrackmap[problem.getStartState()] = []   
  
  endpoint = None
  while not queue.isEmpty():
    cur = queue.pop()
    if problem.isGoalState(cur):
      endpoint = cur
      break;
    previous_path = backtrackmap[cur]
    for succ_tuple in problem.getSuccessors(cur):
      succ = succ_tuple[0]
      if succ not in backtrackmap:
        list = []
        for ele in previous_path:
          list.append(ele)
        list.append(succ_tuple[1])
        backtrackmap[succ] = list
        queue.push(succ, succ_tuple[2] + heuristic(succ, problem))
    # Erase previous list to save some space
    # The map will only store paths to the fringe
    backtrackmap[cur] = [0]
  print backtrackmap[endpoint]
  return backtrackmap[endpoint]"""
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
