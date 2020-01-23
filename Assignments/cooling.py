# -*- coding: utf-8 -*-
"""
Created on Tue Feb 09 12:12:57 2016

@author: jone0208
"""
import matplotlib.pyplot as plt
import Body
import Solver
import Simulation

def main():
    coffee = Body.ThermalBody(500)
    solver = Solver.Euler(0.5)
    def stop_condition(coffee):
        return coffee.temperature > sim.Ta*1.1
    sim = Simulation.CoolingSim(stop_condition,solver,293,0.05,coffee)
    t,T = sim.get_results()
    plt.plot(t,T)
    
    coffee = Body.ThermalBody(500)
    solver = Solver.RK2(0.5)
    def stop_condition(coffee):
        return coffee.temperature > sim.Ta*1.1
    sim = Simulation.CoolingSim(stop_condition,solver,293,0.05,coffee)
    t,T = sim.get_results()
    plt.plot(t,T)
    
    plt.title("OOP Cooling Curves")
    plt.xlabel("Time [s]")
    plt.ylabel("Temperature[K]")
    plt.legend(["Euler Curve","RK2 Cooling Curve"])
        

if __name__ == "__main__": main()