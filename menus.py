import pygame

import layers
import widgets

ITEM_WIDTH = 400
ITEM_HEIGHT = 35

class Popup:
    def __init__(self, sprites, tm, screen):
        self.sprites = sprites
        self.items = pygame.sprite.Group()
        self.tm = tm
        self.canceller = Canceller(self, screen)
        
    def show(self, pos, actions):
        self.hide()
        self.items.add(self.canceller)
        x = pos[0]
        y = pos[1]
        for action in actions:
            if action.isvalid(self.tm.active_player):
                self.items.add(Item(action, (x,y), self.tm, self))
                y += ITEM_HEIGHT
        self.sprites.add(self.items)

    def hide(self):
        self.sprites.remove(self.items)
        self.items.empty()

class Canceller(widgets.Widget):
    def __init__(self, parent, rect):
        widgets.Widget.__init__(self)
        self.parent = parent
        self.set_rect(rect)
        self._layer = layers.HUD
        self.image = pygame.Surface((0,0))

    def pressed(self, pos, button):
        self.parent.hide()
        
class Item(widgets.TextWidget):
    def __init__(self, action, pos, tm, parent):
        widgets.TextWidget.__init__(self, pygame.Rect(pos, (ITEM_WIDTH, ITEM_HEIGHT)), (100, 100, 100), (50, 50, 50), (200, 200, 200), (255,255,255), action.name +" ("+str(action.cost)+")")
        self.action = action
        self.tm = tm
        self.parent = parent
        self._layer = layers.POPUP

    def pressed(self, pos, button):
        widgets.BasicWidget.pressed(self, pos, button)
        if button == 1 and self.action.isvalid(self.tm.active_player):
            self.tm.do(self.action)
            self.tm.advance()
            self.parent.hide()
