import os
import heapq

import pygame
import yaml

import actions
import layers
import menus
import resources
import widgets

class Map:
    def __init__(self, map_file, sprites, tm, screen):
        data = yaml.safe_load(map_file)
        self.menu = menus.Popup(sprites, tm, screen)
        self.initial_rifts = [i != 0 for i in range(5)]
        self._rifts = list(self.initial_rifts)
        self.room_map = {}
        for room in data['rooms']:
            r = Room(room, self.menu, data['directory'], tm, self)
            sprites.add(r)
            self.room_map[room['name']] = r

    def reset(self):
        self._rifts = list(self.initial_rifts)
        for room in self.room_map.values():
            room.reset()

    def get_path(self, start, end, player):
        visited = []
        frontier = [(0, start, [])]
        while len(frontier) > 0:
            current = heapq.heappop(frontier)
            if current[1] == end:
                return current[2]
            if current[1] in visited:
                continue
            visited.append(current[1])
            for link in current[1].links:
                newRoom = self.room_map[link.room]
                if link.isvalid(player) and not newRoom in visited:
                    heapq.heappush(frontier, (current[0] + link.cost, newRoom, current[2] + [link]))
        return None

    def get_rift(self, timeline):
        return self._rifts[timeline]

    def set_rift(self, timeline, value):
        self._rifts[timeline] = value

class Room(widgets.WorldWidget):
    def __init__(self, data, menu, directory, tm, m):
        widgets.WorldWidget.__init__(self, data['position'])
        self._layer = layers.MAP
        self.name = data['name']
        self.centre = data['centre']
        self.base_image, rect = resources.load_png(os.path.join(directory, data['inactive']))
        self.active_image, _ = resources.load_png(os.path.join(directory, data['active']))
        self.mouse_over = False
        self.out_image = self.base_image
        self.over_image = self.active_image
        self.set_image(self.base_image)
        self.set_rect(rect)
        self.mask = pygame.mask.from_surface(self.image)
        self.actions = []
        if 'items' in data:
            self.initial_items = data['items']
        else:
            self.initial_items = []
        self.items = list(self.initial_items)
        self.width = self.base_image.get_width()
        self.height = self.base_image.get_height()
        self.tm = tm
        self.map = m
        self.rift = None
        if 'rift' in data:
            self.rift = actions.TimeTravel(data['rift']['name'], 1, data['rift']['time'], data['rift']['timeline'], tm)
            self.showing_rift = False
            self.rift_base_image, _ = resources.load_png(os.path.join(directory, "rift"+str(data['rift']['timeline'])+"."+data['inactive']))
            self.rift_active_image, _ = resources.load_png(os.path.join(directory, "rift"+str(data['rift']['timeline'])+"."+data['active']))
            self.actions.append(self.rift)
        if 'actions' in data:
            for action in data['actions']:
                self.actions.append(construct_action(action))
        self.links = []
        if 'links' in data:
            for link in data['links']:
                self.links.append(Link(link, self.name))
        self.menu = menu

    def over(self):
        widgets.WorldWidget.over(self)
        self.set_image(self.over_image)
        self.mouse_over = True
        
    def out(self):
        widgets.WorldWidget.out(self)
        self.set_image(self.out_image)
        self.mouse_over = False

    def pressed(self, pos, button):
        widgets.WorldWidget.pressed(self, pos, button)
        if button == 1:
            room = self.tm.active_avatar().room
            if room == self:
                self.menu.show(pos, self.actions +
                               [actions.Take("Take "+item, 1, item, self.tm) for item in self.items] +
                               [actions.Drop("Drop "+item, 1, item, self.tm) for item in self.tm.active_inventory().items])
            else:
                path = self.map.get_path(room, self, self.tm.active_player)
                if path:
                    self.menu.show(pos, [actions.MovePath("Go here", path, self.tm, self.map)])

    def update(self, camera):
        widgets.WorldWidget.update(self, camera)
        if self.rift:
            if self.rift.isvalid(self.tm.active_player):
                if not self.showing_rift:
                    self.showing_rift = True
                    self.out_image = self.rift_base_image
                    self.over_image = self.rift_active_image
                    if self.mouse_over:
                        self.set_image(self.over_image)
                    else:
                        self.set_image(self.out_image)
            else:
                if self.showing_rift:
                    self.showing_rift = False
                    self.out_image = self.base_image
                    self.over_image = self.active_image
                    if self.mouse_over:
                        self.set_image(self.over_image)
                    else:
                        self.set_image(self.out_image)

        if self.mask.get_size() != self.image.get_size():
            self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.items = list(self.initial_items)
        
class Link:
    def __init__(self, data, room):
        self.start = room
        self.room = data['room']
        self.cost = data['cost']

    def isvalid(self, player):
        return True

def construct_action(data):
    return actions.Action(data['name'], data['cost'])
