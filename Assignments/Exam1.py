# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 15:07:39 2016

@author: jone0208
"""

import Body
import Simulation
import Solver
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    skull = Body.GravBody(5,6.371*10**6,8000.)
    solver = Solver.RK2(0.001)
    def stop_condition(skull):
        return skull.velocity > 0
    sim1 = Simulation.TrajectorySim(stop_condition,solver,skull)
    x,y = sim1.get_results()
    skull2 = Body.GravBody(5,6.371*10**6,8000.)
    sim2 = Simulation.InverseTrajectorySim(stop_condition,solver,skull2)
    a,b = sim2.get_results()
   
    plt.plot(x,y)
    plt.plot(a,b)
    plt.title("Skull Tosses")
    plt.xlabel("Time [s]")
    plt.ylabel("Height [m]")
    plt.legend(["Uniform Gravity","Inverse Square Gravity"])
    
    plt.figure()
    varray = np.arange(0,100,0.5)
    harray = []
    for v in varray:
        skull3 = Body.GravBody(5,6.371*10**6,v)
        sim3 = Simulation.InverseTrajectorySim(stop_condition,solver,skull3)
        result = sim3.get_results()
        harray.append(skull3.position)

    plt.plot(varray,harray)        
    plt.title("Maximum Height vs. Initial Velocity")
    plt.xlabel("Initial Velocity [m/s]")
    plt.ylabel("Maximum Height [m]")
    
if __name__ == "__main__": main()