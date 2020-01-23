# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:57:53 2016

@author: jone0208
"""

import numpy as np

class GoldenSection(object):
    '''Golden Section Minimizer
    
    Attributes
    ----------
    error : callable
        the error function to be minimized
        
    tl : float
        the left initial guess
        
    tr : float
        the right initial guess
        
    tolerance : float
        tolerance for the error function
    '''
    
    def __init__(self,error,xl=None,xr=None,tolerance=None):
        
        self.error = error
        self.xl = xl
        self.xr = xr
        self.tolerance = tolerance
        self.xm = xl + (xr-xl)*((3.-np.sqrt(5.))/2.)
        
    def do_it(self):
        '''Runs the Golden Section minimization'''
        xr = self.xr
        xl = self.xl
        xm = self.xm
        error_r = self.error(xr)
        error_l = self.error(xl)
        error_m = self.error(xm)
        while (xr - xl) > self.tolerance:           
            if (xm - xl) > (xr - xm):
                xbar = (xr - xl) - 2*(xr - xm)
                xt = xm - xbar
                error_t = self.error(xt)
                
                if error_t < error_m:
                    xr = xm
                    error_r = error_m
                    xm = xt
                    error_m = error_t
                else:
                    xl = xt
                    error_l = error_t
                
            elif (xr - xm) > (xm - xl):
                xbar = (xr - xl) - 2*(xm-xl)
                xt = xm + xbar
                error_t = self.error(xt)
                
                if error_t < error_m:
                    xl = xm
                    error_l = error_m
                    xm = xt
                    error_m = error_t
                else:
                    xr = xt
                    error_r = error_t
        return xm
        
class Bisect(object):
    '''Optimization and parameter search using bisection technique
    
    Attributes
    ----------
    error : callable
        the function that defines the error for your problem
        
    xlow : array, float
        the low guess for the function
        
    xhigh : array, float
        the high guess for the function
    
    tolerance : float
        the tolerance for the error
    '''
    
    def __init__(self,error,xlow=None,xhigh=None,tolerance=None):
        
        self.error = error
        self.xlow = xlow
        self.xhigh = xhigh
        self.tolerance = tolerance

    def do_it(self):
        '''runs the Bisection Search'''
        xmid = self.xlow + (self.xhigh - self.xlow)/2
        while abs(self.error(xmid)) > self.tolerance:
            if self.error(xmid) > 0:
                self.xhigh = xmid
                xmid = self.xlow + (self.xhigh - self.xlow)/2
            if self.error(xmid) < 0:
                self.xlow = xmid
                xmid = self.xlow + (self.xhigh - self.xlow)/2
        return xmid
      
class NewtonMethod(object):
    '''Optimization and parameter search using Newton's Method
    
    Attributes
    ----------
    error : callable
        the function that defines the error for your problem
        
    x1 : array, float
        the initial guess for the function
        
    stepsize : float
        independent variable step size
    
    tolerance : float
        the tolerance for the error
    '''
    
    def __init__(self,error,x1=None,stepsize=None,tolerance=None):
        
        self.error = error
        self.x1 = x1
        self.stepsize = stepsize
        self.tolerance = tolerance
        
    def do_it(self):
        '''Runs Newton's Method search'''
        x1 = self.x1
        while abs(self.error(x1)) > self.tolerance:
            err_deriv = ((self.error(x1+self.stepsize))-self.error(x1))/self.stepsize
            delta = -(self.error(x1))/err_deriv
            x1 = x1 + delta
        return x1
