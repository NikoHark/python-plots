import sys
import tempfile
from StringIO import StringIO
import numpy as np
import matplotlib as mp 
import math as m
import pylab as pl

def plot(filename):
    print "start reading file"
    file = open(filename)
    data = file.read()
    string = StringIO(data)
    array = np.loadtxt(string)
    print array.shape
    #sensor data storage
    timestamps = array[:,0]
    xValues = array[:,1]
    yValues = array[:,2]
    zValues = array[:,3]-9.81
    sumValues = np.sqrt(xValues*xValues+yValues*yValues+(zValues+9.81)*(zValues+9.81))
    sumValuesZeroGSubstracted = np.sqrt(xValues*xValues+yValues*yValues+(zValues)*(zValues))
    
    #mean values
    xMean = xValues.mean()
    yMean = yValues.mean()
    zMean = zValues.mean()
    sumMean = sumValues.mean()
    
    
    dataSize = xValues.size
    xMeanUntil = np.zeros(dataSize)
    yMeanUntil = np.zeros(dataSize)
    zMeanUntil = np.zeros(dataSize)
    sumMeanUntil = np.zeros(dataSize)
    for i in range(0, dataSize):
        xMeanUntil[i] = xValues[0:i].mean()
        yMeanUntil[i] = yValues[0:i].mean()
        zMeanUntil[i] = zValues[100:i].mean()
        sumMeanUntil[i] = sumValues[:i].mean()+1.6
    #finding steps
    waitForPeak = False
    foundPeak = False
    counter = 0
    for i in range(dataSize):
        if(sumValues[i] > sumMeanUntil[i] and not foundPeak):
            counter = counter + 1
            foundPeak = True
        if(sumValues[i] < sumMeanUntil[i]):
            foundPeak = False
 
    print 'counted steps: ', counter
    #finding step boundaries
    stepBoundaries = np.zeros(counter)
    counter = 0
    waitForPeak = False
    foundPeak = False
    for i in range(dataSize):
        if(sumValues[i] > sumMeanUntil[i] and not foundPeak):
            counter= counter + 1
            foundPeak = True
        if(sumValues[i] > sumMeanUntil[i] and sumValues[stepBoundaries[counter-1]] < sumValues[i]):
            stepBoundaries[counter-1] = i
        if(sumValues[i] < sumMeanUntil[i]): #wait to get over mean
            foundPeak = False
    
    #calculate step beginnings/endings
    stepValues = np.zeros(counter)
    for i in range(0, counter):
        stepValues[i] = timestamps[stepBoundaries[i]]
    
    #calculate steps length with simple formula: d = k * sqrt((max-min)/(avg-min)*sum(accel-avg))
    stepLengths = np.zeros(counter)
    for i in range(0, counter-1):
        if i == 0:
            stepInterval = sumValuesZeroGSubstracted[0:stepBoundaries[0]] # zValues[0:stepBoundaries[0]]
        else:
            stepInterval = sumValuesZeroGSubstracted[stepBoundaries[i-1]:stepBoundaries[i]] # zValues[stepBoundaries[i-1]:stepBoundaries[i]]
        avg = stepInterval.mean()
        minimum = stepInterval.min()
        maximum = stepInterval.max()
        velocity = 0
        displace = 0
        for j in range(stepInterval.size):
            velocity += (stepInterval[j]-avg)
            displace += velocity
        k = 0.0249
        print i, ' length: ', k*np.sqrt(abs(displace*(maximum-minimum)/(avg-minimum)))# 'step number: ', i+1, ' max: ', maximum, ' min: ', minimum, ' avg: ' , avg, 
        stepLengths[i] = k*np.sqrt(abs(displace*(maximum-minimum)/(avg-minimum)))
    #print stepLengths
    print stepLengths.sum()
    
    #plotting figure
    fig = pl.figure(figsize=(16.0, 16.0))
    pl.title(filename)
    
    
    pl.subplot(5,1,1)
    pl.title('x sensor values')
    pl.plot(timestamps, xValues, label='X values')
    pl.plot(timestamps, xMeanUntil)
    pl.grid()
    pl.xticks(stepValues, np.arange(1, counter+1))
    
    pl.subplot(5,1,2)
    pl.title('y sensor values')
    pl.plot(timestamps, yValues, label='Y values')
    pl.plot(timestamps, yMeanUntil)
    pl.grid()
    pl.xticks(stepValues, np.arange(1, counter+1))    
    
    pl.subplot(5,1,3)
    pl.title('z sensor values')
    pl.plot(timestamps, zValues, label='Z values')
    pl.plot(timestamps, zMeanUntil)
    pl.grid()
    pl.xticks(stepValues, np.arange(1, counter+1))
    

    pl.subplot(5,1,4)
    pl.title('sum sensor values')
    pl.plot(timestamps, sumValues, label='vector sum values')
    pl.plot(timestamps, sumMeanUntil, label = 'current mean')
    pl.grid()
    pl.xticks(stepValues, np.arange(1, counter+1))

    #bar plot for the step length
    pl.subplot(5,1,5)
    width = 0.35
    pl.bar(np.arange(counter)+width, stepLengths, width, color='y')
    pl.grid()
    string = 'overall length: ', stepLengths.sum()
    fig.text(0.4, 0.2, string, fontsize=15,
    verticalalignment='bottom')
    
    pl.savefig('sensor.pdf')
    pl.show()
    

plot(sys.argv[1])