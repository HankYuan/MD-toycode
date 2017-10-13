
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import math
import re
import sys

'means of every data file generator'
def main(loadpath='raw/', savepath='.'):
    with open('log.txt') as f:
        for line in f:
            if (line[0] == '#') & (line.find('gamma') <> -1):
                start = line.find('gamma') + 7
                gammastr = line[start:-1]
                gammalist = gammastr.split(' ')
                gammalist = [str(float(gamma)) for gamma in gammalist]
                break
    prefix = 'sim_BAOAB_0.1_M1_gamma'
    qmeanlist = []
    emeanlist = []

    for gamma in gammalist:
        filename = prefix + gamma + '.data'
        data = np.loadtxt(loadpath + filename)
        qmean = np.mean(data[:,1])
        emean = np.mean(data[:,3] + data[:,4])

        qsigma = np.std(data[:,1])
        esigma = np.std(data[:,3] + data[:,4])

        qmeanlist.append((float(gamma), qmean, qsigma))
        emeanlist.append((float(gamma), emean, esigma))


    # print (qmeanlist,emeanlist)
    np.savetxt(savepath + '/qmean.data', qmeanlist)
    np.savetxt(savepath + '/emean.data', emeanlist)

if __name__ == '__main__':
    try:
        main(*sys.argv[1:])
    except:
        print 'USAGE: Mean_Generator.py [data_folder] [savepath]'
