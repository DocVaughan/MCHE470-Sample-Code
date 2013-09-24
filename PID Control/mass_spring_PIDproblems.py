#! /usr/bin/env python 

##########################################################################################
# mass_spring_PIDproblems.py
#
# Script to analyze PID control "problems" for a spring-mass-damper system
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

# Simple mass-spring system
#                   +---> X
#                   |
#   /|     k     +-----+
#   /|---/\/\/---|     |
#   /|           |  M  +=====> F
#   /|-----]-----|     |
#   /|     c     +-----+


from numpy import *                 # Grab all of the NumPy functions
from matplotlib.pyplot import *     # Grab MATLAB-like plotting functions
import control                      # import the control system functions

# Uncomment to use LaTeX to process the text in figure
rc('text',usetex=True)

m = 1.;             # kg
k = 2;             # spring constant - N/m
wn = sqrt(k/m)      # Natural Frequency (rad/s)

c = 2.5;             # damping coeff - N/(m/s)
z = c/(2*wn*m)      # damping ratio


# Set up simulation parameters
t = r_[0:5:500j]            # time for simulation, 0-5s with 500 points in-between


# ----- Try Proportional-Integral-Derivative Control ------------------------------------
kp = 12                    # The proportional gain
kd = 5                     # The derivative gain
ki = 10                    # The integral gain

# Define the closed-loop transfer function
numPID = [kd,kp,ki]
denPID = [m,(c + kd),(k + kp),ki]
sysPID = control.tf(numPID,denPID);


# Let's start it at t=0.5s for clarity in plotting
Xd = zeros(500)  # Define an array of all zeros
Xd[50:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)
Xd[200:] = 0.6   # Make the elements after 2.5s = 0.5

# run the simulation - utilize the built-in forced_response function
[T_PID,yout_PID,xout_PID] = control.forced_response(sysPID,t,Xd)

# Calculate the error terms
error = Xd - yout_PID
error_deriv = r_[0,diff(error)]
error_int = trapz(error,T_PID)

# Calculate the "derivative on measurement" term
error_measurement = -r_[0,diff(yout_PID)]

# Calculate the force input (the output of the PID controller)
force = kp*error + ki*error_int + kd*error_deriv        # Direct application

# Force from "derivative on measurement" method
force_measurement = kp*error + ki*error_int + kd*error_measurement  


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

plot(t,Xd,color='red',linewidth=2,linestyle='--',label='Reference')
plot(T_PID,yout_PID,color='blue',linewidth=2,label='Response')

xlim(0,3)
ylim(0,1.41)

leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# Uncomment below to save the figure as a high-res pdf in the current folder
savefig('PIDControl_2Step_Resp.png')

# show the figures
# show()

#----- Plot the error
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
ylabel('Error (m)',family='CMU Serif',fontsize=22,weight='bold',labelpad=10)

plot(T_PID,error,color='blue',linewidth=2,label='Error')

xlim(0,3)


# leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
# ltext  = leg.get_texts() 
# setp(ltext,family='CMU Serif',fontsize=16)

# Uncomment below to save the figure as a high-res pdf in the current folder
savefig('PIDControl_2Step_Resp_Error.png')

# show the figures
# show()

#----- Plot the error_deriv
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
ylabel(r'$\frac{d}{dt}(\mbox{Error})$',family='CMU Serif',fontsize=22,weight='bold',labelpad=2)

plot(T_PID,error_deriv,color='blue',linewidth=2,label='Error')

xlim(0,3)

# Uncomment below to save the figure as a high-res pdf in the current folder
savefig('PIDControl_2Step_Resp_ErrorDeriv.png')

# show the figures
# show()

# leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
# ltext  = leg.get_texts() 
# setp(ltext,family='CMU Serif',fontsize=16)

# Uncomment below to save the figure as a high-res pdf in the current folder
# savefig('PIDControl_2Step_Resp_Error.png')

# show the figures
# show()

#----- Plot the force
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
ylabel('Force (N)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)

plot(T_PID,force,color='blue',linewidth=2,label='Force Input')

xlim(0,3)

# leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
# ltext  = leg.get_texts() 
# setp(ltext,family='CMU Serif',fontsize=16)

# Uncomment below to save the figure as a high-res pdf in the current folder
savefig('PIDControl_2Step_Resp_Force.png')


#----- Plot the force
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
ylabel('Force (N)',family='CMU Serif',fontsize=22,weight='bold',labelpad=5)

plot(T_PID,force,color='red',linewidth=2,label='Direct Application')
plot(T_PID,force_measurement,color='blue',linewidth=2,linestyle='--',label='Derivative on Measurement')

xlim(0,3)

leg = legend(loc='upper right', fancybox=True,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# Uncomment below to save the figure as a high-res pdf in the current folder
savefig('PIDControl_2Step_Resp_ForceMeasure.png')

# show the figures
show()