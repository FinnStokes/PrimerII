class Action:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def isvalid(self):
        return True

    def perform(self):
        pass
