import pygame

import widgets

ITEM_WIDTH = 100
ITEM_HEIGHT = 20

class Popup:
    def __init__(self, sprites):
        self.sprites = sprites
        self.items = pygame.sprite.Group()
        
    def show(self, pos, actions):
        self.sprites.remove(self.items)
        self.items.empty()
        x = pos[0]
        y = pos[1]
        for action in actions:
            self.items.add(Item(action, (x,y)))
            y += ITEM_HEIGHT
        self.sprites.add(self.items)

    def hide(self):
        self.sprites.remove(self.items)
        self.items.empty()

class Item(widgets.BasicWidget):
    def __init__(self, action, pos):
        widgets.BasicWidget.__init__(self, pygame.Rect(pos, (ITEM_WIDTH, ITEM_HEIGHT)), (100, 100, 100), (200, 200, 200), (50, 50, 50))
        self.action = action
