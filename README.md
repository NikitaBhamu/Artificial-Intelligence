# Artificial-Intelligence

## A1 :  Search
Implemented the following search algorithms :-
1. Depth First Search (DFS)
2. Breadth First Search (BFS)
3. Uniform Cost Search (UCS)
4. A* Search

Then designed the appropriate heuristics for the A* search algorithm for two different problems which are :
1. In this part the agent lives in a corner maze, where there are four dots, one in each corner. The agent’s goal is to find the shortest path through the maze such that it visits all the corners, irrespective of whether there is food present at that maze location or not.
2. This part involves solving the food clearing problem. The goal is to search for the shortest path for the Pacman to collect all the food available in the maze. Note that the solution should depend only on the agent’s state, wall placement and regular food.

## A2 : Multi-Agent Search
This assignment involves enabling the Pacman agent to act appropriately in the game where there are ghosts in the world. The Pacman still aims at eating all the dots but must plan its action taking the behaviour of the ghosts into account. This exercise will involve modeling the decision-making task as an adversarial search problem that allows the Pacman to decide actions while taking into account the behaviour of ghosts.

Implemented the following adversarial search algorithms :-
1. Minimax
2. Alpha-Beta Pruning 
3. Expectimax

Also implemented better evaluation functions to make the agent play better.

## A3 : Decision making for teams
Implemented the basic model of decision making for the team tries to safeguard its resources (food pellets) and tries to capture resources held by the other team.
