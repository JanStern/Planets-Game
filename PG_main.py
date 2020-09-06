import numpy as np 
from numpy.random import randint as rnd

import PG_backend, PG_frontend, PG_loading_screen

import pygame, time,os,pickle



# init #########################################################################
pygame.init()
clock = pygame.time.Clock()
clock.tick(60)


# setup #########################################################################
infoObject = pygame.display.Info()
l = infoObject.current_w
h = infoObject.current_h

l = int(l/2)
h = int(h/2)

# class ####################################################
class planet(object):

    def __init__(self):
        self.x=rnd(0,l)
        self.y=rnd(0,h)
        self.x_vel=0
        self.y_vel=0
        self.mas=rnd(10,200)
        self.heat=rnd(0,100)

    def startConditions(self,x,y,x_vel,y_vel,mas,heat):
        self.x=x
        self.y=y
        self.x_vel=x_vel
        self.y_vel=y_vel
        self.mas=mas
        self.heat=heat

# functions ###############################################
def setup():
    planets[0].startConditions(l//2,h//2,0,0,100,0)
    for i in range(10):
        planets[-1-i].mas=0

def pickle_out_func(N):
    try:
        pickle_in = open("highscore.pickle","rb")
        highscore = pickle.load(pickle_in)
        pickle_in.clos()
    except:
        highscore = 1

    if(highscore < N-2):
        pickle_out = open("highscore.pickle","wb")
        pickle.dump(N-2,pickle_out)
        pickle_out.close()

def pickle_in_func(value):
    try:
        pickle_in = open("highscore.pickle","rb")
        value = pickle.load(pickle_in)
        pickle_in.close()
        return value
    except:
        return 0




# main ################################################

PG_loading_screen.main(l,h)


screen = pygame.display.set_mode((l,h))
done = False
started = False
next_lvl = False
begin = False

N = 3
pickle_out_func(N)
dt = 0.1



planets = [planet() for i in range(N+10)]
setup()


while not done: 

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            if (pos[0]>l//2-100 and pos[1]>h//2-100 and pos[0]<l//2+150 and pos[1]<h//2-40 and not started):
                started = True
                planets = [planet() for i in range(N+10)]
                setup()
                PG_frontend.fade(screen)        
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            if not started:
                planets = [planet() for i in range(N+10)]
                setup()

    if (pos[0]>l//2-20 and pos[1]>h//2-20 and pos[0]<l//2+20 and pos[1]<h//2+20 and not begin and started):
        begin=True
        screen.fill((255,255,255))
        font = pygame.font.SysFont("microsoftyibaiti", int(l/10))
        screen.blit(font.render("GO", True, (0, 0, 0)), (l//2-40,h//2-40))
        pygame.display.flip()
        time.sleep(0.3)


    if next_lvl:
        N += 1
        pickle_out_func(N)
        dt+=0.01
        planets = [planet() for i in range(N+10)]
        setup()
        next_lvl = not next_lvl
        begin = False

    if not started:
        # calculations
        PG_backend.start(planets,dt,l,h)
        #visuals
        highscore = pickle_in_func(N)
        PG_frontend.start(planets,screen,l,h,highscore)

    else:
        #back
        if begin: PG_backend.main(planets,dt,l,h)
        #visuals
        PG_frontend.main(planets,screen,l,h)
        
        next_lvl = PG_frontend.victory(planets,screen,l,h)
        started = PG_frontend.death(planets,screen,l,h,N)
        if not started:  
            N=2
            next_lvl = True





# better collision  DONE
# Highscore DONE

# Specials
# graphics
# portals
# music

    
