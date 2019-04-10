from reinforcementLearning import ReinforcementLearning as rLearning

def startLearning():
    rLearn = rLearning(8, 11)

    rLearn.printQValues()

    print("######################  Q-Learning  ######################")
    for trial in range(10000):
        state = rLearn.initState()
        trajectoryCount = 0
        while True:
            action = rLearn.eGreedy(state)
            nextState = rLearn.simulateMove(state, action)
            rLearn.qLearningUpdate(state, action, nextState)

            if rLearn.isATerminal(nextState):
                break
            
            state = nextState
            trajectoryCount += 1

        if(trial == 100 or trial == 1000):
                rLearn.printQValues()

if __name__ == "__main__":
    startLearning()