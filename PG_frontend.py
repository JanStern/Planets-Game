import numpy as np 
from numpy.random import randint as rnd
import PG_backend

import pygame, time,os


def fade(screen):
    for i in range(200):
        screen.fill((200-i,200-i,200-i))
        pygame.display.flip()
    for i in range(255):
        screen.fill((i,i,i))
        pygame.display.flip()

def active_players(planets):
    i = 0
    for k in range(len(planets)-10):
        if (planets[k].mas !=0): i+=1
    return i 

def color(p):
    c=()
    border = 1000
    if(p.heat<border): 
        a = int(p.heat/border*255)
        c = (a,0,255-a)
    elif(p.heat<2*border):
        a = int((p.heat-border)/border*255)
        c=(255,a,0)
    elif(p.heat>6000):
        c=(0,0,0)
    else: c=(255,255,0)

    return c

def victory(planets,screen,l,h):

    next_lvl = False

    if (active_players(planets)==1 and planets[0].mas != 0):
        next_lvl = True
        font = pygame.font.SysFont("microsoftyibaiti", int(l/15))
        
        for i in range(255):
            screen.fill((255-i,255-i,255-i))
            pygame.display.flip()

        for i in range(255):
            screen.fill((i,i,i))
            screen.blit(font.render("Level passed", True, (0, 0, 0)), (l//2-150,h//2-50))
            time.sleep(0.01)
            pygame.display.flip()
        
        time.sleep(0.5)
    
    return next_lvl


def death(planets,screen,l,h,N):
    start = True

    if planets[0].mas == 0:
        start = False
        font = pygame.font.SysFont("microsoftyibaiti", int(l/15))
        lvl = N-2

        for i in range(255):
            screen.fill((255-i,255-i,255-i))
            screen.blit(font.render(("YOU DIED! Level: %s" % lvl), True, (255, 255, 255)), (l//2-250,h//2-50))
            time.sleep(0.01)
            pygame.display.flip()
        
        time.sleep(0.5)

    return start



def plot_text(planets,screen,l,h):
    font = pygame.font.SysFont("microsoftyibaitiv", int(l/35))
    screen.blit(font.render(("Mas: %s" % int(planets[0].mas)), True, (0, 0, 0)), (10,10))
    screen.blit(font.render(("X: %s" % int(planets[0].x)), True, (0, 0, 0)), (l//2-100,10))
    screen.blit(font.render(("Y: %s" % int(planets[0].y)), True, (0, 0, 0)), (l//2-40,10))
    screen.blit(font.render(("Players: %s" % active_players(planets)), True, (0, 0, 0)), (l//2+40,10))
    screen.blit(font.render(("Heat: %s" % int(planets[0].heat)), True, (0, 0, 0)), (l-100,10))





def start(planets,screen,l,h,highscore):

    screen.fill((200,200,200))

    for i in range(len(planets)):
        if planets[i].mas>3:
            pygame.draw.circle(screen,(0,0,0),(int(planets[i].x),int(planets[i].y)), int(planets[i].mas**(2/3)))


    pos = pygame.mouse.get_pos()  
    font = pygame.font.SysFont("microsoftyibaiti", int(l/15))
    
    if (pos[0]>l//2-100 and pos[1]>h//2-100 and pos[0]<l//2+150 and pos[1]<h//2-40):
        screen.blit(font.render(("New Game"), True, (200, 200, 0)), (l//2-100,h//2-100))
    else:
        screen.blit(font.render(("New Game"), True, (0, 0, 0)), (l//2-100,h//2-100))

    font = pygame.font.SysFont("microsoftyibaiti", int(l/25))
    screen.blit(font.render(("Highscore: %s" % highscore), True, (0, 0, 0)), (l//2-60,h//2))

    pygame.display.flip()



def main(planets,screen,l,h):
    screen.fill((255,255,255))

    for i in range(len(planets)):
        coordinats = int(planets[i].x),int(planets[i].y)
        radius = int(planets[i].mas**(2/3))
        pygame.draw.circle(screen,color(planets[i]),coordinats,radius)

    # font = pygame.font.SysFont("microsoftyibaitiv", int(l/35))
    # screen.blit(font.render(("Mas: %s" % int(planets[0].mas)), True, (0, 0, 0)), (10,10))
    # screen.blit(font.render(("X: %s" % int(planets[0].x)), True, (0, 0, 0)), (l//2-40,10))
    # screen.blit(font.render(("Y: %s" % int(planets[0].y)), True, (0, 0, 0)), (l//2+20,10))
    # screen.blit(font.render(("Players: %s" % active_players(planets)), True, (0, 0, 0)), (l//2+40,10))
    # screen.blit(font.render(("Heat: %s" % int(planets[0].heat)), True, (0, 0, 0)), (l-100,10))

    pygame.display.flip()

