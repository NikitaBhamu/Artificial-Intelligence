# myTeam.py
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


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffendingAgent', second = 'DefendingAgent'):
      """
      This function should return a list of two agents that will form the
      team, initialized using firstIndex and secondIndex as their agent
      index numbers.  isRed is True if the red team is being created, and
      will be False if the blue team is being created.

      As a potentially helpful development aid, this function can take
      additional string-valued keyword arguments ("first" and "second" are
      such arguments in the case of this function), which will come from
      the --redOpts and --blueOpts command-line arguments to capture.py.
      For the nightly contest, however, your team will be created without
      any extra arguments, so you should make sure that the default
      behavior is what you want for the nightly contest.
      """

      # The following line is an example only; feel free to change it.
      return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):

   def registerInitialState(self, gameState):
    
      CaptureAgent.registerInitialState(self, gameState)
      
      
   def chooseAction(self, gameState):
    
      actions = gameState.getLegalActions(self.index)
     
      if(len(actions) > 0):
         score = []
         for a in actions:
            score.append(self.ScoreCalc(gameState,a))
      
         i = 0
         if (len(score) >= 2):
              max = -20
              for j in range(1,len(score)):
                 if(score[j] > max):
                    i = j
                    max = score[j]
         elif(len(score) == 1):
              max = score[0]
        
         return actions[i]
          
      else:
         return None
   
   def getSuccessor(self, gameState, action):
      successor = gameState.generateSuccessor(self.index, action)
      pos = successor.getAgentState(self.index).getPosition()
      if pos != nearestPoint(pos):
         # Only half a grid position was covered
        return successor.generateSuccessor(self.index, action)
      else:
        return successor
    
   def ScoreCalc(self, gameState, action):
      return gameState.getScore()

    
class DefendingAgent(DummyAgent):

   def ScoreCalc(self, gameState, action):
   
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()
      opponents_index = self.getOpponents(successor)
      
      opponent_state = []
      for i in opponents_index:
          opponent_state.append(successor.getAgentState(i))
      
      opponent_pos = []
      for s in opponent_state:
          opponent_pos.append(s.getPosition())
      
      invaders_state = []
      for aa in opponent_state:
          if (aa.isPacman):
              invaders_state.append(aa)
          
      invaders_pos = []
      for ii in invaders_state:
          invaders_pos.append(ii.getPosition())
      

      mindist = 100000
      if (len(invaders_pos) > 0):
          for i in invaders_pos:
             d = util.manhattanDistance(myPos ,i)
             if ( d < mindist):
                 mindist = d
      else:
          mindist = -1
         
      foodimdefending = self.getFoodYouAreDefending(successor)
      foodlist = foodimdefending.asList(key=True)
      
      minfood = 100000
      if (len(foodlist) >0 ):
          for food in foodlist:
             distfood = util.manhattanDistance(myPos ,food)
             if (distfood < minfood) :
                minfood = distfood
      else:
          minfood = -100
      
      if mindist > 0:
         return successor.getScore() + (1/mindist)*200
      else:
         return successor.getScore()
        
    
class OffendingAgent(DummyAgent):

   def ScoreCalc(self, gameState, action):
     
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)
      myPos = myState.getPosition()
      opponents_index = self.getOpponents(successor)
   
      newFood = self.getFood(successor)
      foodlist = newFood.asList(key=True)
      
      minfood = 100000
      if (len(foodlist) >0 ):
          for food in foodlist:
             distfood = util.manhattanDistance(myPos ,food)
             if (distfood < minfood) :
                minfood = distfood
      else:
          minfood = -1
      
      opponent_state = []
      for i in opponents_index:
          opponent_state.append(successor.getAgentState(i))
      
      opponent_pos = []
      for s in opponent_state:
          opponent_pos.append(s.getPosition())
      
      defenders_state = []
      for aa in opponent_state:
          if (not aa.isPacman):
              defenders_state.append(aa)
          
      defenders_pos = []
      for ii in defenders_state:
          defenders_pos.append(ii.getPosition())
    
      defend_min = 100000
      if(len(defenders_pos) >0):
         for d in defenders_pos:
            dist = util.manhattanDistance(myPos ,d)
            if( dist < defend_min):
               defend_min = dist
      else:
         defend_min = 1
         
      Capsule = successor.getCapsules()
      num = len(Capsule)
      
      if( len(defenders_pos) > 0 and defend_min >= 3 and defend_min <= 20):
          return successor.getScore()+ 10*defend_min + (1/minfood)*20
      elif(len(defenders_pos) > 0 and defend_min <= 3):
          return successor.getScore()- 1000 + (1/minfood)*20
      elif(len(defenders_pos) > 0 ):
          return successor.getScore()+ 100 + (1/minfood)*20
      else:
          return successor.getScore()+ 100 + (1/minfood)*20
    


