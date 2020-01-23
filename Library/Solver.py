# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:47:10 2016

@author: jone0208
"""

class Solver(object):
    '''Parent Class for solvers
    
    Attributes
    ----------
    stepsize : float
        the independent variable stepsize
    '''
    
    def __init__(self,stepsize=None):
        
        self.stepsize = stepsize
        
class Euler(Solver):
    '''Euler approximation method for a diff eq
    
    Attributes
    ----------
    stepsize : float
        the independent variable step size
        
    diff_eq : callable
        the right hand side of the diff eq to be solved
    '''
    
    def __init__(self,stepsize=None):
        
        Solver.__init__(self,stepsize)
        
    def advance(self,F,x):
        '''Advances diff eq to next step
        
        Paramters
        ---------
        F : array, float
            the solution at the preceding step
            
        x : float
            the independent variable at the last time step
        
        Returns
        -------
        Fnext: array, float
            the solution at the new step
        
        xnext : float
            the independent variable advanced one step
        '''
        Fnext = F + self.diff_eq(F,x)*self.stepsize
        xnext = x + self.stepsize
        return Fnext, xnext
        
class RK2(Solver):
    '''Runge-Kutta second degree approximation method
    
    Attributes
    ----------
    stepsize : float
        the independent variable step size
        
    diff_eq : callable
        the right hand side of the diff eq to be solved
    '''
    
    def __init__(self,stepsize=None):
        
        Solver.__init__(self,stepsize)
        
    def advance(self,F,x):
        '''Advances diff eq to next step
        
        Paramters
        ---------
        F : array, float
            the solution at the preceding step
            
        x : float
            the independent variable at the last time step
        
        Returns
        -------
        Fnext: array, float
            the solution at the new step
        
        xnext : float
            the independent variable advanced one step
        '''
        k1 = self.diff_eq(F,x)
        k2 = self.diff_eq(F+0.5*k1*self.stepsize,x+0.5*self.stepsize)
        
        Fnext = F + k2*self.stepsize
        xnext = x + self.stepsize
        return Fnext, xnext
        
class RK4(Solver):
    '''Runge-Kutta fourth degree approximation method
    
    Attributes
    ----------
    stepsize : float
        the independent variable step size
        
    diff_eq : callable
        the right hand side of the diff eq to be solved
    '''
    
    def __init__(self,stepsize=None):
        
        Solver.__init__(self,stepsize)
        
    def advance(self,F,x):
        '''Advances diff eq to next step
        
        Paramters
        ---------
        F : array, float
            the solution at the preceding step
            
        x : float
            the independent variable at the last time step
        
        Returns
        -------
        Fnext: array, float
            the solution at the new step
        
        xnext : float
            the independent variable advanced one step
        '''
        k1 = self.diff_eq(F,x)
        k2 = self.diff_eq(F+0.5*k1*self.stepsize,x+0.5*self.stepsize)
        k3 = self.diff_eq(F+0.5*k2*self.stepsize,x+0.5*self.stepsize)
        k4 = self.diff_eq(F+k3*self.stepsize,x+self.stepsize)
        
        Fnext = F + (self.stepsize/6.)*(k1+(2.*k2)+(2.*k3)+k4)
        xnext = x + self.stepsize
        return Fnext, xnext
        
        