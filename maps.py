import os

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
        self.room_map = {}
        for room in data['rooms']:
            r = Room(room, self.menu, data['directory'], tm)
            sprites.add(r)
            self.room_map[room['name']] = r

class Room(widgets.WorldWidget):
    def __init__(self, data, menu, directory, tm):
        widgets.WorldWidget.__init__(self, data['position'])
        self._layer = layers.MAP
        self.name = data['name']
        self.centre = data['centre']
        self.base_image, rect = resources.load_png(os.path.join(directory, data['inactive']))
        self.active_image, _ = resources.load_png(os.path.join(directory, data['active']))
        self.set_image(self.base_image)
        self.set_rect(rect)
        self.mask = pygame.mask.from_surface(self.image)
        self.actions = []
        if 'items' in data:
            self.items = data['items']
        else:
            self.items = []
        self.width = self.base_image.get_width()
        self.height = self.base_image.get_height()
        self.tm = tm
        if 'actions' in data:
            for action in data['actions']:
                self.actions.append(construct_action(action))
        self.links = []
        if 'links' in data:
            for link in data['links']:
                self.links.append(Link(link))
        self.menu = menu

    def over(self):
        widgets.WorldWidget.over(self)
        self.set_image(self.active_image)

    def out(self):
        widgets.WorldWidget.out(self)
        self.set_image(self.base_image)

    def pressed(self, pos, button):
        widgets.WorldWidget.pressed(self, pos, button)
        if button == 1:
            room = self.tm.active_avatar().room
            if room == self:
                self.menu.show(pos, self.actions + [actions.Take("Take "+item, 1, item, self.tm) for item in self.items])
            else:
                for link in room.links:
                    if link.room == self.name:
                        self.menu.show(pos, [actions.Move("Go here", link.cost, room, self, self.tm)])
                        break

    def update(self, camera):
        widgets.WorldWidget.update(self, camera)
        if self.mask.get_size() != self.image.get_size():
            self.mask = pygame.mask.from_surface(self.image)
        
class Link:
    def __init__(self, data):
        self.room = data['room']
        self.cost = data['cost']

def construct_action(data):
    return actions.Action(data['name'], data['cost'])
