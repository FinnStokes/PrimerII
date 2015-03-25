import os

import pygame
import yaml
import math

import actions
import layers
import resources
import widgets

INVBOX_WIDTH = 500
INVBOX_HEIGHT = 1080-880
INVBOX_CORNER = ((1920-INVBOX_WIDTH),0)
MAX_TIMELINES = 5
INV_ITEMS = 4

class Slot(widgets.Widget):
    def __init__(self, centre, width, height):
    	widgets.Widget.__init__(self)
        image, _ = resources.load_png(os.path.join('items', 'blank.png'))
        rect = pygame.Rect(0, 0, width, height)
        rect.center = centre
        self.set_image(image)
        self.set_rect(rect)
        self.mask = pygame.mask.from_surface(self.image)
        self._layer = layers.OBJECTS

class Inventory:
    def __init__(self, timeline, sprites):
        #timelines must start at 0
        self._layer = layers.HUD
        self.timeline = timeline
        self.sprites = sprites

        widthchunk = INVBOX_WIDTH/(INV_ITEMS+1)
        heightchunk = INVBOX_HEIGHT/MAX_TIMELINES
        self.allcentres = [ [INVBOX_CORNER[0]+math.ceil((ii+0.5)*widthchunk),
                             INVBOX_CORNER[1]+math.ceil((self.timeline+0.5)*heightchunk)]
                           for ii in range(INV_ITEMS)]

        self.slots = []
        self.items = []
        for ii in range(INV_ITEMS):
            newSlot = Slot(self.allcentres[ii], heightchunk-10, heightchunk-10)
            self.sprites.add(newSlot)
            self.slots.append(newSlot)

    def isfull(self):
        return len(self.items) >= len(self.slots)

    def addItem(self, newItem):
        if len(self.items) < len(self.slots):
            self.items.append(newItem)
            self.update()
            return True
        return False

    def popItem(self,itemName):
        if itemName in self.items:
            self.items.remove(itemName)
            self.update()
            return True
        return False

    def update(self):
        for ii in xrange(len(self.slots)):
            if ii < len(self.items):
                name = self.items[ii]+".png"
            else:
                name = "blank.png"
            img, _ = resources.load_png(os.path.join('items', name))
            self.slots[ii].set_image(img)
