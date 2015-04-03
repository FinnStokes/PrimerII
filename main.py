#!/usr/bin/env python2
#
# Primer II: Electric Boogaloo
# Travel through time to prevent time travel from existing!

import argparse
import cProfile

import pygame
from pygame.locals import *

import actions
import cameras
import inventory
import layers
import maps
import timelines
import widgets

def main(**kwargs):
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

    tm = timelines.TimelineManager(sprites, screenRect)

    with open("mapdemo.yaml") as f:
        m = maps.Map(f, sprites, tm, screenRect)

    for i in range(len(tm.initial_room)):
        tm.initial_room[i] = m.room_map['CorridorNW']
        tm.players[i].room = tm.initial_room[i]
        
    done = False

    next_tl = 1

    tm.advance()
    
    while not done:
        widgets.update(sprites, active, pygame.mouse.get_pos())
        
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == K_KP0:
                    tm.seek(0)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP1:
                    tm.seek(1)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP2:
                    tm.seek(2)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP3:
                    tm.seek(3)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP4:
                    tm.seek(4)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP5:
                    tm.seek(5)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP6:
                    tm.seek(6)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP7:
                    tm.seek(7)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP8:
                    tm.seek(8)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
                elif event.key == K_KP9:
                    tm.seek(9)
                    tm.insert(next_tl)
                    tm.advance()
                    next_tl += 1
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Time travel game by 3 Silly Hats.')
    parser.add_argument('--profile-file', action='store')
    parser.add_argument('-p', '--profile', action='store_true')
    args = parser.parse_args()
    if args.profile:
        cProfile.run("main(**vars(args))", filename=args.profile_file)
    else:
        main(**vars(args))
