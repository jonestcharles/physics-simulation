# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:48:32 2016

@author: jone0208
"""

import numpy as np
import matplotlib.pyplot as plt #imports needed libraries
import time

def main():
    x = np.arange(-5e6, 5e6, 1)
    time.clock()
    t1 = time.clock()
    y1 = parabola(x, 1, 0, 0)
    t2 = time.clock()
    y2 = loopy_parabola(x, 1, 0, 0)
    t3 = time.clock()
    print(t2-t1,t3-t2)

def parabola(x, a, b, c):
    '''takes inputs and makes a quadratic equation
    
    Parameters
    ----------
    x: array, float
        independent variable array
        
    a: float
        the a of "ax^2 + bx + c"
        
    b: float
        the b of "ax^2 + bx + c"
        
    c: float
        the c of "ax^2 + bx + c"
        
    Returns
    -------
     y: array, float
        array of dependant variables
    '''
    y=a*x**2 + b*x + c #this builds a quadratic equation using inputs

    return y #returns the variables for use
    
def plottit(a, b, title, xlabel, ylabel,legend):
    '''takes a function and plots it
    
    Parameters
    ----------
    a: int32
        a range for the independent variable
        
    b: float
        a quadratic equation
        
    title: str
        Title for the plot
        
    xlabel: str
        label for x axis
        
    ylabel: str
        label for y axis
        
    legend: array, str
        an array of curve name strings
        
    Returns
    -------
    None, plots the inputs
    '''
    plt.plot(a,b) #plots your inputs
    plt.title(title) #sets title and axes labels (below)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)

def loopy_parabola(x, a, b, c):
    '''takes inputs and makes a quadratic equation
    
    Parameters
    ----------
    x: array, float
        independent variable array
        
    a: float
        the a of "ax^2 + bx + c"
        
    b: float
        the b of "ax^2 + bx + c"
        
    c: float
        the c of "ax^2 + bx + c"
        
    Returns
    -------
    y: array, float
        array of dependant variables
    '''
    y=np.zeros(len(x)) #initialize result array
    
    for i in range(len(x)): #loop over x
        y[i] = a*x[i]**2 + b*x[i] + c  #perform calculation
        
    return y #returns the variables for use

if __name__ == "__main__": main() #allows you to test code with run button
