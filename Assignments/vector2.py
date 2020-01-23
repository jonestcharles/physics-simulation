# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:51:46 2016

@author: jone0208
"""
import math

def main():
    a = Vector(x=3,y=4)
    if a.r == 5:
        print "Passed Magnitude"
    else:
        print "Failed Magnitude"
    a.theta = 0
    if a.x == 5:
        print "Passed theta setter"
    else:
        print "Failed theta setter"
    if a.y == 0:
        print "Passed theta setter"
    else:
        print "Failed theta setter"
    a.r = 10
    if a.x == 10:
        print "Passed r setter"
    else:
        print "Failed r setter"

class Vector(object):
    '''Generic Vector class
    
    Attributes
    ----------
    x :float
        cartesian x component
        
    y : float
        cartesian x component
        
    r : float
        polar radial component
        
    theta : float
        polar azimuthal angle
    '''

    def __init__(self,x=None,y=None,r=None,theta=None): #initiation, setting default settings for variables.  self referencing.

        if r==None and theta==None:         
            self.r = math.sqrt(x**2+y**2)
            self.theta = math.atan2(y,x)
        elif x==None and y==None:
            self.r = r
            self.theta = theta
            
    @property
    def x(self):
        return self.r*math.cos(self.theta)
            
    @property
    def y(self):
        return self.r*math.sin(self.theta)
                
    @x.setter
    def x(self,x):
        y = self.y
        r = self.r
        theta = self.theta
        
        self.r = math.sqrt(x**2+y**2)
        self.theta = math.atan2(y/x)
        
    @y.setter
    def y(self,y):
        x = self.x
        r = self.r
        theta = self.theta
        
        self.r = math.sqrt(x**2+y**2)
        self.theta = math.atan2(y/x)
    
    def __repr__(self):
         return "Vector(r=%f, theta=%f)"%(self.r,self.theta)
         
         
if __name__ == "__main__": main() #allows you to test code with run button

