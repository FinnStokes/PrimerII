class Action:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def isvalid(self, player):
        return True

    def perform(self, player):
        pass

    def first_perform(self, player):
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

class Take(Action):
    def __init__(self, name, cost, item, tm):
        Action.__init__(self, name, cost)
        self.item = item
        self.tm = tm

    def isvalid(self, player):
        room = self.tm.players[player].room
        return not self.tm.inventories[player].isfull() and self.item in room.items

    def perform(self, player):
        room = self.tm.players[player].room
        room.items.remove(self.item)
        self.tm.inventories[player].addItem(self.item)

class Drop(Action):
    def __init__(self, name, cost, item, tm):
        Action.__init__(self, name, cost)
        self.item = item
        self.tm = tm

    def isvalid(self, player):
        return self.item in self.tm.inventories[player].items

    def perform(self, player):
        self.tm.inventories[player].popItem(self.item)
        self.tm.players[player].room.items.append(self.item)

class TimeTravel(Action):
    def __init__(self, name, cost, time, timeline, tm):
        Action.__init__(self, name, cost)
        self.time = time
        self.timeline = timeline
        self.tm = tm
        self.incentory = []

    def isvalid(self, player):
        return self.tm.map.get_rift(self.timeline)

    def perform(self, player):
        self.tm.timelines[player].active = False
        self.tm.map.set_rift(self.timeline, False)
        if self.inventory != sorted(self.tm.inventories[player].items):
            print("Error in time travel: incorrect inventory")
    
    def first_perform(self, player):
        inventory = self.tm.inventories[player].items
        self.tm.seek(self.time)
        self.tm.insert(self.timeline)
        self.tm.inventories[self.timeline].initial = list(inventory)
        self.tm.inventories[self.timeline].reset()
        self.inventory = sorted(inventory)
