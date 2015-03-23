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

BLANK = {}
BLANK['name']='blank'
BLANK['desc']='blank'
BLANK['centre']=[0,0]
BLANK['onMap']= 'blank.png'

class Item(widgets.Widget):
    def __init__(self, data, sprites):
    	widgets.Widget.__init__(self)
        self.name = data['name']
        self.desc = data['desc']
        image, rect = resources.load_png(os.path.join('items', data['onMap']))
        rect.center = data['centre']
        self.set_image(image)
        self.set_rect(rect)
        self.mask = pygame.mask.from_surface(self.image)
        self._layer = layers.OBJECTS
        sprites.add(self)

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

        self.invList = []
        for ii in range(INV_ITEMS):
            newItem = Item(BLANK,sprites)
            rect = newItem.rect.copy()
            rect.center = self.allcentres[ii]
            newItem.set_rect(rect)
            self.invList.append(newItem)

    def addItem(self, newItem):
        for ii in range(INV_ITEMS):
            if self.invList[ii].name == 'blank':
                rect = newItem.rect.copy()
                rect.center = self.allcentres[ii]
                newItem.set_rect(rect)
                self.invList[ii] = newItem
                return True
        return False

    def popItem(self,itemName,newCentre):
        for ii in range(INV_ITEMS):
            if self.invList[ii].name == itemName:
                rect = self.invList[ii].rect.copy()
                rect.center = newCentre
                self.invList[ii].set_rect(rect)
                for jj in range(ii,INV_ITEMS-1):
                    self.invList[jj] = self.invList[jj+1]
                    rect = self.invList[jj].rect.copy()
                    rect.center = self.allcentres[jj]
                    self.invList[jj].set_rect(rect)
                self.invList[INV_ITEMS-1]=Item(BLANK,self.sprites)
                rect = self.invList[INV_ITEMS-1].rect.copy()
                rect.center = self.allcentres[INV_ITEMS-1]
                self.invList[INV_ITEMS-1].set_rect(rect)
                return True
        return False

    def clearItem(self,itemName):
        for ii in range(INV_ITEMS):
            if self.invList[ii].name == itemName:
                for jj in range(ii,INV_ITEMS-1):
                    self.invList[jj] = self.invList[jj+1]
                    rect = self.invList[jj].rect.copy()
                    rect.center = self.allcentres[jj]
                    self.invList[jj].set_rect(rect)
                self.invList[INV_ITEMS-1] = Item(BLANK,self.sprites)
                rect = self.invList[INV_ITEMS-1].rect.copy()
                rect.center = self.allcentres[INV_ITEMS-1]
                self.invList[INV_ITEMS-1].set_rect(rect)
                return True
        return False



