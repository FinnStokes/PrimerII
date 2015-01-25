import pygame

import widgets

WIDTH = 30
HEIGHT = 30

OFFSET = [[-1,-1],
          [ 2,-1],
          [-1, 2],
          [-4,-1],
          [-1,-4],
]
          

class Player(widgets.Widget):
    def __init__(self, id, colour, sprites, timeline, inventory, room):
        widgets.Widget.__init__(self)
        self.id = id
        self.sprites = sprites
        self.timeline = timeline
        self.inventory = inventory
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.active = False
        self.room = room
        self.blocking = False

    def refresh(self):
        if self.timeline and self.timeline.isactive():
            if not self.active:
                self.sprites.add(self)
                self.active = True
            self.rect.topleft = ((self.room.centre[0]+OFFSET[self.id][0])*10, (self.room.centre[1]+OFFSET[self.id][1])*10)
        elif self.active:
            self.sprites.remove(self)
            self.active = False
