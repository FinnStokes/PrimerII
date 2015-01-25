import pygame

class Widget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
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

    def update(self, camera):
        pass

class WorldWidget(Widget):
    def __init__(self, pos):
        Widget.__init__(self)
        self.blocking = False
        self.position = pos

    def update(self, camera):
        self.rect.top = camera.screen.top + (self.position[1] - camera.world.top) * camera.screen.width / camera.world.width
        self.rect.left = camera.screen.left + (self.position[0] - camera.world.left) * camera.screen.height / camera.world.height
        self.rect.width = self.width * camera.screen.width / camera.world.width
        self.rect.height = self.height * camera.screen.height / camera.world.height
        if self.rect.width != self.image.get_width() or self.rect.height != self.image.get_height():
            self.image = pygame.transform.scale(self.unscaled_image, self.rect.size)
    
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

class TextWidget(BasicWidget):
    def __init__(self,rect,baseColour,hoverColour,pressedColour,textColour,incText):
        BasicWidget.__init__(self,rect,baseColour,hoverColour,pressedColour)

        self.textColour= textColour
        self.incText = incText

        self.font = pygame.font.SysFont(None, 25)
        self.textImage = self.font.render(self.incText,True,textColour)

        self.baseImage.blit(self.textImage, (10,10))
        self.hoverImage.blit(self.textImage, (10,10))
        self.pressedImage.blit(self.textImage, (10,10))

        self.image=self.baseImage
        self.rect = rect


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

