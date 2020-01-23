# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 16:47:27 2016

@author: jone0208
"""

import Body
import Solver
import Simulation
import Physics
import math
import vector
import matplotlib.pyplot as plt
import numpy as np

class App(object):
    
    def __init__(self):
        
        self.max_steps = 10000 #mx number fo steps to run to failure
        self.AU = 1 #one AU, radius from Earth to Sun
        self.v0_list = [2*math.pi,2*0.8*math.pi] #velocity in Au/orbit
        self.dt_list = [0.003,0.002,0.001]

    def run(self):
        '''Orbits'''
        for v0 in self.v0_list:
            for dt in self.dt_list:
                r = vector.Vector(self.AU,0,0) #starting position in AU
                v = vector.Vector(0,v0,0) 
                earth = Body.GravBody(1,r,v)
                solver = Solver.RK4(dt)
                physics = Physics.CentralGravity(solver,G=4*math.pi**2,M=1) # M is 1 solar mass
                sim = Simulation.OrbitSim(self.stop,physics,earth)
                time, bodies = sim.get_results()
               
                y = [b[0].position.y for b in bodies]
                x = [b[0].position.x for b in bodies]
                energy = physics.energy(bodies)
                errors = self.error(energy)
                
                if v0 == math.pi*2:
                    plt.figure(1)
                    plt.plot(x,y,'.')
                    plt.title("Circular Orbits of Earth Around Sun")
                    plt.ylabel("Position in y [AU]")
                    plt.xlabel("Position in x [AU]")
                    plt.legend(["dt=0.003","dt=0.002","dt=0.001"])
                    
                    plt.figure(2)
                    plt.plot(time,errors)
                    plt.title("Error in Energy vs Time")
                    plt.ylabel("Percent Error")
                    plt.xlabel("Time [Years]")
                    plt.legend(["dt=0.003","dt=0.002","dt=0.001"])
                    
                else:
                    plt.figure(3)
                    plt.plot(x,y,'.')
                    plt.title("Elliptical Orbits of Earth Around Sun")
                    plt.ylabel("Position in y [AU]")
                    plt.xlabel("Position in x [AU]")
                    plt.legend(["dt=0.003","dt=0.002","dt=0.001"])

                    plt.figure(4)
                    plt.plot(time,errors)
                    plt.title("Error in Energy vs Time")
                    plt.ylabel("Percent Error")
                    plt.xlabel("Time [Years]")
                    plt.legend(["dt=0.003","dt=0.002","dt=0.001"])
                   
        """Kepler"""
        r_list = [0.9,1,1.1]
        v_list = [2*math.pi,2*0.9*math.pi,2*1.1*math.pi]
        for r in r_list:
            for v in v_list:
                r0 = vector.Vector(r,0,0)
                v0 = vector.Vector(0,v,0)
                earth = Body.GravBody(1,r0,v0)
                solver = Solver.RK4(0.001)
                physics = Physics.CentralGravity(solver,G=4*math.pi**2,M=1) # M is 1 solar mass
                sim = Simulation.OrbitSim(self.stop,physics,earth)
                time, bodies = sim.get_results()
                a = sim.semimajor_axis()
                p = sim.period()
                plt.figure(5)
                plt.plot(a,p,'.')
        plt.figure(5)
        a = np.arange(0,2,0.001)
        p = a**(3./2.)
        plt.plot(a,p)
        plt.title("Semi Major Axis vs Period")
        plt.ylabel("Orbital Period [Years]")
        plt.xlabel("Semi Major Axis [AU]")
                    
    def error(self,energy):
        errors = []
        for e in energy:
            error = (e-energy[0]/energy[0])*100
            errors.append(error)
        return errors
        
    def stop(self,bodies):
        if len(bodies) == self.max_steps:
            print "Orbit Failed to complete after %f steps"%self.max_steps
            return False
        elif len(bodies) < 2:
            return True
        else:
            L = bodies[0][0].position - bodies[-1][0].position
            F = bodies[0][0].position - bodies[1][0].position
            if L.r < F.r:
                return False
        return True
       
if __name__=="__main__":
    app = App()
    app.run()