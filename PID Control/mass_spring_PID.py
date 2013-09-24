#! /usr/bin/env python 

##########################################################################################
# mass_spring_PID.py
#
# Script to analyze PID control for a spring-mass-damper system
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
# 
# Created: 9/17/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# Simple mass-spring system
#                   +---> X
#                   |
#   /|     k     +-----+
#   /|---/\/\/---|     |
#   /|           |  M  +=====> F
#   /|-----]-----|     |
#   /|     c     +-----+


from numpy import *             # Grab all of the NumPy functions
from matplotlib.pyplot import * # Grab MATLAB-like plotting functions
import control                  # import the control system functions

# Uncomment to use LaTeX to process the text in figure
rc('text',usetex=True)

m = 1.;             # kg
k = 2;             # spring constant - N/m
wn = sqrt(k/m)      # Natural Frequency (rad/s)

c = 2.5;             # damping coeff - N/(m/s)
z = c/(2*wn*m)      # damping ratio


# Set up simulation parameters
t = r_[0:5:500j]            # time for simulation, 0-5s with 500 points in-between


#-----  Open-Loop input the step response -----------------------------------------------
#
# Define the open-loop system to use in simulation - in transfer function form here
num = [1]
den = [m,c,k]
sys = control.tf(num,den);

# Let's start it at t=0.5s for clarity in plotting
F = zeros(500)  # Define an array of all zeros
F[25:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)

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

ylim(0,1.25)

plot(T,yout,color='blue',linewidth=2,label='Response')

# uncomment below save the figure as a high-res pdf in the current folder
# savefig('OpenLoop_Step_Resp_Ziegler.svg')

# show the figure
show()



# ----- Try Proportional Control --------------------------------------------------------
kp = 300                  # The proportional gain

# Define the closed-loop transfer function
numP = [kp]
denP = [m,c,(k + kp)]
sysP = control.tf(numP,denP);

# Let's start it at t=0.5s for clarity in plotting
Xd = zeros(500)  # Define an array of all zeros
Xd[50:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)

# run the simulation - utilize the built-in forced_response function
[T_P,yout_P,xout_P] = control.forced_response(sysP,t,Xd)

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

plot(T_P,yout_P,color='blue',linewidth=2,label='Response')

# Uncomment below save the figure as a high-res pdf in the current folder
# savefig('PropControl_Step_Resp_Kp300.pdf')

# show the figure
show()



# ----- Try Proportional-Derivative Control ---------------------------------------------
kp = 300                  # The proportional gain
kd = 10                   # The derivative gain

# Define the closed-loop transfer function
numPD = [kd,kp]
denPD = [m,(c+kd),(k + kp)]
sysPD = control.tf(numPD,denPD);

# Let's start it at t=0.5s for clarity in plotting
Xd = zeros(500)  # Define an array of all zeros
Xd[50:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)

# run the simulation - utilize the built-in forced_response function
[T_PD,yout_PD,xout_PD] = control.forced_response(sysPD,t,Xd)

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

plot(T_PD,yout_PD,color='blue',linewidth=2,label='Response')


# Uncomment below to save the figure as a high-res pdf in the current folder
# savefig('PropDerivControl_Step_Resp.pdf')

# show the figure
# show()

# ----- Try Proportional-Integral-Derivative Control ------------------------------------
kp = 350                    # The proportional gain
kd = 25                     # The derivative gain
ki = 300                    # The integral gain

# Define the closed-loop transfer function
numPID = [kd,kp,ki]
denPID = [m,(c + kd),(k + kp),ki]
sysPID = control.tf(numPID,denPID);

# Let's start it at t=0.5s for clarity in plotting
Xd = zeros(500)  # Define an array of all zeros
Xd[50:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)

# run the simulation - utilize the built-in forced_response function
[T_PID,yout_PID,xout_PID] = control.forced_response(sysPID,t,Xd)

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

plot(T_PID,yout_PID,color='blue',linewidth=2,label='Response')

# Uncomment below to save the figure as a high-res pdf in the current folder
# savefig('PropIntDerivControl_Step_Resp.pdf')

# show the figures
show()