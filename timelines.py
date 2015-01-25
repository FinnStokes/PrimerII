import inventory

class Timeline:
    def __init__(self, player, actions=[], planned=None, start_time=0):
        self.actions = actions[:]
        if planned:
            self.planned = planned[:]
        self.current_action = -1
        self.ticks = 0
        self.start_time = start_time
        self.active = True
        self.player = player

    def seek(self, time):
        self.current_action = -1
        self.ticks = 0
        current_time = self.start_time
        self.active = True
        while current_time < time:
            if self.ticks <= 0:
                self.current_action += 1
                if self.current_action < len(self.actions):
                    action = self.actions[self.current_action]
                    if action.isvalid(self.player):
                        action.perform(self.player)
                    else:
                        print("Error in action playback")
                    self.ticks = action.cost
                else:
                    break
            self.ticks -= 1
            current_time += 1
        self.ticks = current_time - time

    def advance(self):
        if not self.active:
            return True
        if self.current_action >= len(self.actions):
            return False
        if self.ticks <= 0:
            if self.current_action + 1 < len(self.actions):
                self.current_action += 1
                action = self.actions[self.current_action]
                if action.isvalid(self.player):
                    self.ticks = action.cost
                    action.perform(self.player)
                else:
                    self.planned = self.actions
                    self.actions = self.actions[:self.current_action]
                    return False
            else:
                return False
        self.ticks -= 1
        return True

    def do(self, action):
        self.actions.append(action)
                
class TimelineManager:
    def __init__(self, sprites):
        self.timelines = [Timeline(0), None, None, None, None]
        self.inventories = [inventory.Inventory(i, sprites) for i in range(5)]
        self.active_player = 0
        self.current_time = 0

    def active_timeline(self):
        return self.timelines[self.active_player]

    def active_inventory(self):
        return self.inventories[self.active_player]

    def seek(self, time):
        self.active_player = 0
        self.current_time = time
        for t in self.timelines:
            if t:
                t.seek(time)
        
    def advance(self):
        while True:
            if self.active_timeline():
                if not self.active_timeline().advance():
                    return
            self.active_player += 1
            if self.active_player >= len(self.timelines):
                self.active_player = 0
                self.current_time += 1

    def insert(self, player_no):
        if self.timelines[player_no]:
            self.timelines[player_no] = Timeline(player_no, planned=self.timelines[player_no].actions, start_time=self.current_time)
        else:
            self.timelines[player_no] = Timeline(player_no, start_time=self.current_time)

    def do(self, action):
        self.active_timeline().do(action)
