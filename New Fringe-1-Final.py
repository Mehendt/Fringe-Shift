# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 14:57:29 2022

@author: ad1t1
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

#defining curve fit function
def curve(x,a,b,c,d):
    return a * np.exp(b*x+d) + c

#defining constant variables for wavelength and the difference of refractive indices
wave = 532e-9
ndiff = 0.33

#defining function to plot fringe shift against m, fit the graph with a best fit line, and 
#from that determine and return the film thickness and its uncertainty
def analyse(string, period, distErr, shiftErr, pla, title, col):
    #loading data
    num, fshift = np.loadtxt(string, delimiter = ",", skiprows = 1, unpack = True)
    
    #plotting raw data
    plt.ylabel("Fringe shift F")
    plt.xlabel("Arbitrary integer m")
    sig = np.sqrt((distErr/period)**2 + (shiftErr/fshift)**2) #help defining error bars
    plt.errorbar(num, fshift/period, yerr = (fshift/period)*sig, fmt = "x", capsize = 1.5, color = col[0])
    plt.plot(num, fshift/period, "kx")
    
    #curve fitting
    guess = [-1,-1, max(fshift/period), 0]
    [a,b,c,d], cov = op.curve_fit(curve, num, fshift/period, guess)
    
    #plotting best fit line
    ex = np.arange(0.5,len(fshift)+1,0.01)
    plt.plot(ex, curve(ex,a,b,c,d), label = title, color = col[1])
    
    #finding maximum fringe shift and its error
    errC = np.sqrt(cov[2,2])
    print("Max F is ", c, " +/- ", errC)
    
    #calculating thickness
    thickness = (c * wave) / ndiff #film thickness
    thickerr = (errC * wave) / ndiff #film thickness error
    
    return thickness, thickerr
    
#2d array of colours for formatting purposes
colors = [["#1b5fb3", "#120f7a"], ["#3ca314", "#143806"], ["#96169e", "#38073b"]]

[x1, ux1] = analyse("Bubb1Values.csv", 34,7,10,1, "Bubble 1", colors[1])
[x2, ux2] = analyse("ResB3.csv", 34,8,10,2, "Bubble 2", colors[0])
[x3, ux3] = analyse("Bub4the2the3.csv",36, 6, 10,3, "Bubble 3", colors[2])

plt.legend(loc = "lower right")


plt.savefig("Plot", dpi = 300)
