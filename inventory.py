import os

import pygame
import yaml
import math

import actions
import layers
import resources

INVBOX_WIDTH = 500
INVBOX_HEIGHT = 1080-880
INVBOX_CORNER = [(1920-INVBOX_WIDTH,0]
MAX_TIMELINES = 5
INV_ITEMS = 4

BLANK = {}
BLANK['name']='blank'
BLANK['desc']='blank'
BLANK['centre']=[0,0]
BLANK['onMap']= 'blank.png'

class Item(pygame.sprite.Sprite):
    def __init__(self, data, sprites):
    	pygame.sprite.Sprite.__init__(self)
        self.name = data['name']
        self.desc = data['desc']
        self.centre = data['centre']
        self.image, self.rect = resources.load_png(os.path.join(directory, data['onMap']))
        self.mask = pygame.mask.from_surface(self.image)
        self.layer = layers.OBJECT
        sprites.add(self)

class Inventory:
	def __init__(self, timeline, sprites):
		#timelines must start at 0
		self.layer = layers.HUD
		self.allcentres = [[0 for i in range(INV_ITEMS)] for j in range(2)]
		self.timeline = timeline

		widthchunk = INVBOX_WIDTH/(INV_ITEMS+1)
		heightchunk = INVBOX_HEIGHT/MAX_TIMELINES
		for ii in range(1,INV_ITEMS+1):
			self.allcentres[ii]=[INVBOX_CORNER(1)+ceil((ii+0.5)*widthchunk), INVBOX_CORNER(2)+ceil((self.timeline+0.5)*heightchunk)]

		self.invList = []
		for ii in range(INV_ITEMS):
			newItem=Item(BLANK,sprites)
			newItem.centre = self.allcentres[ii]
			self.invList.append(newItem)

	def addItem(self, newItem,sprites):
		for ii in range(INV_ITEMS):
			if self.invList[ii].name == 'blank':
				newItem.centre = self.allcentres[ii]
				self.invList[ii] = newItem(BLANK,sprites)
				return true
		return false

	def popItem(self,itemName,newCentre,sprites):
		for ii in range(INV_ITEMS):
			if self.invList[ii].name == itemName:
				self.invList[ii].centre = newCentre
				for jj in range(ii,INV_ITEMS-1):
					self.invList[jj]=self.invList[jj+1]
					self.invList[jj].centre=self.allcentres[jj]
				self.invList[INV_ITEMS-1]=Item(BLANK,sprites)
				self.invList[INV_ITEMS-1].centre=self.allcentres[INV_ITEMS-1]
				return true
		return false

	def clearItem(self,itemName,sprites):
		for ii in range(INV_ITEMS):
			if self.invList[ii].name == itemName:
				for jj in range(ii,INV_ITEMS-1):
					self.invList[jj]=self.invList[jj+1]
					self.invList[jj].centre=self.allcentres[jj]
				self.invList[INV_ITEMS-1]=Item(BLANK,sprites)
				self.invList[INV_ITEMS-1].centre=self.allcentres[INV_ITEMS-1]
				return true
		return false



