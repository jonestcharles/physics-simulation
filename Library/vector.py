# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:51:46 2016

@author: jone0208
"""
import math
import numpy as np

class Vector(object):
    '''Generic Vector class
    
    Attributes
    ----------
    x :float
        cartesian x component
        
    y : float
        cartesian x component
        
    z : float
        cartesian z component
        
    r : float
        polar radial component
        
    theta : float
        azimuthal angle
        
    phi : float
        polar angle
    '''

    def __init__(self,x=None,y=None,z=None,r=None,theta=None,phi=None):        
        
        if x == None and y == None and x == None:
            self.x = r*math.sin(phi)*math.cos(theta)
            self.y = r*math.sin(phi)*math.sin(theta)
            self.z = r*math.cos(phi)
        elif r == None and theta == None and phi == None:
            self.x = x
            self.y = y
            self.z = z
        
    @property
    def r(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    
    @property
    def theta(self):
        return math.atan2(self.y,self.x)
        
    @property
    def phi(self):
        return math.acos(self.z/self.r)
        
    @property
    def cart(self):
        return np.array([self.x,self.y,self.z])
        
    @r.setter
    def r(self,r):
        theta = self.theta
        phi = self.phi
        
        self.x = r*math.sin(phi)*math.cos(theta)
        self.y = r*math.sin(phi)*math.sin(theta)
        self.z = r*math.cos(phi)
        
    @theta.setter
    def theta(self,theta):
        r = self.r
        phi = self.phi
        
        self.x = r*math.sin(phi)*math.cos(theta)
        self.y = r*math.sin(phi)*math.sin(theta)
        self.z = r*math.cos(phi)
        
    @phi.setter
    def phi(self,phi):
        r = self.r
        theta = self.theta
        
        self.x = r*math.sin(phi)*math.cos(theta)
        self.y = r*math.sin(phi)*math.sin(theta)
        self.z = r*math.cos(phi)
        
    def __add__(self,other):
        '''Vector Addition'''
        return Vector(x=self.x+other.x,y=self.y+other.y,z=self.z+other.z)
        
    def __sub__(self,other):
        '''Vector Subtraction'''
        return Vector(x=self.x-other.x,y=self.y-other.y,z=self.z-other.z)
        
    def __mul__(self,other):
        '''Vector Dot Product'''
        return self.x*other.x+self.y*other.y+self.z*other.z
        
    def __repr__(self):
        '''Returns a description of the Vector'''
        return "Vector(x=%f, y=%f, z=%f)"%(self.x,self.y,self.z)
         
    def rot_z(self,omega):
        '''rotates V around the z axis, new xy plane'''
        H = np.array([[math.cos(omega),math.sin(omega),0.],[-math.sin(omega),
                       math.cos(omega),0.],[0.,0.,1.]])
        V = np.array([[self.x],[self.y],[self.z]])
        Vnew = np.dot(V.T,H)
        self.x = Vnew[0][0]
        self.y = Vnew[0][1]
        self.z = Vnew[0][2]
        
    def rot_y(self,omega):
        '''rotates V around the y axis, new xz plane'''
        H = np.array([[math.cos(omega),0.,math.sin(omega)],[0.,1.,0.],
                       [-math.sin(omega),0.,math.cos(omega)]])
        V = np.array([[self.x],[self.y],[self.z]])
        Vnew = np.dot(V.T,H)
        self.x = Vnew[0][0]
        self.y = Vnew[0][1]
        self.z = Vnew[0][2]
                
    def rot_x(self,omega):
        '''rotates V around the x axis, new yz plane'''
        H = np.array([[1.,0.,0.],[0.,math.cos(omega),math.sin(omega)],
                       [0.,-math.sin(omega),math.cos(omega)]])
        V = np.array([[self.x],[self.y],[self.z]])
        Vnew = np.dot(V.T,H)
        self.x = Vnew[0][0]
        self.y = Vnew[0][1]
        self.z = Vnew[0][2]
        
    def scal_mul(self,scalar):
        self.x = self.x*scalar
        self.y = self.y*scalar
        self.z = self.z*scalar

