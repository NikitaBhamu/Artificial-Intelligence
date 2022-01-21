# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
         remaining food (newFood) and Pacman position after moving (newPos).
         newScaredTimes holds the number of moves that each ghost will remain
         scared because of Pacman having eaten a power pellet.

         Print out these variables to see what you're getting, then combine them
         to create a masterful evaluation function.
         """
         
         successorGameState = currentGameState.generatePacmanSuccessor(action)
         newPos = successorGameState.getPacmanPosition()
         #print(newPos)
         #position is basically coordinates
         newFood = successorGameState.getFood()
         newGhostStates = successorGameState.getGhostStates()
         newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
         "*** YOUR CODE HERE ***"
         #print("ghostposition")
         foodlist = newFood.asList(key=True)
         ghostPosition = successorGameState.getGhostPositions()
         value = 0
         mindist = 100000
         for food in foodlist:
            distfood = util.manhattanDistance(newPos ,food)
            if (distfood < mindist) :
               mindist = distfood
               
         if(mindist > 0):
           value = 1*(1/mindist)
         else:
           value = 1.1
         
         distghost = 999999
         for ghost in ghostPosition:
            dist = util.manhattanDistance(newPos ,ghost)
            if(dist < distghost):
               distghost = dist
         
         if(distghost <= 3 and distghost > 0):
           value = -4*(1/distghost)
         elif(distghost == 0):
           value = -4.5
         
         #print(ghostPosition[0])
         #print(successorGameState.getScore())
         Capsule = successorGameState.getCapsules()
         num = len(Capsule)
         
         return successorGameState.getScore()+value-(1.2)*num
    
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
    def minmax(self,gameState,agentIndex,depth,deep):
         if(depth == deep ):
            return self.evaluationFunction(gameState), None
         else:
            if(agentIndex == gameState.getNumAgents()):
                agentIndex = 0
                
            if(agentIndex==0): #it is a pacman
               actions = gameState.getLegalActions(agentIndex)
               Max = -999999
               act = None
               for action in actions:
                  succ = gameState.generateSuccessor(agentIndex, action)
                  value,_ = self.minmax(succ,agentIndex+1,depth+1,deep)
                  if(value > Max):
                     Max = value
                     act = action
               
               if(Max == -999999): Max = self.evaluationFunction(gameState)
               return Max,act
               
            else: #middle ghost
               actions = gameState.getLegalActions(agentIndex)
               Min = 999999
               act = None
               for action in actions:
                  succ = gameState.generateSuccessor(agentIndex, action)
                  value,_ = self.minmax(succ,agentIndex+1,depth+1,deep)
                  if(value < Min):
                     Min = value
                     act = action
                     
               if(Min == 999999):  Min = self.evaluationFunction(gameState)
               return Min,act
        
    
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
  
        if(gameState.isWin()):
            print("Pacman Won")
            return None
        elif(gameState.isLose()):
            print("Pacman Lost")
            return None
        else:
            deep = self.depth * gameState.getNumAgents()
            value,action = self.minmax(gameState,0,0,deep)
            return action
           
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabetaprune(self,gameState,agentIndex,depth,deep,alpha,beta):
     if(depth == deep or alpha > beta):
        return self.evaluationFunction(gameState), None
     else:
        if(agentIndex == gameState.getNumAgents()):
            agentIndex = 0
            
        if(agentIndex==0): #it is a pacman
           actions = gameState.getLegalActions(agentIndex)
           Max = -999999
           act = None
           for action in actions:
              succ = gameState.generateSuccessor(agentIndex, action)
              value,_ = self.alphabetaprune(succ,agentIndex+1,depth+1,deep,alpha,beta)
              if(value > Max):
                 Max = value
                 act = action
                 if(value > alpha):
                    alpha = value
              if (alpha > beta):
                 break
           
        
           if(Max == -999999): Max = self.evaluationFunction(gameState)
           return Max,act
           
        else: #middle ghost
           actions = gameState.getLegalActions(agentIndex)
           Min = 999999
           act = None
           for action in actions:
              succ = gameState.generateSuccessor(agentIndex, action)
              value,_ = self.alphabetaprune(succ,agentIndex+1,depth+1,deep,alpha,beta)
              if(value < Min):
                 Min = value
                 act = action
                 if(value < beta):
                    beta = value
              if (alpha > beta):
                 break
           
           if(Min == 999999):  Min = self.evaluationFunction(gameState)
           return Min,act

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        if(gameState.isWin()):
           print("Pacman Won")
           return None
        elif(gameState.isLose()):
           print("Pacman Lost")
           return None
        else:
           alpha = -999999
           beta = 999999
           deep = self.depth * gameState.getNumAgents()
           value,action = self.alphabetaprune(gameState,0,0,deep,alpha,beta)
           return action
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectimax(self,gameState,agentIndex,depth,deep):
        if(depth == deep):
           return self.evaluationFunction(gameState), None
        else:
           if(agentIndex == gameState.getNumAgents()):
               agentIndex = 0
               
           if(agentIndex==0): #it is a pacman
              actions = gameState.getLegalActions(agentIndex)
              Max = -999999
              act = None
              for action in actions:
                 succ = gameState.generateSuccessor(agentIndex, action)
                 value,_ = self.expectimax(succ,agentIndex+1,depth+1,deep)
                 if(value > Max):
                    Max = value
                    act = action
              
              if(Max == -999999): Max = self.evaluationFunction(gameState)
              return Max,act
              
           else: #middle ghost
              avg = None
              act = None
              actions = gameState.getLegalActions(agentIndex)
              num = len(actions)
              if(num==0):
                 prob = 0.0
              else:
                 prob = 1.0/num
              for action in actions:
                  succ = gameState.generateSuccessor(agentIndex, action)
                  value,_ = self.expectimax(succ, agentIndex + 1, depth+1,deep)
                  if avg is None:
                     avg = 0.0
                  avg += prob * value
                  act = action
            
              if avg is None:
                return self.evaluationFunction(gameState),None
              return avg, act
      
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        if(gameState.isWin()):
            print("Pacman Won")
            return None
        elif(gameState.isLose()):
            print("Pacman Lost")
            return None
        else:
            deep = self.depth * gameState.getNumAgents()
            value,action = self.expectimax(gameState,0,0,deep)
            return action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    In this evaluation function, the parameters which play a role are :
    1. The distance of the food from the pacman's position
    2. The distance of the ghost from the pacman's position
    3. The number of the capsules still not eaten in the present state
    So in my code the factor decreasing the value of a state most is when the ghost are so close to the present position of pacman,so it basically adds negative value to the score of the state and that magnitude of negative value is high. The ghost which are under the manhattan distance of 2 are considered to be the ones effecting the next step of the pacman, in this the ghost with the minimum dstance with the pacman position is taken into consideration.
    And the dependency on the food is such that if distance of the nearest food item is >0, then it depends on the inverse of the distance of the food and when it is zero then a value of 1.5 adds to the score of the state.
    And as the number of capsule increases in a state, the score of a state decreases.
    Even if the food is very nearer to the present pacman position, still the effect of the ghost if it very nearer to the present position will be considered for evaluating the score of the state.
    """
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostPosition = currentGameState.getGhostPositions()
    foodlist = newFood.asList(key=True)
    
    value = 0
    mindist = 100000
    for food in foodlist:
       distfood = util.manhattanDistance(newPos ,food)
       if (distfood < mindist) :
          mindist = distfood
          
    if(mindist > 0):
      value = 1*(1/mindist)
    else:
      value = 1.3
    
    distghost = 999999
    for ghost in ghostPosition:
       dist = util.manhattanDistance(newPos ,ghost)
       if(dist < distghost):
          distghost = dist
    
    if(distghost <= 2 and distghost > 0):
      value = -3*(1/distghost)
    elif(distghost == 0):
      value = -4
    
    Capsule = currentGameState.getCapsules()
    num = len(Capsule)
    
    return currentGameState.getScore()+value-(1.4)*num
    
    
    "*** YOUR CODE HERE ***"

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
