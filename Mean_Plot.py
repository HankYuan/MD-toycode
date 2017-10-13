#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 14:49:40 2017

@author: yyuan
"""

import numpy as np
import matplotlib.pyplot as plt

qmean = np.loadtxt('qmean.data')
emean = np.loadtxt('emean.data')

q_expected = -0.220223
e_expected = 0.2938

with open('log.txt') as f:
    for line in f:
        if (line[0] == '#') & (line.find('steps') <> -1):
            start = line.find('steps') + 7
            steps_N = line[start:-1]
            steps_N = int(steps_N)
            break
'standard errors'
q_se = [sigma / np.sqrt(steps_N) for sigma in qmean[:,2]]
e_se = [sigma / np.sqrt(steps_N) for sigma in emean[:,2]]

'position mean plot'
plt.errorbar(qmean[:,0], qmean[:,1], yerr=q_se, label='position', marker='s')
horizontal = [q_expected for x in range(qmean[:,0].size)]
plt.plot(qmean[:,0], horizontal, label='expected position')
plt.xscale('log')
plt.xlabel('gamma')
plt.ylabel('position')
plt.legend()
plt.show()

'energy mean plot'
plt.errorbar(emean[:,0], emean[:,1], yerr=e_se, label='energy',marker='o')
horizontal = [e_expected for x in range(qmean[:,0].size)]
plt.plot(qmean[:,0], horizontal, label='expected energy')
plt.xscale('log')
plt.xlabel('gamma')
plt.ylabel('energy')
plt.legend()
plt.show()

'Relative error calculate'
qerr = [abs(q / q_expected - 1)*100 for q in qmean[:,1]]
eerr = [abs(e / e_expected - 1)*100 for e in emean[:,1]]

'position error plot'
plt1 = plt.plot(qmean[:,0], qerr, label='q', marker='s')
plt.xscale('log')
plt.xlabel('gamma')
plt.ylabel('%err in position')
plt.legend()
plt.show()
'energy error plot'
plt1 = plt.plot(emean[:,0], eerr, label='e', marker='o')
plt.xscale('log')
plt.xlabel('gamma')
plt.ylabel('%err in energy')
plt.legend()
plt.show()


