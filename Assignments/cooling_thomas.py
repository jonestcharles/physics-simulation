# -*- coding: utf-8 -*-
"""
Created on Tue Feb 02 15:48:57 2016

@author: well8613
"""

import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    k=0.1
    dt=5
    
    t=np.arange(0,math.log(10)/k,0.05)
    T=np.exp(-k*t)
    plt.plot(t,T)
    
    t=np.arange(0,math.log(10)/k,dt)
    plt.plot(t,cooling_euler(k,t,dt))
    plt.title('Temperature')
    plt.xlabel('Time'); plt.ylabel('Temperature (as proportion of T0 - Ta)')
     
    plt.plot(t,cooling_rk2(cooling_diffeq,t,dt,1))     
    plt.legend(['Exact','Euler','RK2'])
    '''
    dt=np.arange(.2,4.2,.2)
    error=np.exp(-k*dt) + k*dt -1
    plt.figure()
    plt.plot(dt,error)
    plt.title('Error with step size')
    plt.xlabel('step size'); plt.ylabel('Error')        
    return
    '''
    
def cooling_rk2(G,t,dt,T0):
    '''rk2 for cooling function
    
     Parameters
    ----------
    G:function
        cooling_diffeq gives the derivative at T
        
    t:array,float
        time/independent variable
        
    dt:float
        time step
    
    T0:float
        initial temperature
        
    Returns
    -------
    T:array,float
        rk2 values for T
    ''' 
    T= 0*t
    T[0]=1
    for i in range(1,len(T)):
        k1 = G(T[i-1],t)
        k2 = G(T[i-1]+k1*dt*0.5,t)
        T[i] = T[i-1] + k2*dt
    return np.array(T)   
    
def cooling_diffeq(T,t):
    '''Provides the slope of the cooling function
    
    Parameters
    ---------
    T: float
        initial temperature
    
    t: array, float
        time/independent variable
        
    Returns
    -------
    slope: float
        derivative at a certain T
    '''
    k=0.1
    slope = -k*T
    return slope

    
def cooling_euler(k,t,dt):
    ''' Approximates the cooling function exp(-kt), using Euler's method
    
    Parameters
    ----------
    k:float
        the cooling constant
        
    t:array,float
        time/independent variable
        
    dt:float
        time step
    
    Returns
    -------
    T:array,float
    ''' 
    T=0*t
    T[0]=1
    for i in range(1,len(T)):
        T[i]=T[i-1]-k*T[i-1]*dt
    return T
   
    
def cooling_taylor(k,t,t_0,n):
    ''' Gives the nth order Talor polynomial for the cooling function exp(-kt)
    
    Parameters
    ----------
    k:float
        the cooling constant
        
    t:array,float
        time/independent variable
        
    t_0:float
        center of Taylor expansion
        
    n:int
        order of taylor polynomial
    
    Returns
    -------
    T:array,float
    '''
    T=1
    for i in range(1,n+1):
        T=T+ ((-k*(t-t_0))**i)/math.factorial(i)
    T=T*np.exp(-k*t_0)
    return T
    
if __name__=="__main__":main()

