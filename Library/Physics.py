# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:47:11 2016

@author: jone0208
"""
import numpy as np
import vector

class Physics(object):
    '''Physics parent class
    
    Attributes
    ----------
    solver : callable
        the approximation technique object
    '''
    
    def __init__(self,solver):
        
        self.solver = solver
        solver.diff_eq = self.diff_eq
        
    def advance(self,body,time):
        '''Advances the sim through the solver
        
        Parameters
        ----------
        body : list, Gravbody
            the list of bodies to be advanced
            
        time : float
            the time variable for a diff eq; tn
            
        Returns
        -------
        body : list, Gravbody
            the new Gravbodies after advancement
            
        time : float
            the new time; tn+1
        '''        
        F = np.array([self.serialize(b) for b in body])
        self.m_list = [b.mass for b in body]
        F, time = self.solver.advance(F,time)
        body = [self.deserialize(b,f) for b,f in zip(body,F)]
        return body, time
        
    def serialize(self,body):
        '''Function that diassembles a body into a matrix
        
        Parameters
        ----------
        body : Gravbody
            the Gravbody to be serialized
        
        Returns
        -------
        array of body's attributes
        '''
        x = body.position.x
        y = body.position.y
        z = body.position.z
        vx = body.velocity.x
        vy = body.velocity.y
        vz = body.velocity.z
        return np.array([x,y,z,vx,vy,vz])
        
    def deserialize(self,body,F):
        '''Function that reassembles an advanced GravBody
        
        Parameters
        ----------
        body : Gravbody
            the body to be reassembled with updated values
            
        F : array, float
            the array from solver with updated values
            
        Returns
        -------
        body : GravBody
            the Gravbody with updated values
        '''
        body.position.x = F[0]
        body.position.y = F[1]
        body.position.z = F[2]
        body.velocity.x = F[3]
        body.velocity.y = F[4]
        body.velocity.z = F[5]
        return body
        
class NBody(Physics):
    '''NBody Simulator
    
    Attributes
    ----------
    solver : solver
        the approximation technique object
        
    G : float
        the gravitational constant, default -6.67*10^-11 m^3/kgs^2
    '''
    
    def __init__(self,solver=None,G=6.67*10**-11):
        
        self.G = G
        Physics.__init__(self,solver)
        
    def diff_eq(self,F,t):
        '''The Physics of an NBody Sim
        
        Parameters
        ----------
        F : array, float
            the array of positions and velocities of bodies
        
        t : float
            the independent variable (time) to be advanced
            
        Returns
        -------
        f : array, floats
            the results of the diff eqs for each body
        '''
        pos = F[:,:3]
        vel = F[:,3:]
        drdt = vel
        dvdt = np.zeros_like(drdt)
        for j in np.arange(F.shape[0]):
            us = pos[j,:]
            m = np.delete(self.m_list,j)
            them = np.delete(pos,j,axis=0)
            diff = them - us
            den = np.sum(diff**2,axis=1)**(-3./2.)
            trans = m*diff.T*den
            Trans = self.G*np.sum(trans.T,axis=0)
            dvdt[j] = Trans
        f = np.append(drdt,dvdt,axis=1)
        return f

class CentralGravity(Physics):
    '''Physics of a gravitational field GM/y^2 with a central attractor

    Attributes
    ----------
    solver : solver
        the approximation technique object
        
    G : float
        the gravitational constant, default -.67*10^-11 m^3/kgs^2
        
    M : float
        the mass of the central attractor, default mass of earth
    ''' 

    def __init__(self,solver=None,G=6.67*10**-11,M=5.972*10**24):
        
        self.M = M
        self.G = G
        Physics.__init__(self,solver)
        
    def diff_eq(self,F,t):
        '''The Physics of an NBody Sim
        
        Parameters
        ----------
        F : array, float
            the array of positions and velocities of bodies
        
        t : float
            the independent variable (time) to be advanced
            
        Returns
        -------
        array, floats
            the results of the diff eqs for each body
        '''
        pos = F[:,:3]
        drdt = F[:,3:]
        mag_pos = np.sum(pos**2,axis=1)**(-3./2.)
        trans = pos.T*mag_pos
        Trans = trans.T
        dvdt = -(Trans*self.G*self.M)
        return np.append(drdt,dvdt,axis=1)
        
    def energy(self,bodies):
        '''Takes a list of bodies and calculates the total energy for each'''
        E_list = []
        for b in bodies:
            KE = 0.5*b[0].mass*b[0].velocity.r**2
            PE = -(self.G*self.M*b[0].mass)/(b[0].position.r)
            E = KE + PE
            E_list.append(E)
        return E_list
        
class NewtonCooling(Physics):
    '''Physics of Cooling diff eq
    
    Attributes
    ----------
    solver : solver
        the approximation technique object
        
    Ta : float
        the ambient temperature
        
    k : float
        the cooling coefficient
    '''
    
    def __init__(self,solver=None,Ta=None,k=None):
        
        self.Ta = Ta
        self.k = k
        Physics.__init__(self,solver)
        
    def diff_eq(self,T,t):
        '''The Physics of an NBody Sim
        
        Parameters
        ----------
        T : array, float
            the array of temperatures of bodies
        
        t : float
            the independent variable (time) to be advanced
            
        Returns
        -------
        array, floats
            the results of the diff eqs for each body
        '''
        return (self.Ta-T)*self.k
    
    def serialize(self,body):
        '''Function that diassembles a body into a matrix
        
        Parameters
        ----------
        body : ThermalBody
            the ThermalBody to be serialized
        
        Returns
        -------
        array of body's attributes
        '''
        temperature = body.temperature
        return temperature
        
    def deserialize(self,body,F):
        '''Function that reassembles an advanced GravBody
        
        Parameters
        ----------
        body : ThermalBody
            the ThermalBody to be reassembled with updated values
            
        F : array, float
            the array from solver with updated values
            
        Returns
        -------
        body : ThermalBody
            the ThermalBody with updated values
        '''
        body.temperature = F
        return body

class UniformGravity(Physics):
    '''Physics of a uniform gravitational field

    Attributes
    ----------
    solver : solver
        the approximation technique object
        
    g : vector
        the gravitational acceleration vector, constant at a.y=-9.81 m/2^s
        
    c : float
        the drag coefficient c=yd^2 d=diameter of ball y=0.25 Ns^2/m^4

    ''' 

    def __init__(self,solver=None,g=vector.Vector(0,-9.81,0),c=0):
        
        self.g = g
        self.c = c
        Physics.__init__(self,solver)
        
    def diff_eq(self,F,t):
        '''The Physics of an NBody Sim
        
        Parameters
        ----------
        F : array, float
            the array of positions and velocities of bodies
        
        t : float
            the independent variable (time) to be advanced
            
        Returns
        -------
        array, floats
            the results of the diff eqs for each body
        '''
        dxdt = F[3]
        dvxdt = self.g.x - ((self.c/self.mass)*(F[3]**2))
        dydt = F[4]
        dvydt = self.g.y - ((self.c/self.mass)*(F[4]**2))
        dzdt = F[5]
        dvzdt = self.g.z - ((self.c/self.mass)*(F[5]**2))
        return np.array([dxdt,dydt,dzdt,dvxdt,dvydt,dvzdt])
        
    def serialize(self,body):
        '''Function that diassembles a body into a matrix
        
        Parameters
        ----------
        body : Gravbody
            the Gravbody to be serialized
        
        Returns
        -------
        array of body's attributes
        '''
        self.mass = body.mass
        x = body.position.x
        y = body.position.y
        z = body.position.z
        vx = body.velocity.x
        vy = body.velocity.y
        vz = body.velocity.z
        return np.array([x,y,z,vx,vy,vz])