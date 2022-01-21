# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """
    REVERSE_PUSH = False

    @staticmethod
    def reverse_push():
        SearchProblem.REVERSE_PUSH = not SearchProblem.REVERSE_PUSH

    @staticmethod
    def print_push():
        print(SearchProblem.REVERSE_PUSH)

    @staticmethod
    def get_push():
        return SearchProblem.REVERSE_PUSH

    def get_expanded(self):
        return self.__expanded

    def inc_expanded(self):
        self.__expanded+=1

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    print ("Start:", problem.getStartState())
    print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print ("Start's successors:", problem.getSuccessors(problem.getStartState()))
    print("The goal is: ", problem.getGoal())
   """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    visited = []
    stack = util.Stack()
    action = []
    stack.push([problem.getStartState(), action])

    while(not stack.isEmpty()):
        state_action = stack.pop()
        state = state_action[0]
        action = state_action[1]
        visited.append(state)

        if (problem.isGoalState(state)) :
                return action
        else:
           successors = problem.getSuccessors(state)
           for x in successors:
              if (x[0] not in visited):
                stack.push([x[0],action+[x[1]]])

    return action

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    visited = []
    queue = util.Queue()
    action = []
    queue.push([problem.getStartState(), action])

    while(not queue.isEmpty()):
        state_action = queue.pop()
        state = state_action[0]
        action = state_action[1]

        if (problem.isGoalState(state)) :
                return action
        elif(state not in visited):
           visited.append(state)
           successors = problem.getSuccessors(state)
           for x in successors:
              if (x[0] not in visited):
                    queue.push([x[0],action+[x[1]]])
        else: pass
    return action

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    import heapq
    visited = []
    prior_queue = util.PriorityQueue()
    action = []

    prior_queue.push([problem.getStartState(),action],0)

    while( not prior_queue.isEmpty()):
       (pathCost,_,state_action) = heapq.heappop(prior_queue.heap)
       state = state_action[0]
       action = state_action[1]

       if (problem.isGoalState(state)) :
           return action
       elif (state not in visited):
           visited.append(state)
           successors = problem.getSuccessors(state)
           for x in successors:
              if (x[0] not in visited):
                prior_queue.update([x[0],action+[x[1]]], pathCost+x[2])
       else: pass
    return action
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"


    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    import heapq
    visited = []
    prior_queue = util.PriorityQueue()
    action = []

    prior_queue.push([problem.getStartState(),action,0],0)

    while( not prior_queue.isEmpty()):
       (totalValue,_,state_action) = heapq.heappop(prior_queue.heap)
       state = state_action[0]
       action = state_action[1]
       pathCost = state_action[2]

       if (problem.isGoalState(state)) :
           return action
       elif (state not in visited):
           visited.append(state)
           successors = problem.getSuccessors(state)
           for x in successors:
              if (x[0] not in visited):
                prior_queue.update([x[0],action+[x[1]],pathCost+x[2]], pathCost+x[2]+heuristic(x[0],problem))
       else: pass
    return action
    util.raiseNotDefined()
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
reverse_push=SearchProblem.reverse_push
print_push=SearchProblem.print_push

