# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:17:30 2016

@author: jone0208
"""

import Simulation
import matplotlib.pyplot as plt

class App(object):
    
    def __init__(self):

        self.time = 4.

    def run(self):
        self.sim_1()
        
    def sim_1(self):
        sim = Simulation.BinarySim(1.,4.,2.,0.5)
        sim.advance(self.time)
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