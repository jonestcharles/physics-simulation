# -*- coding: utf-8 -*-
"""
Created on Mon May 02 18:55:59 2016

@author: jones_000
"""

import vector
import Body
import numpy as np
import Simulation
import Physics
import Solver

class SolarModel(object):
    '''Model Class for Pygame with NBody physics'''
    
    def __init__(self):
        
        '''Build Grav Bodies'''
        ms = 9. 
        sunr = vector.Vector(0.,0.,0.)
        sunv = vector.Vector(0.,-0.6*np.pi/ms,0.)
        self.sun = Body.GravBody(ms,sunr,sunv)
        
        me = 0.1 
        earthr = vector.Vector(1.,0.,0.)
        earthv = vector.Vector(0.,6.*np.pi,0.)
        self.earth = Body.GravBody(me,earthr,earthv)
        
        mr5 = 0.1 
        rigel5r = vector.Vector(5.,0.,0.)
        rigel5v = vector.Vector(0.,2.*np.pi*np.sqrt(me+ms)/np.sqrt(5.),0.)
        self.rigel5 = Body.GravBody(mr5,rigel5r,rigel5v)
        
        '''Build Sim'''
        planets = [self.sun,self.earth,self.rigel5]
        solver = Solver.RK4(0.01)
        physics = Physics.NBody(solver,G=4.*np.pi**2.)
        self.sim = Simulation.OrbitSim(physics=physics,body=planets,apnd=False)
        
    def advance(self,time):
        '''Advances the sim one time step
        
        Parameters
        ----------
        time : float
            one time step for one pygame frame'''
        self.sim.advance(time)