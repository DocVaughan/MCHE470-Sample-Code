#! /usr/bin/env python 

from numpy import *    
import scipy
from matplotlib.pyplot import * # Grab MATLAB plotting functions
from scipy.integrate import odeint


def accel_input(Amax,Vmax,Distance,StartTime,CurrTime,Shaper):
# Original MATLAB/Octave premable
###########################################################################
# function [accel] = accel_input(Amax,Vmax,Distance,CurrTime,Shaper)
#
# Function returns acceleration at a given timestep based on user input
#
# Amax = maximum accel, assumed to besymmetric +/-
# Vmax = maximum velocity, assumed to be symmetric in +/-
# Distance = desired travel distance 
# StartTime = Time command should begin
# CurrTime = current time 
# Shaper = array of the form [Ti Ai] - matches output format of shaper functions
#           in toolbox
#          * If no Shaper input is given, then unshaped in run
#          * If Shaper is empty, then unshaped is run
#
#
# Assumptions:
#   * +/- maximums are of same amplitude
#   * command will begin at StartTime (default = 0)
#   * rest-to-rest bang-coast-bang move (before shaping)
#
# Created: 9/23/11 - Joshua Vaughan - vaughanje@gatech.edu
#
# Modified: 
#   10/11/11
#       * Added hard-coded shaping option - JEV (vaughanje@gatech.edu)
#       * embedded into shaped_jumping.m for use there
#
###########################################################################
#
# Converted to Python on 3/3/13 by Joshua Vaughan (joshua.vaughan@louisiana.edu)

    # These are the times for a bang-coast-bang input 
    t1 = StartTime
    t2 = (Vmax/Amax) + t1
    t3 = (Distance/Vmax) + t1
    t4 = (t2 + t3)-t1
    end_time = t4

    if len(Shaper) == 0:
    # if nargin == 5 || not Shaper:
        # If no shaper is input, create an unshaped command
        if t3 <= t2: # command should be bang-bang, not bang-coast-bang
            t2 = sqrt(Distance/Amax)+t1
            t3 = 2*sqrt(Distance/Amax)+t1
            end_time = t3
        
            accel = Amax*(CurrTime > t1) - 2*Amax*(CurrTime > t2) + Amax*(CurrTime > t3)
    
        else: # command is bang-coast-bang
            accel = Amax*(CurrTime > t1) - Amax*(CurrTime > t2) - Amax*(CurrTime > t3) + Amax*(CurrTime > t4)


    else: # create a shaped command
        ts = zeros((9,1))
        A = zeros((9,1))
        #   Parse Shaper parameters
        for ii in range(len(Shaper)):
            ts[ii] = Shaper[ii,0]  # Shaper impulse times
            A[ii] = Shaper[ii,1]  # Shaper impulse amplitudes
#       print A
#       print ts

        #     if len(Shaper) > 9:
        #         error('Error: As of 10/11/11, accel_input.m only works for shapers of less than 9 impulses.')

        # Hard-coded for now
        # TODO: be smarter about constructing the total input - JEV - 10/11/11
        accel = (A[0]*(Amax*(CurrTime > (t1+ts[0])) - Amax*(CurrTime > (t2+ts[0])) - Amax*(CurrTime > (t3+ts[0])) + Amax*(CurrTime > (t4+ts[0])))
        +   A[1]*(Amax*(CurrTime > (t1+ts[1])) - Amax*(CurrTime > (t2+ts[1])) - Amax*(CurrTime > (t3+ts[1])) + Amax*(CurrTime > (t4+ts[1])))
        +   A[2]*(Amax*(CurrTime > (t1+ts[2])) - Amax*(CurrTime > (t2+ts[2])) - Amax*(CurrTime > (t3+ts[2])) + Amax*(CurrTime > (t4+ts[2])))
        +   A[3]*(Amax*(CurrTime > (t1+ts[3])) - Amax*(CurrTime > (t2+ts[3])) - Amax*(CurrTime > (t3+ts[3])) + Amax*(CurrTime > (t4+ts[3])))
        +   A[4]*(Amax*(CurrTime > (t1+ts[4])) - Amax*(CurrTime > (t2+ts[4])) - Amax*(CurrTime > (t3+ts[4])) + Amax*(CurrTime > (t4+ts[4])))
        +   A[5]*(Amax*(CurrTime > (t1+ts[5])) - Amax*(CurrTime > (t2+ts[5])) - Amax*(CurrTime > (t3+ts[5])) + Amax*(CurrTime > (t4+ts[5])))
        +   A[6]*(Amax*(CurrTime > (t1+ts[6])) - Amax*(CurrTime > (t2+ts[6])) - Amax*(CurrTime > (t3+ts[6])) + Amax*(CurrTime > (t4+ts[6])))
        +   A[7]*(Amax*(CurrTime > (t1+ts[7])) - Amax*(CurrTime > (t2+ts[7])) - Amax*(CurrTime > (t3+ts[7])) + Amax*(CurrTime > (t4+ts[7])))
        +   A[8]*(Amax*(CurrTime > (t1+ts[8])) - Amax*(CurrTime > (t2+ts[8])) - Amax*(CurrTime > (t3+ts[8])) + Amax*(CurrTime > (t4+ts[8]))))

    return accel

def vectorfield(w, t, p):
    """
    Defines the differential equations for the coupled spring-mass system.

    Arguments:
        w :  vector of the state variables:
                  w = [x1,y1,x2,y2]
        t :  time
        p :  vector of the parameters:
                  p = [m1,m2,k1,k2,L1,L2,b1,b2]
    """
    x1, y1, x2, y2 = w
    m1, m2, k, Amax, Vmax, StartTime, Distance, Shaper = p

    # Create f = (x1',y1',x2',y2'):
    f = [y1,
         (k * (x2 - x1) + accel_input(Amax,Vmax,Distance,StartTime,t,Shaper)) / m1,
         y2,
         (-k * (x2 - x1)) / m2]
    return f


#
# two_springs_solver.py
#
"""Use ODEINT to solve the differential equations defined by the vector field
in two_springs.py.
"""

# Parameter values
# Masses:
m1 = 1.0
m2 = 1.0
# Spring constants
k = 10.0

# Initial conditions
# x1 and x2 are the initial displacements; y1 and y2 are the initial velocities
x1 = 0.0
y1 = 0.0
x2 = 0.0
y2 = 0.0

# ODE solver parameters
abserr = 1.0e-8
relerr = 1.0e-6
stoptime = 10.0
numpoints = 250

# Set input paramters
A_max = 1       # 1 N peak force on data sheet
V_max = 1       # 1 m/s
Start = 0.50    # start input at 0.5s

# ODE solver parameters
abserr = 1.0e-9
relerr = 1.0e-9
max_step = 0.005
stoptime = 5.0
numpoints = 5000

Shaper = []


# Create the time samples for the output of the ODE solver.
# I use a large number of points, only because I want to make
# a plot of the solution that looks nice.
# t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]
t = r_[0:10:0.01]

# Create range of "command spacings":
max_dist = 5.
num_samples = 1000
Dist = r_[1:max_dist:(max_dist/num_samples)]



vib_amp = zeros(len(Dist))

count = 0
for ii in range(len(Dist)):

    # Pack up the parameters and initial conditions:
    p = [m1, m2, k, A_max, V_max, Start, Dist[ii], Shaper]
    w0 = [x1, y1, x2, y2]

    # Call the ODE solver.
    wsol = odeint(vectorfield, w0, t, args=(p,),
                  atol=abserr, rtol=relerr)
                  
    #----- Test closed form solution for bang-bang input
    t1 = Start
    t2 = (V_max/A_max) + t1
    t3 = (Dist[ii]/V_max) + t1
    t4 = (t2 + t3)-t1
    end_time = t4

    if t3 < t2: # command should be bang-bang, not bang-coast-bang
        t2 = sqrt(Dist/A_max)+t1
        t3 = 2*sqrt(Dist/A_max)+t1
        end_time = t3
    
    end_sample = end_time*1/0.01
              
    vib_amp[ii] = max(wsol[end_sample:-1,2])-min(wsol[end_sample:-1,2])

# 
#     #  Plot the response#   Many of these setting could also be made default by the .matplotlibrc file
#     fig = figure(figsize=(6,4))
#     ax = gca()
#     subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
#     setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
#     setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)
#     ax.spines['right'].set_color('none')
#     ax.spines['top'].set_color('none')
#     ax.xaxis.set_ticks_position('bottom')
#     ax.yaxis.set_ticks_position('left')
#     ax.grid(True,linestyle=':',color='0.75')
#     ax.set_axisbelow(True)
# 
#     xlabel(r'Time (s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
#     ylabel(r'Position (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=8)
# 
# 
#     plot(t,wsol[:,0],linewidth=2,label=r'$x_1$')
#     plot(t,wsol[:,2],linewidth=2,label=r'$x_2$')
# 
#     leg = legend(loc='upper right', fancybox=True)
#     ltext  = leg.get_texts() 
#     setp(ltext,family='CMU Serif',fontsize=16)
#     
#     print end_time
#         ## save the figure as a high-res pdf in the current folder
#     #savefig('MCHE485_Two_mass_spring.pdf',dpi=600)
# 
#     show()

#  Plot the response
#   Many of these setting could also be made default by the .matplotlibrc file
fig = figure(figsize=(6,4))
ax = gca()
subplots_adjust(bottom=0.17,left=0.17,top=0.96,right=0.96)
setp(ax.get_ymajorticklabels(),family='CMU Serif',fontsize=18)
setp(ax.get_xmajorticklabels(),family='CMU Serif',fontsize=18)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.grid(True,linestyle=':',color='0.75')
ax.set_axisbelow(True)

xlabel(r'Move Distance (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel(r'Vibration Amplitude (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=8)


plot(Dist,vib_amp,linewidth=2,label=r'$x_1$')
# plot(t,wsol[:,2],linewidth=2,label=r'$x_2$')
# 
# leg = legend(loc='upper right', fancybox=True)
# ltext  = leg.get_texts() 
# setp(ltext,family='CMU Serif',fontsize=16)

## save the figure as a high-res pdf in the current folder
savefig('Vib_vs_MoveDistance.png')

show()
