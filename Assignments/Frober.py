# -*- coding: utf-8 -*-
"""
Created on Tue Mar 08 15:45:52 2016

@author: jone0208
"""
import Body
import Solver
import Simulation
import Search
import Physics
import math
import vector

def main():
    def error(theta):
        htarg = 0
        r =  vector.Vector(0,0,0)
        v = vector.Vector(r=100,theta=theta,phi=(math.pi/2))
        particle = Body.GravBody(5,r,v)
        solver =Solver.RK4(0.1)
        physics = Physics.UniformGravity(solver,c=0.1)
        sim = Simulation.TrajectorySim(stop_maker(htarg),physics,particle)
        a,b = sim.get_results()
        y = [p.position.y for p in b]
        E = particle.position.x - max(y)
        return E
    test = Search.NewtonMethod(error,(math.pi/4),0.0001,0.1)
    result =  test.do_it()
    print result
       
def stop_maker(htarg):
    def s(particle):
        return particle.position.y > htarg or particle.velocity.y > 0
    return s
    
if __name__=="__main__": main()