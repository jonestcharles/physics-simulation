# -*- coding: utf-8 -*-
"""
Created on Mon May 02 18:33:12 2016

@author: jones_000
"""

import Sprites
import pygame as pg
import Model

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)


class App(object):
    
    def __init__(self):
           
        pg.init()

        '''Animation Parameters'''
        self.years_per_tick = 0.0001
        self.pixels_per_AU = 800./3.
        
        '''Initialize display surface'''
        self.screen_size = (800,800)
        self.screen = pg.display.set_mode((int(self.screen_size[0]),
                                           int(self.screen_size[1])))
        self.background = pg.Surface(self.screen_size)
        self.background.fill(BLACK)
        
        self.model = Model.SolarModel()
        
        '''Build Sprites'''
        self.sun = Sprites.PlanetSprite(self.pixels_per_AU,self.screen_size,
                                        'sun.png',self.model.sun)
        self.earth = Sprites.PlanetSprite(self.pixels_per_AU,self.screen_size,
                                          'googleearth.png',self.model.earth)
        self.sgroup = pg.sprite.RenderUpdates([self.sun,self.earth])
                                           
        '''Set up the timer'''        
        self.ticks = pg.time.get_ticks()
        
        self.screen.blit(self.background,(0,0))
        self.sgroup.clear(self.screen,self.background)
        dirty = self.sgroup.draw(self.screen)
        pg.display.update(dirty)                    
                                                                                    
    def run(self):
        '''Main animation loop'''
    
        done = False
                                           
        while not done:
                        
            '''Process events'''
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                elif event.type == pg.KEYDOWN:                
                    if event.key == pg.K_ESCAPE:
                        done = True
                        
            self.advance()
                                    
        pg.quit()

    def advance(self):
        '''Advance the simulation one frame'''
            
        '''Calculate the time step'''
        ticks = pg.time.get_ticks()
        elapsed_time = (ticks - self.ticks)*self.years_per_tick

        '''Advance the simulation'''
        self.model.advance(time=elapsed_time)
        
        '''Update the display'''
        self.screen.blit(self.background,(0,0))
        self.sgroup.update()
        dirty = self.sgroup.draw(self.screen)
        
        pg.display.update(dirty)
    
if __name__=='__main__':
    app = App()
    app.run()