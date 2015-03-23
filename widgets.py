import pygame

class Widget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.blocking = True
        self.rect = None
        self.image = None
        self._base_image = None

    def set_image(self, image):
        self._base_image = image
        self.image = image
        self.rescale_image()

    def set_rect(self, rect):
        self.rect = rect
        self.rescale_image()
        
    def rescale_image(self):
        if self.rect and self.image and self._base_image and (self.rect.width != self.image.get_width() or self.rect.height != self.image.get_height()):
            self.image = pygame.transform.scale(self._base_image, self.rect.size)
        
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
        self.set_rect(pygame.Rect(camera.screen.left + (self.position[0] - camera.world.left) * camera.screen.height / camera.world.height,
                                  camera.screen.top + (self.position[1] - camera.world.top) * camera.screen.width / camera.world.width,
                                  self.width * camera.screen.width / camera.world.width,
                                  self.height * camera.screen.height / camera.world.height))
    
class BasicWidget(Widget):
    def __init__(self, rect, baseColour, hoverColour, pressedColour):
        Widget.__init__(self)
        
        self.baseImage = pygame.Surface([rect.width, rect.height])
        self.baseImage.fill(baseColour)

        self.hoverImage = pygame.Surface([rect.width, rect.height])
        self.hoverImage.fill(hoverColour)

        self.pressedImage = pygame.Surface([rect.width, rect.height])
        self.pressedImage.fill(pressedColour)

        self.set_image(self.baseImage)
        self.set_rect(rect)

    def over(self):
        self.set_image(self.hoverImage)

    def out(self):
        self.set_image(self.baseImage)

    def pressed(self, pos, button):
        if button == 1:
            self.set_image(self.pressedImage)

    def released(self, pos, button):
        if button == 1:
            self.set_image(self.hoverImage)

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

        self.set_image(self.baseImage)
        self.set_rect(rect)


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

