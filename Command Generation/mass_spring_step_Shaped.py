#! /usr/bin/env python 

##########################################################################################
# mass_spring_step_Shaped.py
#
# Script to analyze a spring-mass system response to various inputs in position
# 
# Created: 9/26/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################

# The baseline system, a simple mass-spring-damper system
#
#    +---> Xd       +---> X
#    |              |
#    |           +-----+
#    |     k     |     |
#    +--\/\/\/\--+  M  |
#                |     |
#                +-----+
#
# Step input in Y, response of the mass is X

from numpy import *             # Grab all of the NumPy functions
from matplotlib.pyplot import * # Grab MATLAB plotting functions
import control                  # import the control system functions
from InputShaping import *      # import the input shaping toolbox

# Uncomment to use LaTeX to process the text in figure
# from matplotlib import rc
# rc('text',usetex=True)

m = 1.;             # kg
k = (2.*pi)**2;     # N/m (Selected to give an undamped wn of 1Hz)
wn = sqrt(k/m)      # Natural Frequency (rad/s)


# Define the system to use in simulation - in transfer function form here
num = [wn**2];
den = [1.,0.,wn**2];

sys = control.tf(num,den);
       

# Set up simulation parameters
t = r_[0:5:0.001]            # time for simulation, 0-5s with 500 points in-between


#-----  Look at a  step response --------------------------------------------------------
# Let's start it at t=0.5s for
U = zeros(5000)  # Define an array of all zeros
U[500:] = 1      # Make all elements of this array index>50 = 1 (all after 0.5s)

# run the simulation - utilize the built-in initial condition response function
[T_un,yout_un,xout_un] = control.forced_response(sys,t,U)

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

plot(T_un,U,color='red',linewidth=2,linestyle='--',label='Step Input')
plot(T_un,yout_un,color='blue',linewidth=2,label='Response')

xlim(0,3)
ylim(0,2.5)

leg = legend(loc='upper right', fancybox=True,ncol=2,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
# savefig('Step_Resp_Unshaped.pdf')

# show the figure
# show()



#-----  Look at a ramp-based input ------------------------------------------------------
# Let's start it at t=0.5s for
Uramp = zeros(5000)  # Define an array of all zeros
Uramp[500:1999] = 2./3*t[0:1499]
Uramp[1999:] = 1      # Make all elements of this array index>2000 = 1 (all after 2.0s)

# run the simulation - utilize the built-in initial condition response function
[T_ramp,yout_ramp,xout_ramp] = control.forced_response(sys,t,Uramp)

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

plot(T_ramp,Uramp,color='red',linewidth=2,linestyle='--',label='Ramp-based Input')
plot(T_ramp,yout_ramp,color='blue',linewidth=2,label='Response')

xlim(0,3)
ylim(0,2.5)

leg = legend(loc='upper right', fancybox=True,ncol=2,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
# savefig('Step_Resp_UnshapedRamp.pdf')

# show the figure
# show()



#----- Try Input Shaping ----------------------------------------------------------------
#---  Design the input shaper
[shaper, exactshaper] = ZV(wn/(2.*pi),0.,0.001)

# Create the shaped command
[t_shap,U_shaped] = conv(transpose(U),shaper,0.001);

# run the simulation - utilize the built-in initial condition response function
[T_shaped,yout_shap,xout_shap] = control.forced_response(sys,t_shap,U_shaped,hmax=0.01)

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

plot(T_shaped,U_shaped,color='red',linewidth=2,linestyle='--',label='ZV-Shaped Input')
plot(T_shaped,yout_shap,color='blue',linewidth=2,label='Response')

ylim(0,2.5)
xlim(0,3)

leg = legend(loc='upper right', fancybox=True,ncol=2,borderaxespad=0.1)
ltext  = leg.get_texts() 
setp(ltext,family='CMU Serif',fontsize=16)

# save the figure as a high-res pdf in the current folder
# savefig('Step_Resp_ZVshaped.pdf')

# show the figure
show()




