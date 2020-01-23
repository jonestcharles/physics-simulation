# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 13:04:53 2016

@author: jone0208
"""

import Body
import Solver
import Simulation
import Physics
import math
import vector
import Search
import matplotlib.pyplot as plt

class App(object):
    
    def __init__(self):
        
        
        self.rEarth = vector.Vector(1,0,0)
        self.vEarth = vector.Vector(0,2*math.pi,0)
        self.rMars = vector.Vector(1.5,0,0)
        self.vMars = vector.Vector(0,2*math.pi/math.sqrt(1.5),0)
        self.max_steps = 10000
        self. solver = Solver.RK4(0.01)
        self.physics = Physics.CentralGravity(self.solver,G=4*math.pi**2,M=1)
        
    def run(self):
        sim1 = self.sim_1()
        print sim1
        sim2 = self.sim_2()
        print sim2
        sim3 = self.sim_3()
        print sim3
        
    def sim_1(self):    
        Earth = Body.GravBody(1,self.rEarth,self.vEarth)
        Mars = Body.GravBody(1,self.rMars,self.vMars)
        Planets = [Earth,Mars]
        sim = Simulation.OrbitSim(self.stop_1,self.physics,Planets)
        sim.advance()
        time, bodies = sim.get_results()
        return bodies[-1][1].position.theta
        
    def sim_2(self):
        test = Search.NewtonMethod(self.error_2,1.1*2*math.pi,0.01,0.01)
        result = test.do_it()
        self.vL = result
        return result
        
    def sim_3(self):
        test = Search.NewtonMethod(self.error_3,1.9,0.01,0.01) 
        result = test.do_it()
        return result
        
    def stop_1(self,time,bodies):
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

    def error_2(self,v0):
        vShip = vector.Vector(0,v0,0)
        rShip = vector.Vector(1,0,0)
        Ship = Body.GravBody(1,rShip,vShip)
        sim = Simulation.OrbitSim(self.stop_1,self.physics,Ship)
        sim.advance()
        time, Ships = sim.get_results()
        r = [[s.position.r for s in ship] for ship in Ships]
        max_r = max(r)
        error = max_r[0] - 1.5 #since r becomes another stupid list of lists
        return error
        
    def error_3(self,launch_time):
        vShip = vector.Vector(0,2*math.pi,0)
        rShip = vector.Vector(1,0,0)
        Ship = Body.GravBody(1,rShip,vShip)
        rMars = vector.Vector(1.5,0,0)
        vMars = vector.Vector(0,2*math.pi/math.sqrt(1.5),0)
        Mars = Body.GravBody(1,rMars,vMars)
        Objects = [Ship,Mars]
        sim = Simulation.OrbitSim(physics=self.physics,body=Objects)
        sim.advance(time=launch_time)
        sim.body[0].velocity.r = self.vL
        p = ((2.5/2.)**(3./2.))/2.
        sim.advance(time=p+launch_time)
        t2list,blist = sim.get_results()
        sep = sim.body[1].position - sim.body[0].position
        error = sep.r
        if error <= 0.01:
            self.plorbits(blist)
        return error
        
    def plorbits(self,bodies):
        x0= [b[0].position.x for b in bodies]
        y0= [b[0].position.y for b in bodies]
        x1= [b[1].position.x for b in bodies]
        y1= [b[1].position.y for b in bodies]
        plt.figure()
        plt.plot(x0,y0,x1,y1)
        plt.title('Mission to Mars')
        plt.xlabel('X axis [AU]')
        plt.ylabel('Y axis [AU]')
        plt.legend(['Ship','Mars'])
        
        
        
if __name__=="__main__":
    app = App()
    app.run()