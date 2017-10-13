#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 10:55:21 2017

@author: yyuan
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import sys
import time

def energycal_fast(x):
    return 0.25 * x**4 + 0.5 * x**2
def energycal_slow(x):
    return np.sin(0.5 * x)

def forcecal_fast(x):
    ffast = -x**3-x
    return ffast

def forcecal_slow(x):
    fslow = -0.5*np.cos(0.5*x)
    return fslow


def OBABO(x,p,N,dt,M,seed,gamma):
    data = []
    c1 = np.exp(-gamma*dt/2)
    c2 = np.sqrt((1-c1**2)*m/beta)
    ddt = dt/M
    ffast = forcecal_fast(x)
    fslow = forcecal_slow(x)
    np.random.seed(seed)
    for i in range(1, 1+N):
        R = np.random.normal(0,1)
        p = c1*p + c2*R
        p = p + dt*fslow/2
        for j in range(M):
            p = p + ddt*ffast/2
            x = x + ddt*p/m
            ffast = forcecal_fast(x)
            p = p + ddt*ffast/2
        fslow = forcecal_slow(x)
        p = p + dt*fslow/2
        R = np.random.normal(0,1)
        p = c1*p + c2*R
        data.append([i,x,p,energycal_fast(x),energycal_slow(x)])
    return data

def BAOAB(x,p,N,dt,M,seed,gamma):
    data = []
    c1 = np.exp(-gamma*dt)
    c2 = np.sqrt((1-c1**2)*m/beta)
    ddt = dt/M
    ffast = forcecal_fast(x)
    fslow = forcecal_slow(x)
    np.random.seed(seed)
    if M == 1:
        for i in range(1, 1 + N):
            p = p + dt * (fslow + ffast) / 2
            x = x + dt * p / m / 2
            R = np.random.normal(0, 1)
            p = c1 * p + c2 * R
            x = x + dt * p / m / 2
            ffast = forcecal_fast(x)
            fslow = forcecal_slow(x)
            p = p + dt * (fslow + ffast) / 2
            data.append([i, x, p, energycal_fast(x), energycal_slow(x)])
        return data
    else:
        for i in range(1, 1 + N):
            p = p + dt * fslow / 4
            for j in range(M / 2):
                p = p + ddt * ffast / 2
                x = x + ddt * p / m
                ffast = forcecal_fast(x)
                p = p + ddt * ffast / 2
            fslow = forcecal_slow(x)
            p = p + dt * fslow / 4

            R = np.random.normal(0, 1)
            p = c1 * p + c2 * R

            p = p + dt * fslow / 4
            for k in range(M / 2):
                p = p + ddt * ffast / 2
                x = x + ddt * p / m
                ffast = forcecal_fast(x)
                p = p + ddt * ffast / 2
            fslow = forcecal_slow(x)
            p = p + dt * fslow / 4
            data.append([i, x, p, energycal_fast(x), energycal_slow(x)])
    return data



'oscillator parameters'
k = 1
m = 1
'system parameter'
beta = 1

def main(N, dt, M, seed, gamma, type_int="BAOAB", savepath='.'):

    print "#  TOYCODE 3.0"
    N = int(N)
    dt = float(dt)
    M = int(M)
    seed = int(seed)
    gamma = float(gamma)

    timenow = time.time()
    print ""
    print "#  Total steps       : ", N
    print "#  Outer time step   : ", dt
    print "#  Inner time step   : ", dt / M
    print "#  Random seed       : ", seed
    print "#  gamma             : ", gamma
    print "#  Integrator        : ", type_int
    print "# Sim starts at ", timenow
    p0 = 1
    x0 = 0 
    if type_int == 'BAOAB':
        delta_time = time.time()
        data = BAOAB(x0,p0,N,dt,M,seed,gamma)
        delta_time = time.time() - delta_time
    elif type_int == 'OBABO':
        delta_time = time.time()
        data = OBABO(x0,p0,N,dt,M,seed,gamma)
        delta_time = time.time() - delta_time
    else:
        raise ValueError('# ERROR: Unknown integrator')

    prefix = 'sim'
    filename = prefix+ "_" + type_int + '_' + str(dt) + "_" + "M" + str(M) + "_" + "gamma" + str(gamma) + ".data"
    print "# Takes ", delta_time ," s."
    print "# Dumping output [step, position, momentum, energy_fast, energy_slow] in ", savepath + '/' + filename
    np.savetxt(savepath + '/' + filename, data)
    
    
if __name__ == '__main__':
    try:
      main(*sys.argv[1:])
    except:
      print "USAGE: MTS3.0.py N dt M seed gamma type_int savepath"
