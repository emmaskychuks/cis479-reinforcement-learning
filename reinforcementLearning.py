import numpy as np
import random
from state import State

class ReinforcementLearning():
    def __init__(self, envHeight, envWidth):
        self.envHeight = envHeight
        self.envWidth = envWidth
        self.qValues = [[State(x, y, 0.0) for y in range(envWidth)] for x in range(envHeight)] # Q value matrix
        self.freqAccessValues = [[State(x, y, 0) for y in range(envWidth)] for x in range(envHeight)] # Access Frequency
        self.rewards = {"west": -2, "north": -1, "east": -2, "south": -3} # Reward Matrix
        self.obstacles = [(4, 3), (4, 4), (3, 4), (2, 4), (5, 6), (5, 7), (2, 5), (2, 6), (2, 7), (4, 7), (3, 7)] # Obstacles in the environment
        self.goalState = (0, 10) # Goal state
        self.discountRate = 0.90
        self.assignObstacleValue()
        self.assignGoalValues()

    def initState(self):
        x = random.randint(0, self.envHeight - 1)
        y = random.randint(0, self.envWidth - 1)

        #If it's an obstacle or a terminal state
        while not self.isNotAnObstacle((x, y)) or self.isATerminal(self.qValues[x][y]):
            x = random.randint(0, self.envHeight - 1)
            y = random.randint(0, self.envWidth - 1)

        return self.qValues[x][y]

    def assignGoalValues(self):
        x, y = self.goalState

        self.qValues[x][y].west = str(50.0)
        self.qValues[x][y].north = str(50.0)
        self.qValues[x][y].east = str(50.0)
        self.qValues[x][y].south = str(50.0)

        self.qValues[x][y].policy = "GGGG"

    def assignObstacleValue(self):

        for x in range(0, self.envHeight):
            for y in range(0, self.envWidth):
                if not self.isNotAnObstacle((x, y)):
                    self.qValues[x][y].west = "####"
                    self.qValues[x][y].north = "####"
                    self.qValues[x][y].east = "####"
                    self.qValues[x][y].south = "####"

                    self.freqAccessValues[x][y].west = "####"
                    self.freqAccessValues[x][y].north = "####"
                    self.freqAccessValues[x][y].east = "####"
                    self.freqAccessValues[x][y].south = "####"


    def isNotAnObstacle(self, coordinate):
        if coordinate in self.obstacles:
            return False
        else:
            return True

    def isWithinBoundary(self, coordinate):
        x, y = coordinate
        # Check if a node is within the boundary of the map
        if (x >= 0 and x < self.envHeight) and (y >= 0 and y < self.envWidth):
            return True
        else:
            return False
    
    def isATerminal(self, state):
        x, y = state.x, state.y
        goalX, goalY = self.goalState
        if x == goalX and y == goalY:
            return True
        else:
            return False

    def printQValues(self):
        print(" Q-Values")
        print("")
        for x in range(0, self.envHeight):
            row = self.qValues[x]
            width = 15

            print(''.join('{0:15}'.format("   " + state.north + "    ", width=width) + "   " for state in row))
            print(''.join('{0:15}'.format(state.west + "   " + state.east, width=width) + "   " for state in row))
            print(''.join('{0:15}'.format("   " + state.south + "    ", width=width) + "   " for state in row))
            print(" ")
            
    def printNValues(self):
        print(" N-Values")
        for x in range(0, self.envHeight):
            row = self.freqAccessValues[x]
            width = 15

            print(''.join('{0:15}'.format("   " + state.north + "    ", width=width) + "   " for state in row))
            print(''.join('{0:15}'.format(state.west + "   " + state.east, width=width) + "   " for state in row))
            print(''.join('{0:15}'.format("   " + state.south + "    ", width=width) + "   " for state in row))
            print(" ")

    def printOptimalActions(self):
        pass

    def eGreedy(self, state):
        possibleActions = []
        actionsMap = {}
        actionsMap = {0: "west", 1: "north", 2: "east", 3: "south"}

        e = 0.05

        possibleActions.append((0, float(state.west)))
        possibleActions.append((1, float(state.north)))
        possibleActions.append((2, float(state.east)))
        possibleActions.append((3, float(state.south)))

        optimalActions = self.findLocalOptimals(possibleActions)

        greedyAction = random.choices([random.choice(optimalActions), random.choice(possibleActions)], weights=[1-e, e], k=1)

        return actionsMap[greedyAction[0][0]] 
    

    def findLocalOptimals(self, variants):
        maxVariant = max([x[1] for x in variants])
        variants = [x for x in variants if x[1] == maxVariant]

        return variants

    def simulateMove(self, state, action):
        x, y = state.x, state.y
        possibleStates = []
        variantProb = []

        if action == "north":
            possibleStates, variantProb = self.simulateTransition((x, y), (x - 1, y), (x, y - 1), (x, y + 1))
        elif action == "east":
            possibleStates, variantProb = self.simulateTransition((x, y), (x, y + 1), (x - 1, y), (x + 1, y))
        elif action == "west":
            possibleStates, variantProb = self.simulateTransition((x, y), (x, y - 1), (x + 1, y), (x - 1, y))
        elif action == "south":
            possibleStates, variantProb = self.simulateTransition((x, y), (x + 1, y), (x, y + 1), (x, y - 1))

        nextState = random.choices(population=possibleStates, weights=variantProb, k=1)

        return nextState[0]
           

    def simulateTransition(self, currentCoordinate, forwardCoordinate, leftDriftCordinate, rightDriftCoordinate):
        possibleStates = []
        variantProb = []
        totalProbability = 0.00
        
        x, y = forwardCoordinate
        if self.isWithinBoundary((x, y)):
            if self.isNotAnObstacle((x, y)):
                possibleStates.append(self.qValues[x][y])
                totalProbability += 0.80
                variantProb.append(0.80)

        x, y = leftDriftCordinate
        if self.isWithinBoundary((x, y)):
            if self.isNotAnObstacle((x, y)):
                possibleStates.append(self.qValues[x][y])
                totalProbability += 0.10
                variantProb.append(0.10)

        x, y = rightDriftCoordinate
        if self.isWithinBoundary((x, y)):
            if self.isNotAnObstacle((x, y)):
                possibleStates.append(self.qValues[x][y])
                totalProbability += 0.10
                variantProb.append(0.10)

        x, y = currentCoordinate
        # probability the robot bounced back to current position
        if totalProbability < 1.0:
            possibleStates.append(self.qValues[x][y])
            variantProb.append(1.0 - totalProbability)

        return possibleStates, variantProb


    def qLearningUpdate(self, state, action, nextState):
        x, y = state.x, state.y
        freqAccessState = self.freqAccessValues[x][y]
        qValueState = self.qValues[x][y]
       
        freqAccessState.setValue(action, str(int(freqAccessState.getValue(action)) + 1))
        #Q-learning Function
        qValue = str(round(1 / int(freqAccessState.getValue(action)) * 
                (self.rewards[action] + self.discountRate * (nextState.getMaxAction()) - float(qValueState.getValue(action))), 1))
        qValueState.setValue(action, qValue)
        

    def sasaLearningUpdate(self, s, ss):
        pass