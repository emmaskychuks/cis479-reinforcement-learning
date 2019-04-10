from reinforcementLearning import ReinforcementLearning as rLearning

def startLearning():
    rLearn = rLearning(8, 11)

    rLearn.printQValues()

    print("######################  Q-Learning  ######################")
    for trial in range(10000):
        state = rLearn.initState()
        trajectoryCount = 0
        while True:
            if rLearn.isATerminal(state):
                print("error")
            action = rLearn.eGreedy(state)
            nextState = rLearn.simulateMove(state, action)
            rLearn.qLearningUpdate(state, action, nextState)

            if rLearn.isATerminal(nextState):
                break
            
            state = nextState
            trajectoryCount += 1

        if(trial == 999 or trial == 9999):
                rLearn.printQValues()

    

if __name__ == "__main__":
    startLearning()