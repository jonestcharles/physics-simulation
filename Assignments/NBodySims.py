# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 16:39:24 2016

@author: jone0208
"""

import Body
import Solver
import Simulation
import Physics
import math
import vector
import matplotlib.pyplot as plt

class App(object):
    
    def __init__(self):
        
        self.solver = Solver.RK4(0.01)
        self.physics = Physics.NBody(self.solver,4*math.pi**2)

    def run(self):
        self.sim_1()
        self.sim_2()
        self.sim_3()

    def sim_1(self):
        r1 = vector.Vector(1.,0,0)
        v1 = vector.Vector(0,math.pi,0)
        r2 = vector.Vector(-1.,0,0)
        v2 = vector.Vector(0,-math.pi,0)
        One = Body.GravBody(1.,r1,v1)
        Two = Body.GravBody(1.,r2,v2)
        Objects = [One,Two]
        sim = Simulation.OrbitSim(physics=self.physics,body=Objects)
        sim.advance(time=10.)
        time, bodies = sim.get_results()
        self.plorbits(bodies)
        
    def sim_2(self):
        r1 = vector.Vector(1.,0,0)
        v1 = vector.Vector(0,1.1*math.pi,0)
        r2 = vector.Vector(-1.,0,0)
        v2 = vector.Vector(0,-math.pi,0)
        One = Body.GravBody(1.,r1,v1)
        Two = Body.GravBody(1.,r2,v2)
        Objects = [One,Two]
        sim = Simulation.OrbitSim(physics=self.physics,body=Objects)
        sim.advance(time=10.)
        time, bodies = sim.get_results()
        self.plorbits(bodies)
        
    def sim_3(self):
        r1 = vector.Vector(1.,0,0)
        v1 = vector.Vector(0,1.1*math.pi,0)
        r2 = vector.Vector(-1.,0,0)
        v2 = vector.Vector(0,-1.1*math.pi,0)
        One = Body.GravBody(1.,r1,v1)
        Two = Body.GravBody(1.,r2,v2)
        Objects = [One,Two]
        sim = Simulation.OrbitSim(physics=self.physics,body=Objects)
        sim.advance(time=10.)
        time, bodies = sim.get_results()
        self.plorbits(bodies)
        
    def plorbits(self,bodies):
        x0= [b[0].position.x for b in bodies]
        y0= [b[0].position.y for b in bodies]
        x1= [b[1].position.x for b in bodies]
        y1= [b[1].position.y for b in bodies]
        plt.figure()
        plt.plot(x0,y0,'.',x1,y1,'.')
        plt.title('Binary Orbits')
        plt.xlabel('X axis [AU]')
        plt.ylabel('Y axis [AU]')
        plt.legend(['One','Two'])

if __name__=="__main__":
    app = App()
    app.run()