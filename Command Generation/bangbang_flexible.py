#! /usr/bin/env python 

##########################################################################################
# bangbang_flexible.py
#
# Script to analyze bang-bang commands for flexible systems
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 9/24/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# Simple two-mass system
#
#             +---> X1        +---> X2
#             |               |      
#          +-----+         +-----+   
#          |     |         |     |   
#  F=====> |  M1 +--/\/\/--+  M2 |
#          |     |         |     |   
#          +-----+         +-----+   


from numpy import *                 # Grab all of the NumPy functions
from matplotlib.pyplot import *     # Grab MATLAB-like plotting functions
import control                      # import the control system functions

# Uncomment to use LaTeX to process the text in figure
rc('text',usetex=True)

k = 10       # spring constant (N/m)
m1 = 1             # first mass (kg)
m2 = 1             # second mass (kg)

# Define the system
A = [[0,1,0,0],
    [-k/m1,0,k/m1,0],
    [0,0,0,1],
    [k/m2,0,-k/m2,0]]

B = [[0],[1/m1],[0],[0]]

C = [[1,0,0,0],[0,0,1,0]]

D = [[0], [0]]

sys = control.ss(A,B,C,D)


# Set up simulation parameters
t = r_[0:5:0.001]            # time for simulation, 0-5s with 500 points in-between

# Let's start it at t=0.5s for clarity in plotting
fmax = 2.                   # Define the maximum actuator force (assumed symmetric)
F = zeros(5000)             # Define an array of all zeros
F[500:1499] = fmax
F[1500:2499] = -fmax

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
ylim(-1.25*fmax,1.25*fmax)

plot(t,F,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
savefig('BangBang_Force_Flexible.png')

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
ylim(0,2)

plot(T,yout[0,:],color='blue',linewidth=2,label=r'$m_1$ Response')
plot(T,yout[1,:]+0.25,color='red',linestyle='--',linewidth=2,label=r'$m_2$ Response')

leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# uncomment below save the figure as a high-res pdf in the current folder
# savefig('BangBang_Mass_Flexible.pdf')

# show the figure
# show()

# ----- Double the command duration -----
# Set up simulation parameters
t = r_[0:10:0.001]            # time for simulation, 0-10s

# Let's start it at t=0.5s for clarity in plotting
fmax = 1.                   # Define the maximum actuator force (assumed symmetric)
F = zeros(10000)             # Define an array of all zeros
F[500:1914] = fmax
F[1915:3329] = -fmax

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

xlim(0,8)
ylim(-1.25*fmax,1.25*fmax)

plot(t,F,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
# savefig('BangBang_Force_Flexible.pdf')

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

xlim(0,8)
ylim(0,2)

plot(T,yout[0,:],color='blue',linewidth=2,label=r'$m_1$ Response')
plot(T,yout[1,:]+0.25,color='red',linestyle='--',linewidth=2,label=r'$m_2$ Response')

leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# uncomment below save the figure as a high-res pdf in the current folder
# savefig('BangBang_Mass_FlexibleDurationIncrease.pdf')

# show the figure
show()