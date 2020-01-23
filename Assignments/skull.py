# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 15:57:53 2016

@author: jone0208
"""

import Body
import matplotlib.pyplot as plt
import Solver
import Simulation

def main():
    skull = Body.GravBody(5,5,5)
    solver = Solver.RK2(0.001)
    def stop_condition(skull):
        return skull.velocity > 0
    sim = Simulation.TrajectorySim(stop_condition,solver,skull)
    t, h = sim.get_results()
    plt.plot(t,h)
    plt.title("OOP Skull Toss")
    plt.xlabel("Time [s]")
    plt.ylabel("Height [m]")
    
    
if __name__ == "__main__": main()