import pygame
import yaml

import actions
import layers
import menus
import resources
import widgets

class Map:
    def __init__(self, map_file, sprites):
        data = yaml.safe_load(map_file)
        self.menu = menus.Popup(sprites)
        self.room_map = {}
        for room in data['rooms']:
            r = Room(room, self.menu)
            sprites.add(r)
            self.room_map[room['name']] = r

class Room(widgets.WorldWidget):
    def __init__(self, data, menu):
        widgets.WorldWidget.__init__(self, data['position'])
        self.level = layers.MAP
        self.name = data['name']
        self.centre = data['centre']
        self.base_image, self.rect = resources.load_png(data['inactive'])
        self.active_image, _ = resources.load_png(data['active'])
        self.image = self.base_image
        self.actions = []
        for action in data['actions']:
            self.actions.append(construct_action(action))
        self.links = []
        for link in data['links']:
            self.links.append(Link(link))
        self.menu = menu

    def over(self):
        self.image = self.active_image

    def out(self):
        self.image = self.base_image

    def pressed(self, pos, button):
        if button == 1:
            self.menu.show(pos, self.actions)
        
class Link:
    def __init__(self, data):
        self.room = data['room']
        self.cost = data['cost']

def construct_action(data):
    return actions.Action(data['name'], data['cost'])
