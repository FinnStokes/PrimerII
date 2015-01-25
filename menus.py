import pygame

import widgets

ITEM_WIDTH = 100
ITEM_HEIGHT = 20

class Popup:
    def __init__(self, sprites, tm):
        self.sprites = sprites
        self.items = pygame.sprite.Group()
        self.tm = tm
        
    def show(self, pos, actions):
        self.sprites.remove(self.items)
        self.items.empty()
        x = pos[0]
        y = pos[1]
        for action in actions:
            if action.isvalid(self.tm.active_player):
                self.items.add(Item(action, (x,y), self.tm))
                y += ITEM_HEIGHT
        self.sprites.add(self.items)

    def hide(self):
        self.sprites.remove(self.items)
        self.items.empty()

class Item(widgets.BasicWidget):
    def __init__(self, action, pos, tm):
        widgets.BasicWidget.__init__(self, pygame.Rect(pos, (ITEM_WIDTH, ITEM_HEIGHT)), (100, 100, 100), (200, 200, 200), (50, 50, 50))
        self.action = action
        self.tm = tm

    def pressed(self, pos, button):
        widgets.BasicWidget.pressed(self, pos, button)
        if button == 0 and action.isvalid(self.tm.active_player):
            self.tm.do(self.action)
            self.tm.advance()
