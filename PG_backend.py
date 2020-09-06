import numpy as np 
from numpy.random import randint as rnd

import pygame, time,os


def get_distance(p1,p2):
    return ((p1.x-p2.x)**2 + (p1.y-p2.y)**2) ** (1/2)

def getAngel_to_horizontal(x1,y1,x2,y2):
    if (x2 > x1 and y2 > y1):
        alpha = np.arctan((y2-y1)/(x2-x1))
    elif(x2 < x1 and y2 > y1):
        alpha = np.arctan((y2-y1)/(x1-x2))
    elif(x2 < x1 and y2 < y1):
        alpha = np.arctan((y1-y2)/(x1-x2))
    elif(x2 > x1 and y2 < y1):
        alpha = np.arctan((y1-y2)/(x2-x1))
    elif(x2==x1):
        alpha=np.pi/2
    elif(y2==y1):
        alpha=0    
    return alpha


def calc_new_vel(p1,p2,dt):

    distance = get_distance(p1,p2)

    if (p1.mas!=0 and p2.mas!=0  and (distance > p1.mas**(2/3)/4 or distance > p2.mas**(2/3)/4)):           
        force = (p1.mas*p2.mas)/(distance**2)
        alpha = getAngel_to_horizontal(p1.x, p1.y, p2.x, p2.y)   

        if (p2.x >= p1.x and p2.y >= p1.y):
            fx = np.cos(alpha)*force
            fy = np.sin(alpha)*force
        elif(p2.x < p1.x and p2.y > p1.y):
            fx = -np.cos(alpha)*force
            fy = np.sin(alpha)*force
        elif(p2.x <= p1.x and p2.y <= p1.y):
            fx = -np.cos(alpha)*force
            fy = -np.sin(alpha)*force
        elif(p2.x > p1.x and p2.y < p1.y):
            fx = np.cos(alpha)*force
            fy = -np.sin(alpha)*force
        
        p1.x_vel += fx/p1.mas*dt
        p1.y_vel += fy/p1.mas*dt




def collison(p1,p2,planets):
    if (p1.mas!=0 and p2.mas!=0):           

        distance = get_distance(p1,p2)
        
        if (distance < p1.mas**(2/3)/2 or distance < p2.mas**(2/3)/2):
            Momentum1_x = p1.x_vel*p1.mas
            Momentum1_y = p1.y_vel*p1.mas
            Momentum2_x = p2.x_vel*p2.mas
            Momentum2_y = p2.y_vel*p2.mas

            E1=1/2 * p1.mas * (p1.x_vel**2 + p1.y_vel**2)
            E2=1/2 * p2.mas * (p2.x_vel**2 + p2.y_vel**2)

            deltaM_x = Momentum1_x + Momentum2_x
            deltaM_y = Momentum1_y + Momentum2_y
            deltaE = np.abs(E1-E2)

            if (abs(Momentum1_x)+abs(Momentum1_y) > abs(Momentum2_x)+abs(Momentum2_y)):
                pd = p1
                pl = p2
            else: 
                pd = p2
                pl = p1

            pd.mas += 0.9*pl.mas
            pd.heat += pl.heat + E1 + E2 - deltaE

            pd.x_vel = deltaM_x/pd.mas
            pd.y_vel = deltaM_y/pd.mas

        
            new_planets = rnd(3,11)
            radius = pd.mas**(2/3)
            for i in range(new_planets):
                planets[-1-i].mas = rnd(0,int(pl.mas*0.1))
                planets[-1-i].heat = rnd(100,400)

                planets[-1-i].x = pd.x+rnd(-radius,radius)
                if (planets[-1-i].x>pd.x): planets[-1-i].x_vel = 10/rnd(10,1000) 
                else: planets[-1-i].x_vel = -10/rnd(10,1000)

                planets[-1-i].y = pd.y+rnd(-radius,radius) 
                if (planets[-1-i].y>pd.y): planets[-1-i].y_vel = 10/rnd(10,1000) 
                else: planets[-1-i].y_vel = -10/rnd(10,1000)

            
            pl.mas=0
            pl.heat=0
            pl.x_vel=0
            pl.y_vel=0

def small_collision(p1,p2):
    if (p1.mas!=0 and p2.mas!=0):           

        distance = get_distance(p1,p2)
        
        if (distance < p1.mas**(2/3)/4 ):

            E1=1/2 * p1.mas * (p1.x_vel**2 + p1.y_vel**2)
            E2=1/2 * p2.mas * (p2.x_vel**2 + p2.y_vel**2)

            deltaE = np.abs(E1-E2)

            pd = p1
            pl = p2   

            pd.mas += 0.9*pl.mas
            pd.heat += pl.heat + E1 + E2 - deltaE
            
            pl.mas=0
            pl.heat=0
            pl.x_vel=0
            pl.y_vel=0



def accelerate_player(planets,dt,l,h):

    pos = pygame.mouse.get_pos()
    if (pos[0]>5 and pos[0]<l-5 and pos[1]>5 and pos[1]<h-5):
            
        distance =  ((planets[0].x-pos[0])**2 + (planets[0].y-pos[1])**2) ** (1/2)

        if (distance > planets[0].mas**(2/3) and planets[0].mas!=0):
            force = distance**(1/2)
            alpha = getAngel_to_horizontal(planets[0].x, planets[0].y, pos[0], pos[1])   

            if (pos[0] >= planets[0].x and pos[1] >= planets[0].y):
                fx = np.cos(alpha)*force
                fy = np.sin(alpha)*force
            elif(pos[0] < planets[0].x and pos[1] > planets[0].y):
                fx = -np.cos(alpha)*force
                fy = np.sin(alpha)*force
            elif(pos[0] <= planets[0].x and pos[1] <= planets[0].y):
                fx = -np.cos(alpha)*force
                fy = -np.sin(alpha)*force
            elif(pos[0] > planets[0].x and pos[1] < planets[0].y):
                fx = np.cos(alpha)*force
                fy = -np.sin(alpha)*force
            
            planets[0].x_vel += fx/(planets[0].mas**(3/5))*dt
            planets[0].y_vel += fy/(planets[0].mas**(3/5))*dt




def main(planets,dt,l,h):
    accelerate_player(planets,dt,l,h)

    for i in range(len(planets)):
        for k in range(len(planets)):
            if(k!=i):
                calc_new_vel(planets[k],planets[i],dt)
    
    for i in range(len(planets)):
        planets[i].x += planets[i].x_vel*dt
        planets[i].y += planets[i].y_vel*dt
        if (planets[i].heat>0): planets[i].heat *= 0.999
        if(planets[i].x<0 or planets[i].x>l or planets[i].y<0 or planets[i].y>h):
            planets[i].mas=0

    for i in range(len(planets)-10):
        for k in range(len(planets)-10):
            if(k!=i):
                collison(planets[k],planets[i],planets)
        for k in range(10):
            small_collision(planets[i],planets[-1-k])        



def start(planets,dt,l,h):
    accelerate_player(planets,dt,l,h)

    for i in range(len(planets)):
        for k in range(len(planets)):
            if(k!=i):
                calc_new_vel(planets[k],planets[i],dt)
    
    for i in range(len(planets)):
        planets[i].x += planets[i].x_vel*dt
        planets[i].y += planets[i].y_vel*dt
        if(planets[i].x<0):
            planets[i].x_vel *=0.1
            planets[i].x = l
        elif(planets[i].x>l): 
            planets[i].x_vel *=0.1
            planets[i].x = 0          
        elif(planets[i].y<0):
            planets[i].y_vel *=0.1
            planets[i].y = h
        elif(planets[i].y>h):
            planets[i].y_vel *=0.1
            planets[i].y = 0

        

# border