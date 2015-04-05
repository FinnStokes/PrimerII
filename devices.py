import actions

class Device:
    def __init__(self, data, room, tm):
        self.name = data['name']
        self.room = room
        self.initial_state = data.get('state')
        self.state = self.initial_state
        self.functions = [Activate(func, self, tm) for func in data.get('functions', [])]

    def reset(self):
        self.state = self.initial_state

class Activate(actions.Action):
    def __init__(self, data, device, tm):
        actions.Action.__init__(self, data['name'], data['cost'])
        self.effects = [Effect(r, device, tm) for r in data.get('effects', [])]
        self.prerequisites = [construct_prerequisite(p, tm, room=device.room.name, device=device.name) for p in data.get('prerequisites', [])]
        self.device = device
        self.tm = tm

    def isvalid(self, player):
        return self.tm.players[player].room == self.device.room and all([p.met(player) for p in self.prerequisites])

    def perform(self, player):
        for e in self.effects:
            e.perform(player)
        for p in self.prerequisites:
            p.enact(player)

class Effect:
    def __init__(self, data, device, tm):
        self.room = data.get('room', device.room.name)
        self.device = data.get('device', device.name)
        self.newState = data.get('state')
        self.item = data.get('item')
        self.tm = tm

    def perform(self, player):
        room = self.tm.map.room_map[self.room]
        if self.newState:
            for device in room.devices:
                if device.name == self.device:
                    device.state = self.newState
        if self.item:
            room.items.append(self.item)

class Prerequisite:
    def met(self, player):
        return True

    def enact(self, player):
        pass

class ItemPrerequisite(Prerequisite):
    def __init__(self, item, consumes, tm):
        self.item = item
        self.consumes = consumes
        self.tm = tm

    def met(self, player):
        return self.item in self.tm.inventories[player].items

    def enact(self, player):
        if self.consumes:
            self.tm.inventories[player].popItem(self.item)

class StatePrerequisite(Prerequisite):
    def __init__(self, room, device, states, tm):
        self.room = room
        self.device = device
        self.states = states
        self.tm = tm

    def met(self, player):
        for device in self.tm.map.room_map[self.room].devices:
            if device.name == self.device and device.state in self.states:
                return True
        return False

def construct_prerequisite(data, tm, room=None, device=None):
    if data['type'] == 'item':
        return ItemPrerequisite(data['item'], data.get('consumes', False), tm)
    else:
        states = data.get('states', [])
        if 'state' in data:
            states.append(data['state'])
        return StatePrerequisite(data.get('room', room), data.get('device', device), states, tm)
