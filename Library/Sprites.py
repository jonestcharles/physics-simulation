# -*- coding: utf-8 -*-
"""
Created on Mon May 02 19:02:12 2016

@author: jones_000
"""
import pygame as pg
import numpy as np
import vector
import random as rand
import Body

class PlanetSprite(pg.sprite.Sprite):
    '''Planet Sprite object for PyGame
    
    Attributes
    ----------
    pixels_per_AU : float
        the scale used to adjust AU to pixels for pygame
        
    screen_size : float
        the size of the pygame window
        
    image_file : 
        the png image used to represent the sprite
        
    body : GravBody
        the GravBody used to drive the sim and update the sprite's position
    '''
    
    def __init__(self,pixels_per_AU=None,screen_size=None,image_file=None,body=None):
        
        pg.sprite.Sprite.__init__(self)
        self.pixels_per_AU = pixels_per_AU
        self.screen_size = screen_size
        self.image = pg.image.load(image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.body = body
        self.update()
        
    def update(self):
        '''This updates the Sprite's position with the GravBody Position'''
        self.rect.x = (self.body.position.x*self.pixels_per_AU) + self.screen_size[0]/2.
        self.rect.y = (self.screen_size[1]/2. - (self.body.position.y*self.pixels_per_AU))
        
class WarheadSprite(pg.sprite.Sprite):
    '''Warhead Sprite object for PyGame
    
    Attributes
    ----------
    pixels_per_AU : float
        the scale used to adjust AU to pixels for pygame
        
    screen_size : float
        the size of the pygame window
        
    launcher : PlanetSprite
        the Planet launching the warhead
    '''
    
    def __init__(self,pixels_per_AU=None,screen_size=None,launcher=None):
        
        pg.sprite.Sprite.__init__(self)
        self.pixels_per_AU = pixels_per_AU
        self.screen_size = screen_size
        self.image = pg.image.load('warhead.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        '''Position is that of launcher'''
        self.pos = vector.Vector(float(launcher.rect.x),float(launcher.rect.y),z=0.0) 
        
        '''Velocity'''
        self.p = vector.Vector(self.screen_size[0]/2,self.screen_size[1]/2,z=0.0)
        self.velocity = self.p - self.pos
        self.r = 0.4

        self.update()        
        
    def update(self):
        '''Updates the Sprite's Position, deletes if it leaves screen'''
        
        self.pos.x += self.r*np.cos(self.velocity.theta)
        self.pos.y += self.r*np.sin(self.velocity.theta)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)        

        if self.rect.x >= self.screen_size[0]:
            self.kill()
        if self.rect.x <= 0:
            self.kill()
            
        if self.rect.y >= self.screen_size[1]:
            self.kill()
        if self.rect.y <= 0:
            self.kill()
            
    def steer(self,flag):
        '''Takes in a direction flag and steers warhead'''
        if flag == 'right':
            self.velocity.theta += np.pi/180.
        if flag == 'left':
            self.velocity.theta -= np.pi/180.
            
    def accelerate(self):
        '''Accelerates the Sprite'''
        self.r += 0.001

    def decelerate(self):
        '''Decelerates Sprite'''
        self.r -= 0.001

class DefenseSprite(pg.sprite.Sprite):
    '''Defensive Cannon Sprite object for PyGame
    
    Attributes
    ----------
    pixels_per_AU : float
        the scale used to adjust AU to pixels for pygame
        
    screen_size : float
        the size of the pygame window
        
    launcher : PlanetSprite
        the Planet launching the warhead
        
    target : Sprite
        the Sprite that is the target
    '''
    
    def __init__(self,pixels_per_AU=None,screen_size=None,launcher=None,target=None):
        
        pg.sprite.Sprite.__init__(self)
        self.pixels_per_AU = pixels_per_AU
        self.screen_size = screen_size
        self.image = pg.image.load('defense.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        '''Position is that of launcher'''
        self.pos = vector.Vector(float(launcher.rect.x),float(launcher.rect.y),z=0.0) 
        
        '''Velocity'''
        self.tar = vector.Vector(float(target.rect.x),float(target.rect.y),z=0.0)
        self.velocity = self.tar - self.pos
        self.r = 2.

        self.update()

    def update(self):
        '''Updates the Sprite's Position, deletes if it leaves screen'''
        
        self.pos.x += self.r*np.cos(self.velocity.theta)
        self.pos.y += self.r*np.sin(self.velocity.theta)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)        
    
        if self.rect.x >= self.screen_size[0]:
            self.kill()
        if self.rect.x <= 0:
            self.kill()
                
        if self.rect.y >= self.screen_size[1]:
            self.kill()
        if self.rect.y <= 0:
            self.kill()

class ExplosionSprite(pg.sprite.Sprite):
    '''Explosion Animation for Impacts
    
     Attributes
    ----------
    pixels_per_AU : float
        the scale used to adjust AU to pixels for pygame
        
    screen_size : float
        the size of the pygame window
        
    destroyed : Sprite
        the Sprite that is destroyed
    '''

    def __init__(self,pixels_per_AU=None,screen_size=None,destroyed=None):
        
        pg.sprite.Sprite.__init__(self)
        self.pixels_per_AU = pixels_per_AU
        self.screen_size = screen_size
        self.image = pg.image.load('explosion.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.count = 0
        '''Place at Location of Destroyed Sprite'''
        self.rect.x = destroyed.rect.x
        self.rect.y = destroyed.rect.y
        
    def update(self):
        '''Kills Sprite When Updated'''
        self.count += 1
        if self.count == 10:
            self.kill()
        
class AsteroidSprite(pg.sprite.Sprite):
    '''Asteroid class for asteroids in pygame
    
    Attributes
    ----------
    pixels_per_AU : float
        the scale used to adjust AU to pixels for pygame
        
    screen_size : float
        the size of the pygame window
        
    image_file : 
        the png image used to represent the sprite
    '''
    
    def __init__(self,pixels_per_AU=None,screen_size=None):
        
        pg.sprite.Sprite.__init__(self)
        self.pixels_per_AU = pixels_per_AU
        self.screen_size = screen_size
        self.image = pg.image.load('asteroid.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        '''Create Random GravBodies'''
        mass = 0.0
        index = rand.randint(1,4)
        if index == 1:
            position = vector.Vector(x=rand.uniform(-6,6),y=5.99,z=0.0)
            velocity = vector.Vector(r=5*np.pi,theta=(rand.uniform(180,360)*np.pi/180),phi=np.pi/2.)
        if index == 2:
            position = vector.Vector(x=rand.uniform(-6,6),y=-5.99,z=0.0)
            velocity = vector.Vector(r=5*np.pi,theta=(rand.uniform(0,180)*np.pi/180),phi=np.pi/2.)
        if index == 3:
            position = vector.Vector(x=-5.99,y=rand.uniform(-6,6),z=0.0)
            velocity = vector.Vector(r=5*np.pi,theta=(rand.uniform(270,450)*np.pi/180),phi=np.pi/2.)
        if index == 4:
            position = vector.Vector(x=5.99,y=rand.uniform(-6,6),z=0.0)
            velocity = vector.Vector(r=5*np.pi,theta=(rand.uniform(90,270)*np.pi/180),phi=np.pi/2.)
        self.body = Body.GravBody(mass,position,velocity)
        self.update()
        
    def update(self):
        '''This updates the Sprite's position with the GravBody Position'''
        self.rect.x = (self.body.position.x*self.pixels_per_AU) + self.screen_size[0]/2.
        self.rect.y = (self.screen_size[1]/2. - (self.body.position.y*self.pixels_per_AU))
        
        if self.rect.x >= self.screen_size[0]:
            self.kill()
        if self.rect.x <= 0:
            self.kill()
                
        if self.rect.y >= self.screen_size[1]:
            self.kill()
        if self.rect.y <= 0:
            self.kill()
