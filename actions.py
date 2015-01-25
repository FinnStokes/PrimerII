class Action:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def isvalid(self, player):
        return True

    def perform(self, player):
        pass

class Move(Action):
    def __init__(self, name, cost, fromRoom, toRoom, tm):
        Action.__init__(self, name, cost)
        self.fromRoom = fromRoom
        self.toRoom = toRoom
        self.tm = tm

    def isvalid(self, player):
        return self.tm.players[player].room == self.fromRoom

    def perform(self, player):
        self.tm.players[player].room = self.toRoom
