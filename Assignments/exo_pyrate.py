# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 19:30:44 2016

@author: jones_000
"""

import Simulation
import matplotlib.pyplot as plt
import math
import numpy as np
import Search

class App(object):
    
    def __init__(self):

        self.time = 4.

    def run(self):
        self.sim_1()
        tlist = np.arange(0,self.max,self.max/100.)
        dlist = [self.error_1(t) for t in tlist]
        plt.figure()
        plt.plot(tlist,dlist,'.')
        plt.title('Error Function')
        plt.xlabel('Time [Years]')
        plt.ylabel('Distance [AU]')
        sim2 = self.sim_2()
        print "Time of min distance is %f"%sim2
                
    def sim_1(self):
        Mp = 1.0
        Ms = 1.*10.**(-6)
        ap = 2.0
        e = 0.5
        As = 1.0
        Ap = 0.25
        omega = 0.
        i = 0.
        sim = Simulation.ExoSim(Mp,Ms,ap,e,As,Ap,omega,i,apnd=True)
        self.max = sim.period
        sim.advance()
        time, bodies = sim.get_results()
        self.plorbits(bodies)
        
    def sim_2(self):
        times = self.start_times()
        print times
        test1 = Search.GoldenSection(self.error_1,times[0],times[1],0.0001)
        result1 = test1.do_it()
        return result1
        
    def start_times(self):
        Mp = 1.0
        Ms = 1.*10.**(-6)
        ap = 2.0
        e = 0.5
        As = 1.0
        Ap = 0.25
        omega = 0.
        i = 0.
        sim = Simulation.ExoSim(Mp,Ms,ap,e,As,Ap,omega,i,apnd=True)
        sim.advance()
        time, bodies = sim.get_results()
        t = np.array(time)
        v = np.array([b[1].velocity.x for b in bodies])
        test = v[1:]*v[:-1]
        vt = v[:-1]
        tt = t[:-1]
        times = tt[test<0]
        if len(times) == 1.:
            times = np.append(times,sim.period/2.+times[0])
        test2 = vt[test<0]
        if test2[0] < 0:
            return times
        elif test2[0] > 0:
            return np.array([times[1],times[0]+sim.period])
        
    def error_1(self,t):
        Mp = 1.0
        Ms = 1.*10.**(-6)
        ap = 2.0
        e = 0.5
        As = 1.0
        Ap = 0.25
        omega = 0.
        i = math.pi/2.
        sim = Simulation.ExoSim(Mp,Ms,ap,e,As,Ap,omega,i,apnd=True)
        sim.advance(t)
        time, bodies = sim.get_results()
        r = bodies[-1][0].position - bodies[-1][1].position
        d = np.sqrt(r.x**2. + r.y**2.)
        return d
        
    def plorbits(self,bodies):
        x0 = [b[0].position.x for b in bodies]
        y0 = [b[0].position.y for b in bodies]
        z0 = [b[0].position.z for b in bodies]
        x1 = [b[1].position.x for b in bodies]
        y1 = [b[1].position.y for b in bodies]
        z1 = [b[1].position.z for b in bodies] 
        plt.figure()
        plt.plot(x0,y0,'.',x1,y1,'.')
        plt.title('Binary Orbits')
        plt.xlabel('X axis [AU]')
        plt.ylabel('Y axis [AU]')
        plt.legend(['Star','Planet'])
#        plt.figure()
#        plt.plot(x0,z0,'.',x1,z1,'.')
#        plt.title('Binary Orbits')
#        plt.xlabel('X axis [AU]')
#        plt.ylabel('Z axis [AU]')
#        plt.legend(['Star','Planet'])
#        plt.figure()
#        plt.plot(y0,z0,'.',y1,z1,'.')
#        plt.title('Binary Orbits')
#        plt.xlabel('Y axis [AU]')
#        plt.ylabel('Z axis [AU]')
#        plt.legend(['Star','Planet'])

if __name__=="__main__":
    app = App()
    app.run()