import pygame

class Widget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.layer = 0
        self.blocking = True

    def over(self):
        pass

    def out(self):
        pass

    def pressed(self, pos, button):
        pass

    def released(self, pos, button):
        pass

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        pass

class BasicWidget(Widget):
    def __init__(self, rect, baseColour, hoverColour, pressedColour):
        Widget.__init__(self)
        
        self.baseImage = pygame.Surface([rect.width, rect.height])
        self.baseImage.fill(baseColour)

        self.hoverImage = pygame.Surface([rect.width, rect.height])
        self.hoverImage.fill(hoverColour)

        self.pressedImage = pygame.Surface([rect.width, rect.height])
        self.pressedImage.fill(pressedColour)

        self.image = self.baseImage
        self.rect = rect

    def over(self):
        self.image = self.hoverImage

    def out(self):
        self.image = self.baseImage

    def pressed(self, pos, button):
        if button == 1:
            self.image = self.pressedImage

    def released(self, pos, button):
        if button == 1:
            self.image = self.hoverImage

def update(sprites, active, pos):
    current = pygame.sprite.Group()
    for s in reversed(sprites.sprites()):
        if s.contains and s.contains(pos):
            current.add(s)
            if not s in active:
                active.add(s)
                s.over()
            if s.blocking:
                break
    for s in active:
        if not s in current:
            active.remove(s)
            s.out()
