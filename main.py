#!/usr/bin/env python2
#
# Primer II: Electric Boogaloo
# Travel through time to prevent time travel from existing!

import os

import pygame
from pygame.locals import *

import actions
import cameras
import inventory
import layers
import maps
import timelines
import widgets

def main():
    # Initialise mixer
    pygame.mixer.pre_init(44100, -16, 2, 4096)

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((0,0), (pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE))
    pygame.display.set_caption('Primer II: Electric Boogaloo')
    screenRect = screen.get_rect()

    # Initialise background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0,0,0))

    # Initialise sprite groups
    sprites = pygame.sprite.LayeredUpdates()
    active = pygame.sprite.Group()
    pressed = pygame.sprite.Group()

    camera = cameras.Camera((0,0,1000,800),(0,0,100,80))
    
    #btn1 = widgets.BasicWidget(pygame.rect.Rect(300,300,900,500), (255, 0, 0), (0, 255, 0), (0, 0, 255))
    #btn2 = widgets.BasicWidget(pygame.rect.Rect(400,400,900,500), (255, 0, 0), (0, 255, 0), (0, 0, 255))
    #btn3 = widgets.BasicWidget(pygame.rect.Rect(100,100,1500,1000), (100, 100, 100), (200, 200, 200), (50, 50, 50))

    #sprites.add(btn1, btn2)
    #sprites.add(btn3, layer=layers.MAP)

    tm = timelines.TimelineManager(sprites)

    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 3))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 1))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 2))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.seek(4)
    tm.insert(2)
    tm.seek(2)
    tm.insert(1)
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 1))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 2))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 3))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 2))
    tm.advance()
    print(tm.active_player, tm.current_time)
    tm.active_timeline().actions.append(actions.Action("test", 2))
    tm.advance()
    print(tm.active_player, tm.current_time)

    with open("mapdemo.yaml") as f:
        m = maps.Map(f, sprites, tm)        
    
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            elif event.type == MOUSEMOTION:
                widgets.update(sprites, active, event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                for s in active:
                    if s.pressed:
                        s.pressed(event.pos, event.button)
            elif event.type == MOUSEBUTTONUP:
                for s in active:
                    if s.released:
                        s.released(event.pos, event.button)

        # Blit everything to the screen
        screen.blit(background, (0, 0))
        sprites.update(camera)
        sprites.draw(screen)
        pygame.display.flip()

if __name__ == '__main__': main()
