#! /usr/bin/env python 

##########################################################################################
# bangbang_mass.py
#
# Script to analyze bang-bang inputs to a simple mass system
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 9/23/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# Simple mass system
#
#             +---> X
#             |
#          +-----+
#          |     |
#  F=====> |  M  |
#          |     |
#          +-----+


from numpy import *                 # Grab all of the NumPy functions
from matplotlib.pyplot import *     # Grab MATLAB-like plotting functions
import control                      # import the control system functions

# Uncomment to use LaTeX to process the text in figure
rc('text',usetex=True)

m = 1.;             # kg

# Define the system
num = 1.
den = [m,0,0]
sys = control.tf(num,den)


# Set up simulation parameters
t = r_[0:5:0.001]            # time for simulation, 0-5s with 500 points in-between

# Let's start it at t=0.5s for clarity in plotting
F = zeros(5000)  # Define an array of all zeros
F[500:1499] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)
F[1500:2499] = -1

# Plot the command
# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
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

xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Force (N)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

xlim(0,4)
ylim(-1.25,1.25)

plot(t,F,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
savefig('BangBang_Force.svg')

#show the figure
#show()


# run the simulation - utilize the built-in forced_response function
[T,yout,xout] = control.forced_response(sys,t,F)

# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
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

xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Position (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

xlim(0,4)
ylim(0,1.25)

plot(T,yout,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
savefig('BangBang_Mass.png')

# show the figure
show()


#----- Look at the velocity
sys_vel = control.tf(num,[m,0])

# run the simulation - utilize the built-in forced_response function
[T,yout,xout] = control.forced_response(sys_vel,t,F)

# Make the figure pretty, then plot the results
#   "pretty" parameters selected based on pdf output, not screen output
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

xlabel('Time (s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)
ylabel('Velocity (m/s)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

xlim(0,4)
ylim(0,1.25)

plot(T,yout,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
savefig('BangBang_MassVel.png')

# show the figure
show()

