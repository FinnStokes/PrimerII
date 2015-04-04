import os

import pygame
from pygame.locals import *

from actions import Action, CompoundAction
import inventory
import layers
import players
import resources
import widgets

COLOURS = ((255,0,0), (0,255,0), (0,0,255), (255, 255, 0), (255, 0, 255))

class Timeline:
    def __init__(self, player, tm, actions=[], planned=None, start_time=0):
        self.actions = list(actions)
        if planned:
            self.planned = list(planned)
        self.current_action = -1
        self.ticks = 0
        self.start_time = start_time
        self.active = True
        self.player = player
        self.tm = tm
        self.sprites = pygame.sprite.Group()
        self.current_time = start_time

    def seek(self, time):
        self.current_action = -1
        self.ticks = 0
        self.current_time = min(self.start_time, time)
        self.active = True
        while self.current_time < time:
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
            self.current_time += 1
        #print(self.player, "playback done", self.ticks, self.current_time)
        self.ticks += self.current_time - time

    def advance(self):
        if not self.isactive():
            #print(self.player, "inactive")
            self.current_time += 1
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
                    self.current_action -= 1
                    self.tm.sprites.remove(self.sprites)
                    self.tm.allsprites.remove(self.sprites)
                    self.sprites.empty()
                    for action in self.actions:
                        aw = ActionWidget(action, self.player, self.tm)
                        self.sprites.add(aw)
                        self.tm.sprites.add(aw)
                        self.tm.allsprites.add(aw)
                        for sprite in self.sprites:
                            rect = sprite.rect.copy()
                            rect.left -= self.tm.images[0].get_width()*action.cost
                            sprite.set_rect(rect)
                    return False
            else:
                #print(self.player, "out of actions")
                return False
        #else:
            #print(self.player, "continuing action")
        self.ticks -= 1
        self.current_time += 1
        return True

    def do(self, action):
        if isinstance(action, Action):
            self.actions.append(action)
            aw = ActionWidget(action, self.player, self.tm)
            self.sprites.add(aw)
            self.tm.sprites.add(aw)
            self.tm.allsprites.add(aw)
            action.first_perform(self.player)
        elif isinstance(action, CompoundAction):
            ticks = 0
            for act in action.actions:
                self.actions.append(act)
                aw = ActionWidget(act, self.player, self.tm, offset=ticks)
                self.sprites.add(aw)
                self.tm.sprites.add(aw)
                self.tm.allsprites.add(aw)
                ticks += act.cost
                act.first_perform(self.player)
        else:
            print("Error doing action: not subclass of Action or CompoundAction")

    def isactive(self):
        return self.active and self.current_time >= self.start_time

    def clear(self):
        self.tm.sprites.remove(self.sprites)
        self.tm.allsprites.remove(self.sprites)
        self.sprites.empty()

PANE_TOP = 880
SPACING = 15
CURRENT_TIME_X = 1920/2

class ActionWidget(widgets.Widget):
    def __init__(self, action, timeline, tm, offset=0):
        widgets.Widget.__init__(self)
        self.action = action
        image = tm.images[action.cost-1].copy()
        image.fill(COLOURS[timeline], special_flags=BLEND_RGB_MULT)
        self.set_image(image)
        rect = self.image.get_rect()
        rect.top = PANE_TOP + SPACING + (SPACING + self.image.get_height()) * timeline
        rect.left = CURRENT_TIME_X + offset*tm.images[0].get_width()
        self.set_rect(rect)
        
        self._layer = layers.HUD
                
class TimelineManager:
    def __init__(self, sprites, screen, m=None):
        self.timelines = [Timeline(0, self), None, None, None, None]
        self.inventories = [inventory.Inventory(i, sprites, screen, self) for i in range(5)]
        self.initial_room = [None] * 5
        self.players = [players.Player(i, COLOURS[i], sprites, self.timelines[i], self.inventories[i], self.initial_room[i]) for i in range(5)]
        self.active_player = 0
        self.current_time = 0
        self.sprites = pygame.sprite.Group()
        self.allsprites = sprites
        self.images = [resources.load_png(os.path.join('timeline', str(cost)+'part.png'))[0] for cost in range(1,6)]
        self.map = m

    def active_timeline(self):
        return self.timelines[self.active_player]

    def active_inventory(self):
        return self.inventories[self.active_player]

    def active_avatar(self):
        return self.players[self.active_player]
    
    def seek(self, time):
        self.active_player = 0
        for sprite in self.sprites:
            rect = sprite.rect.copy()
            rect.left -= self.images[0].get_width() * (time - self.current_time)
            sprite.set_rect(rect)
        self.current_time = time
        self.map.reset()
        for i in range(len(self.players)):
            self.players[i].room = self.initial_room[i]
        for inventory in self.inventories:
            inventory.reset()
        for t in self.timelines:
            if t:
                t.seek(time)
        for player in self.players:
            player.refresh(self.active_player)
        
    def advance(self):
        while True:
            if self.active_timeline():
                if not self.active_timeline().advance():
                    break
            self.active_player += 1
            if self.active_player >= len(self.timelines):
                self.active_player = 0
                self.current_time += 1
                for sprite in self.sprites:
                    rect = sprite.rect.copy()
                    rect.left -= self.images[0].get_width()
                    sprite.set_rect(rect)
        for player in self.players:
            player.refresh(self.active_player)

    def insert(self, player_no):
        if self.timelines[player_no]:
            old = self.timelines[player_no]
            self.timelines[player_no] = Timeline(player_no, self, planned=old.actions, start_time=self.current_time)
            old.clear()
        else:
            self.timelines[player_no] = Timeline(player_no, self, start_time=self.current_time)
        self.players[player_no].timeline = self.timelines[player_no]
        self.players[player_no].refresh(self.active_player)

    def do(self, action):
        self.active_timeline().do(action)
