# -*- coding: utf-8 -*-
"""
Created on Mon May 02 18:33:12 2016

@author: jones_000
"""

import Sprites
import pygame as pg
import Model

'''Define some colors'''
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)


class App(object):
    
    def __init__(self):
           
        pg.init()

        '''Animation Parameters'''
        self.years_per_tick = 0.0001
        self.pixels_per_AU = 1000./12.
        
        '''Initialize display surface'''
        self.screen_size = (1000,1000)
        self.screen = pg.display.set_mode((int(self.screen_size[0]),
                                           int(self.screen_size[1])))
        self.background = pg.image.load('spacebackground.png').convert_alpha()
        
        self.model = Model.SolarModel()
        
        '''Build Sprites'''
        self.sun = Sprites.PlanetSprite(self.pixels_per_AU,self.screen_size,
                                        'sun.png',self.model.sun)
        self.earth = Sprites.PlanetSprite(self.pixels_per_AU,self.screen_size,
                                          'earth.png',self.model.earth)
        self.rigel5 = Sprites.PlanetSprite(self.pixels_per_AU,self.screen_size,
                                           'rigel5.png',self.model.rigel5)
        self.all = pg.sprite.RenderUpdates([self.sun,self.earth,self.rigel5])                                   
        self.warheadgrp = pg.sprite.RenderUpdates([])
        self.defensegrp = pg.sprite.RenderUpdates([])
        self.asteroidgrp = pg.sprite.RenderUpdates([])
                                           
        '''Set up the timer'''        
        self.ticks = pg.time.get_ticks()
        
        self.screen.blit(self.background,(0,0))
        self.all.clear(self.screen,self.background)
        planets = self.all.draw(self.screen)
        pg.display.update()

        '''Set up Key Flags'''
        self.ra = False
        self.la = False
        self.ua = False 
        self.da = False                   
                                                                                    
    def run(self):
        '''Main animation loop'''
    
        self.end_game = False
        
        '''Set Event and Timer For Defense Cannon'''
        DEFENSE = pg.USEREVENT + 1
        pg.time.set_timer(DEFENSE,1000)
        ASTEROID = pg.USEREVENT + 2
        pg.time.set_timer(ASTEROID,5000)
                                           
        while not self.end_game:
                        
            '''Process events'''
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:                
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        
                    '''Creates Warhead'''    
                    if event.key == pg.K_SPACE and len(self.warheadgrp) == 0:
                        self.warhead_launch()
                    
                    '''Steer Warhead'''
                    if event.key == pg.K_RIGHT and len(self.warheadgrp) == 1:
                        self.ra = True 
                    if event.key == pg.K_LEFT and len(self.warheadgrp) == 1:
                        self.la = True
                    if event.key == pg.K_UP and len(self.warheadgrp) == 1:
                        self.ua = True
                    if event.key == pg.K_DOWN and len(self.warheadgrp) == 1:
                        self.da = True    

                elif event.type == pg.KEYUP:
                    '''Stop Steering'''
                    if event.key == pg.K_RIGHT:
                        self.ra = False
                    if event.key == pg.K_LEFT:
                        self.la = False
                    if event.key == pg.K_UP:
                        self.ua = False
                    if event.key == pg.K_DOWN:
                        self.da = False
                
                elif event.type == DEFENSE:
                    if len(self.defensegrp) < 5:
                        self.defense_cannon()
                        
                elif event.type == ASTEROID:
                    self.make_roid()
                        
            '''Check Flags and Steer Warhead'''            
            if self.ra:
                self.warhead.steer('right')
            if self.la:
                self.warhead.steer('left')
            if self.ua:
                self.warhead.accelerate()
            if self.da:
                self.warhead.decelerate()
                                                             
            self.advance()
        
        countFont=pg.font.Font(None,36)
        ticks = pg.time.get_ticks()
        end_time = (ticks - self.ticks)*self.years_per_tick                            
        statusText=countFont.render('You Have Destroyed the Puny Earthlings in %f years'%end_time,
                                    True,(52, 152, 219),(231,230,33))
        self.screen.blit(statusText,(200,400))
        pg.display.flip()

    def advance(self):
        '''Advance the simulation one frame'''
            
        '''Calculate the time step'''
        ticks = pg.time.get_ticks()
        elapsed_time = (ticks - self.ticks)*self.years_per_tick

        '''Advance the simulation'''
        self.model.advance(time=elapsed_time)
        
        '''Update the display'''
        self.screen.blit(self.background,(0,0))
        self.all.update()
        
        '''Test for Warhead-Defense Collisions'''
        impacts = pg.sprite.groupcollide(self.warheadgrp,self.defensegrp,True,True)
        for impact in impacts:
            exp = Sprites.ExplosionSprite(self.pixels_per_AU,
                                                self.screen_size,impact)
            self.all.add(exp)                                    
        
        '''Test for Warhead-Asteroid Collisions'''
        boom = pg.sprite.groupcollide(self.asteroidgrp,self.warheadgrp,True,True)
        for b in boom:
            exp = Sprites.ExplosionSprite(self.pixels_per_AU,
                                                self.screen_size,b)
            self.all.add(exp)
            del self.model.sim.body[3]
            
        '''Test for Defense-Asteroid Collisions'''
        whap = pg.sprite.groupcollide(self.asteroidgrp,self.warheadgrp,True,True)
        for w in whap:
            self.model.sim.body
            exp = Sprites.ExplosionSprite(self.pixels_per_AU,
                                                self.screen_size,w)
            self.all.add(exp)
            del self.model.sim.body[3] 
              
        '''Test for Warhead-Earth Collision and End Game if Earth is Destroyed'''
        collisions = pg.sprite.spritecollide(self.earth,self.warheadgrp,True)
        if len(collisions) > 0:
            self.end_game = True
            exp = Sprites.ExplosionSprite(self.pixels_per_AU,
                                                self.screen_size,self.earth)
            self.earth.kill()
            self.all.add(exp)
                
        '''Draw'''    
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)

    def warhead_launch(self):
        '''creates and launches a warhead'''
        self.warhead = Sprites.WarheadSprite(self.pixels_per_AU,self.screen_size,
                                                             self.rigel5)
        self.warheadgrp.add(self.warhead)
        self.all.add(self.warhead)
        
    def defense_cannon(self):
        '''fires the defense cannon if warhead is incoming'''
        if len(self.warheadgrp) == 1:
            defense = Sprites.DefenseSprite(self.pixels_per_AU,self.screen_size,
                                            self.earth,self.warhead)
            self.defensegrp.add(defense)
            self.all.add(defense)
    
    def make_roid(self):
        '''generates random asteroid'''
        if len(self.asteroidgrp) == 0:
            self.asteroid = Sprites.AsteroidSprite(self.pixels_per_AU,self.screen_size)
            self.asteroidgrp.add(self.asteroid)
            self.all.add(self.asteroid)
            self.model.sim.body.append(self.asteroid.body)
                                            
        
if __name__=='__main__':
    app = App()
    app.run()    