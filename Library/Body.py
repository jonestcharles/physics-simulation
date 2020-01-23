# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:46:30 2016

@author: jone0208
"""

class ThermalBody(object):
    '''Body class with a temperature
    
    Attributes
    ----------
    temperature : float
        the initial temperature of the thermal body
    '''
    
    def __init__(self,temperature=None):
        
        self.temperature = temperature
        
class GravBody(object):
    '''Body class with mass, height, and velocity
        
    Attributes
    ----------
    mass : float
        the mass of the body in kg
        
    position : Vector
        the initial position vector of the body in m
        
    velocity : Vector
        the initial velocity vector of the body in m/s
    '''
    
    def __init__(self,mass=None,position=None,velocity=None):
        
        self.mass = mass
        self.position = position
        self.velocity = velocity
       