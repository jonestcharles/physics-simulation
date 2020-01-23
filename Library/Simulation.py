# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 18:03:59 2016

@author: jones_000
"""
import copy as cp
import numpy as np
import math
import Solver
import Physics
import Body
import vector
import matplotlib.pyplot as plt

class Simulation(object):
    '''Parent Simulation class
    
    Attributes
    ----------
    stop_condition : callable
        sets the stop condition for simulation
        
    physics : Physics
        the physics being simulated with a solver
        
    body : array, GravBody
        the array of bodies with position, velocity, and mass
    '''
    
    def __init__(self,stop_condition=None,physics=None,body=None):
        
        '''Make body a list'''
        if type(body) == list:
            self.body = body
        else:
            self.body = [body]
        self.physics = physics
        self.stop_condition = stop_condition
        
    def get_results(self):
        '''This advances the sim and returns results'''
        body = self.body
        time = 0
        self.bodies = [cp.deepcopy(self.body)]
        self.t = [0]
        while self.stop_condition(self.bodies) == True:
            body, time = self.physics.advance(body,time)
            self.bodies.append(cp.deepcopy(body))
            self.t.append(time)
        return self.t, self.bodies
        
class OrbitSim(Simulation):
    '''Drives the Central Grav sim for orbits
    
    Attributes
    ----------
    stop_condition : callable
        sets the stop condition for simulation
        
    physics : Physics
        the physics being simulated with a solver
        
    body : GravBody
        the body with position, velocity, and mass
    '''
    
    def __init__(self,stop_condition=None,physics=None,body=None,apnd=True):
        
        Simulation.__init__(self,stop_condition,physics,body)
        self.bodies = [cp.deepcopy(self.body)]
        self.t = [0]
        self.apnd = apnd
        
    def get_results(self):
        '''Returns time and bodies lists'''
        return self.t, self.bodies
        
    def advance(self,time=None,step=None):
        '''Advances sim to a certain time or step
        
        Parameters
        ----------
        time : float
            the target time for the sim
            
        step : float
            the number of steps to run
        '''
        if time != None:
            dt = self.physics.solver.stepsize
            time = time - dt
            self.run(self.time_stop(time))
            self.physics.solver.stepsize = time + dt - self.t[-1]
            self.run(self.time_stop(time+dt))
            self.physics.solver.stepsize = dt
        if step != None:
            self.run(self.step_stop(step))
        if time == None and step == None:
            self.run(self.stop_condition)
            
    def step_stop(self,step):
        '''Reference to stop function to end at a certain step'''
        def stop(time,bodies):
            steps = math.floor(time/self.physics.solver.step_size)
            if steps < step:  
                return True
            else:
                return False
        return stop
        
    def time_stop(self,goal):
        '''Reference to a stop function to end at a certain time'''
        def stop(time,bodies):
            if time < goal:
                return True
            else:
                return False
        return stop
            
    def run(self,stop_condition):
        '''Internal run function that advances bodies
        
        Parameters
        ----------
        stop_condition : callable
            the stop function to end the sim
        '''
        time = self.t[-1]
        while stop_condition(time,self.bodies) == True:
            self.body, time = self.physics.advance(self.body,time)
            if self.apnd:
                self.bodies.append(cp.deepcopy(self.body))
                self.t.append(time)
        if not self.apnd:
            self.bodies.append(cp.deepcopy(self.body))
            self.t.append(cp.deepcopy(time))

class BinarySim(OrbitSim):
    '''Takes in Elliptical Inputs and produces a Binary Sim
    
    Attributes
    ----------
    M1 : float
        mass of the first body
        
    M2 : float 
            mass of the second body
    a1 : float
        the semi-major axis of the first body's orbit
        
    e : float
        the orbits' eccentricity
    '''
    
    def __init__(self,M1=None,M2=None,a1=1,e=0,apnd=True):
        
        '''Build GravBodies'''
        self.G = 4*math.pi**2.
        r1p = a1-e*a1
        r2p = -(M1/M2)*r1p
        v1p = math.sqrt(((self.G*M2**3.)/(a1*(M1+M2)**2.))*((1.+e)/(1.-e)))
        v2p = -(M1/M2)*v1p
        r1 = vector.Vector(r1p,0.,0.)
        r2 = vector.Vector(r2p,0.,0.)
        v1 = vector.Vector(0.,v1p,0.)
        v2 = vector.Vector(0.,v2p,0.)
        body1 = Body.GravBody(M1,r1,v1)
        body2 = Body.GravBody(M2,r2,v2)
        
        '''Set up Sim'''
        self.body = [body1,body2]
        solver = Solver.RK2(0.01)
        self.physics = Physics.NBody(solver,self.G)
        self.bodies = [cp.deepcopy(self.body)]
        self.t = [0]
        self.apnd = apnd
            
class ExoSim(BinarySim):
    '''Runs a siim for an exoplant search
    
    Attributes
    ----------
    Ms : float
        mass of the star
        
    Mp : float 
            mass of the plant
    ap : float
        the semi-major axis of the planet's orbit
        
    e : float
        the orbits' eccentricity
        
    Rs : float
        the radius of the star in Solar Radii
    
    Rp : float
        the radius of the planet in Solar Radii
        
    omega : float
        the angle of periastron
        
    i : float
        the angle of inclination
    '''
    
    def __init__(self,Ms=None,Mp=None,ap=None,e=0,Rs=None,Rp=None,omega=None,i=None,apnd=True):
        
        '''Save Values'''
        self.apnd = apnd
        self.Rs = Rs
        self.Rp = Rp
        self.G = 4*math.pi**2.
        self.period = np.sqrt(((ap**3.)*((Ms+Mp)**2.))/Ms**3.)
        
        '''Set up Vectors'''
        rpp = ap-e*ap
        rsp = -(Mp/Ms)*rpp
        vpp = math.sqrt(((self.G*Ms**3.)/(ap*(Ms+Mp)**2.))*((1.+e)/(1.-e)))
        vsp = -(Mp/Ms)*vpp
        
        '''Rotate Vectors into Viewer frame'''
        rs = vector.Vector(rsp,0.,0.)
        rs.rot_z(omega)
        rs.rot_x(i)
        rp = vector.Vector(rpp,0.,0.)
        rp.rot_z(omega)
        rp.rot_x(i)
        vs = vector.Vector(0.,vsp,0.)
        vs.rot_z(omega)
        vs.rot_x(i)
        vp = vector.Vector(0.,vpp,0.)
        vp.rot_z(omega)
        vp.rot_x(i)
        
        '''Set Up Sim'''
        star = Body.GravBody(Ms,rs,vs)
        planet = Body.GravBody(Mp,rp,vp)
        self.body = [star,planet]
        solver = Solver.RK2(0.01)
        self.physics = Physics.NBody(solver,self.G)
        self.bodies = [cp.deepcopy(self.body)]
        self.t = [0]

    def advance(self,time=None):
        '''Advances Sim to a certain time or for one orbital period
        
        Parameters
        ----------
        time : float
            the target time for the simulation, defaults to one orbital period
        '''
        if time == None:
            time = self.period
        dt = self.physics.solver.stepsize
        time = time - dt
        self.run(self.time_stop(time))
        self.physics.solver.stepsize = time + dt - self.t[-1]
        self.run(self.time_stop(time+dt))
        self.physics.solver.stepsize = dt
                     
    def light_curve(self,time,bodies):
        '''Creates and plots an exoplanet transit light curve for the orbit
        
        Paramters
        ---------
        time : list, float
            a list of the independant variable, time
            
        bodies : list, GravBody
            a list of the Gravbodies at each time in time list
            
        Returns
        -------
        a graph of the light curve
        '''
        r_list = np.array([b[0].position - b[1].position for b in bodies])
        p = np.array([r.cart for r in r_list])
        d = np.sqrt((p[:,0])**2. + (p[:,1])**2.)
        x = (self.Rp**2. - self.Rs**2. + d**2.)/(2.*d)
        h = np.sqrt(self.Rp**2. - x**2.)
        theta = np.arccos(x/self.Rp)
        psi = np.arccos((d-x)/self.Rs)
            
        '''Areas of Arcs and Triangles'''
        a1 = 0.5*x*h
        ap = 0.5*theta*(self.Rp**2.)
        A1 = ap - a1
        a2 = 0.5*(d-x)*h
        As = 0.5*psi*(self.Rs**2.)
        A2 = As -a2
        A = 2*(A1 + A2)
            
        '''Fix Failures'''
        A[d>=(self.Rp+self.Rs)] = 0.
        A[d<=(self.Rs-self.Rp)] = np.pi*(self.Rp**2.)
        A[p[:,2]<=0] = 0
           
        I = ((np.pi*self.Rs**2.) - A)/(np.pi*self.Rs**2.)
        
        plt.figure()
        plt.plot(time,I,'.')
        plt.title('Exo Planet Light Curve')
        plt.xlabel('Time [Years]')
        plt.ylabel('Intensity')
            