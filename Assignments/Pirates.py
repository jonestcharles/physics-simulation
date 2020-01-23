# -*- coding: utf-8 -*-
"""
Created on Thu Feb 04 15:20:04 2016

@author: jone0208
"""

import numpy as np
import matplotlib.pyplot as plt
import Plottit

def main():
    a_list = [-4.9, -4.9, -4.9]
    b_list = [1, 3, 5]
    c_list = [2, 2, 2]
    for a,b,c, in zip(a_list,b_list,c_list):
        x = np.arange(0,stoptime(a,b,c),0.005)
        y = Plottit.parabola(x,a,b,c)  
        Plottit.plottit(x,y,"Pirate Tosses","Time","Height [m]")
    plt.legend(["Initial Velocity: 1 m/s", "Initial Velocity; 3 m/s", "Initial Velocity: 5 m/s"])
    return
    
def stoptime(a, b, c):
    '''Calcuates time until 0 of a pirate toss
    
    Parameters
    ----------
    a: float
        Quadratic coefficient
        
    b: float
        Linear Coefficient
        
    c: float
        Constant Coefficient
            
    Returns
    -------
    t = time until the toss skull hits the ground
    '''
    t1 = (-b + np.sqrt(b**2-4*a*c))/(2*a) #Quadratic Equations
    t2 = (-b - np.sqrt(b**2-4*a*c))/(2*a)
    t = max(t1,t2)
    return t
  
if __name__=="__main__":main()