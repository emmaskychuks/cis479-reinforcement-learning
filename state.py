class State():
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.west = str(val)
        self.north = str(val)
        self.east = str(val)
        self.south = str(val)
        self.policy = ""

    def setValue(self, action, val):
        if action == "west":
            self.west = val
        elif action == "north":
            self.north = val
        elif action == "east":
            self.east = val
        elif action == "south":
            self.south = val    

    def getValue(self, action):
        if action == "west":
            return self.west
        elif action == "north":
            return self.north
        elif action == "east":
            return self.east
        elif action == "south":
            return self.south

    def getMaxAction(self):
        actions = []
        actions.append(float(self.west))
        actions.append(float(self.north))
        actions.append(float(self.east))
        actions.append(float(self.south))

        return max(actions)
        