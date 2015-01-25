import os

import pygame

import inventory
import layers
import resources
import widgets

class Timeline:
    def __init__(self, player, tm, actions=[], planned=None, start_time=0):
        self.actions = actions[:]
        if planned:
            self.planned = planned[:]
        self.current_action = -1
        self.ticks = 0
        self.start_time = start_time
        self.active = True
        self.player = player
        self.tm = tm
        self.sprites = pygame.sprite.Group()

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
                        #print(self.player, "playback beginning action")
                        action.perform(self.player)
                    else:
                        print("Error in action playback")
                    self.ticks = action.cost
                else:
                    #print(self.player, "playback out of actions")
                    break
            #else:
                #print(self.player, "playback continuing action")
            self.ticks -= 1
            current_time += 1
        #print(self.player, "playback done", self.ticks, current_time)
        self.ticks += current_time - time

    def advance(self):
        if not self.active:
            #print(self.player, "inactive")
            return True
        if self.current_action >= len(self.actions):
            #print(self.player, "out of actions")
            return False
        if self.ticks <= 0:
            if self.current_action + 1 < len(self.actions):
                self.current_action += 1
                action = self.actions[self.current_action]
                if action.isvalid(self.player):
                    #print(self.player, "starting action")
                    self.ticks = action.cost
                    action.perform(self.player)
                else:
                    #print(self.player, "invalid action")
                    self.planned = self.actions
                    self.actions = self.actions[:self.current_action]
                    print("clear")
                    self.tm.sprites.remove(self.sprites)
                    self.tm.allsprites.remove(self.sprites)
                    self.sprites.empty()
                    for action in self.actions:
                        aw = ActionWidget(action, self.player)
                        self.sprites.add(aw)
                        self.tm.sprites.add(aw)
                        self.tm.allsprites.add(aw)
                    return False
            else:
                #print(self.player, "out of actions")
                return False
        #else:
            #print(self.player, "continuing action")
        self.ticks -= 1
        return True

    def do(self, action):
        self.actions.append(action)
        aw = ActionWidget(action, self.player, self.tm)
        self.sprites.add(aw)
        self.tm.sprites.add(aw)
        self.tm.allsprites.add(aw)

PANE_TOP = 880
SPACING = 15
CURRENT_TIME_X = 1920/2

class ActionWidget(widgets.Widget):
    def __init__(self, action, timeline, tm):
        widgets.Widget.__init__(self)
        self.action = action
        self.image = tm.images[action.cost-1]
        self.rect = self.image.get_rect()
        self.rect.top = PANE_TOP + SPACING + (SPACING + self.image.get_height()) * timeline
        self.rect.left = CURRENT_TIME_X
        self._layer = layers.HUD
                
class TimelineManager:
    def __init__(self, sprites):
        self.timelines = [Timeline(0, self), None, None, None, None]
        self.inventories = [inventory.Inventory(i, sprites) for i in range(5)]
        self.active_player = 0
        self.current_time = 0
        self.sprites = pygame.sprite.Group()
        self.allsprites = sprites
        self.images = [resources.load_png(os.path.join('timeline', str(cost)+'part.png'))[0] for cost in range(1,6)]

    def active_timeline(self):
        return self.timelines[self.active_player]

    def active_inventory(self):
        return self.inventories[self.active_player]

    def seek(self, time):
        self.active_player = 0
        for sprite in self.sprites:
            sprite.rect.left -= self.images[0].get_width() * (time - self.current_time)
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
                for sprite in self.sprites:
                    sprite.rect.left -= self.images[0].get_width()

    def insert(self, player_no):
        if self.timelines[player_no]:
            self.timelines[player_no] = Timeline(player_no, self, planned=self.timelines[player_no].actions, start_time=self.current_time)
        else:
            self.timelines[player_no] = Timeline(player_no, self, start_time=self.current_time)

    def do(self, action):
        self.active_timeline().do(action)
