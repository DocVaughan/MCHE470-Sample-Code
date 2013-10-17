#! /usr/bin/env python 

##########################################################################################
# serial_realtime_matplotlib.py
#
# Script to plot data from a serial connection in realtime
#
# NOTE: Plotting is set up for output, not viewing on screen.
#       So, it will likely be ugly on screen. The saved PDFs should look
#       better.
#
# Adapted from: https://gist.github.com/electronut/5641933
# 
# Created: 10/12/13 
#   - Joshua Vaughan 
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   *
#
##########################################################################################


import sys, serial
import numpy as np
from time import sleep
from collections import deque
from matplotlib import pyplot as plt

# class that holds analog data for N samples
class AnalogData:
  # constr
  def __init__(self, maxLen):
    self.unshaped = deque([0.0]*maxLen)
    self.A1 = deque([0.0]*maxLen)
    self.A2 = deque([0.0]*maxLen)
    self.shaped = deque([0.0]*maxLen)
    self.maxLen = maxLen

  # ring buffer
  def addToBuf(self, buf, val):
    if len(buf) < self.maxLen:
      buf.append(val)
    else:
      buf.pop()
      buf.appendleft(val)

  # add data
  def add(self, data):
    assert(len(data) == 4)
    self.addToBuf(self.A1, data[1])
    self.addToBuf(self.A2, data[2])
    self.addToBuf(self.shaped, data[3])
    
# plot class
class AnalogPlot:
  # constr
  def __init__(self, analogData):
    # set plot to animated
    fig = plt.figure(figsize=(8,4.5))
    plt.ion() 
    
    
    plt.subplot(2,1,1)
    self.shapedline, = plt.plot(analogData.shaped,color='black',label=r'Shaped Command')#,linestyle='.-')
    plt.xticks([])
    plt.ylim([0, 1.501])
    plt.yticks([0,0.5,1.0],['0','0.5','1.0'])
    leg = plt.legend(loc='upper right', fancybox=True,borderaxespad=0.1)
    ltext  = leg.get_texts() 
    plt.setp(ltext,family='CMU Serif',fontsize=16)
    
    
    plt.subplot(2,1,2)
    self.A1line, = plt.plot(analogData.A1,color='blue',label=r'$A_1$ Component')#,linestyle='--')
    self.A2line, = plt.plot(analogData.A2,color='red',label=r'$A_2$ Component')#,linestyle='-.')
    plt.ylim([0, 1.501])
    plt.yticks([0,0.5,1.0],['0','0.5','1.0'])
    
    leg = plt.legend(loc='upper right', fancybox=True,borderaxespad=0.1,ncol = 2)
    ltext  = leg.get_texts() 
    plt.setp(ltext,family='CMU Serif',fontsize=16)
    
    plt.xlabel('Time Sample',fontsize=22,labelpad=5)
#     plt.ylabel('Amplitude',fontsize=22,weight='bold',labelpad=10)
    plt.text(-15, 2, 'Amplitude',family='CMU Serif',weight='bold',fontsize=22,rotation=90)

    
  # update plot
  def update(self, analogData):
    self.A1line.set_ydata(analogData.A1)
    self.A2line.set_ydata(analogData.A2)
    self.shapedline.set_ydata(analogData.shaped)
    plt.draw()

# main() function
def main():
  strPort = '/dev/tty.usbserial-A601EGPS'


  # plot parameters
  analogData = AnalogData(100)
  analogPlot = AnalogPlot(analogData)

  print 'plotting data...'

  # open serial port
  ser = serial.Serial(strPort, 9600)
  
  while True:
    try:
      line = ser.readline()
#       print line
      data = [float(val) for val in line.split()]
      #print data
      if(len(data) == 4):
        analogData.add(data)
        analogPlot.update(analogData)
    except KeyboardInterrupt:
      print 'exiting'
      break
  # close serial
  ser.flush()
  ser.close()

# call main
if __name__ == '__main__':
  main()
