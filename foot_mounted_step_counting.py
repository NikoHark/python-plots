import sys
import StringIO
import numpy as np
import pandas as pd
import pylab as pl
import csv

LIDAR = 'log_file.csv'

def rewrite_lidar_data(path):
    with open(path, 'rU') as inputData:
        with open('some.csv', 'wb') as outputData:
            reader = csv.reader(inputData)
            writer = csv.writer(outputData)
            timestamp = 0
            length = 0
            counter = 0
            for row in reader:
                if(length == counter):
                    counter = 0
                    length = int(row[1])
                    timestamp = float(row[0])
                    print (timestamp, ", ", length)
                    writer.writerow(row)
                else: 
                    #writer.writerow(np.append(timestamp,row))
                    counter+=1


def plot(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    print ("data size", array.shape)
    #timestamp, layer, echo, angle, distance, echo_width
    timestamp_header = array[:, 0]
    layer = array[:,1]
    echo = array[:,2]
    angle = array[:,3]
    distance = array[:,4]
    echo_width = array[:,5]

    length = timestamp_header.size
    scan_counter = 0
    angle_counter_layer0 = 0
    last_timestamp = timestamp_header[0]
    layer0_max_angle = angle[0]
    layer0_min_angle = 0
    for i in range(length):
        #count timestamps
        if(timestamp_header[i] != last_timestamp):
            scan_counter+=1
            last_timestamp=timestamp_header[i]
        #count angles per layer
        if(timestamp_header[i] == timestamp_header[0] and layer[i] == 0 and echo[i]== 0):
            angle_counter_layer0+=1
            if(angle_counter_layer0 == 1):
                layer0_min_angle = angle[i]
                print ("timestamp_header[i]:", timestamp_header[i+1] , ", timestamp_header[0]: ", timestamp_header[0])
    print ("number of scans", scan_counter, ", number of scans in layer 0: ", angle_counter_layer0)
    # frequency per scan
    # track exact angle ranges per layer 
    # max, mean, min per angle
    frequencies = np.zeros(scan_counter)
    timestamps = np.zeros(scan_counter)
    last_timestamp = timestamp_header[0]
    timestamps[0] = timestamp_header[0]
    counter = 0

    #distances
    #angles = np.zeros((angle_counter_layer0+1,2))
    #angles[:,0] = np.arange(angle_counter_layer0+1)
    max_distances = np.zeros(angle_counter_layer0)
    min_distances = np.zeros(angle_counter_layer0)
    mean_distances = np.zeros(angle_counter_layer0)
    angle_counter_tmp = 0
    for i in range(length):
        if(counter == 0 and layer[i] == 0):
            #angles[angle_counter_tmp][1] = angle[i]
            angle_counter_tmp+=1

        if(timestamp_header[i] != last_timestamp and counter < scan_counter):
            frequencies[counter] = (1000/(timestamp_header[i]-last_timestamp))
            timestamps[counter] = timestamp_header[i]
            counter+=1


    print ("layer0_min_angle: ", layer0_min_angle, ", layer0_max_angle: ", layer0_max_angle)
    #print angles

    


    fig = pl.figure(figsize=(16.0, 16.0))
    pl.title(filename)

    pl.subplot(5,1,1)
    pl.title('frequencies')
    pl.plot(timestamps, frequencies, label='frequencies')
    #pl.plot(timestamp_header, xMeanUntil)
    pl.grid()

    #pl.xticks(stepValues, np.arange(1, counter+1))

  
    #bar plot for the frequency
    pl.subplot(5,1,5)
    pl.title('frequencies [Hz]')
    width = 0.02
    pl.bar(np.arange(scan_counter)+width, frequencies, width, color='y')
    pl.grid()
    #string = 'mean frequency: ', frequencies.mean()
    #fig.text(0.4, 0.2, string, fontsize=15,
    verticalalignment='bottom'
    pl.show()


def plot_old(filename):
    print ("start reading file")
    file = open(filename)
    data = file.read()
    string = StringIO(data)
    array = np.loadtxt(string)
    print (array.shape)
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
 
    print ('counted steps: ', counter)
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
        print (i, ' length: ', k*np.sqrt(abs(displace*(maximum-minimum)/(avg-minimum))))# 'step number: ', i+1, ' max: ', maximum, ' min: ', minimum, ' avg: ' , avg,
        stepLengths[i] = k*np.sqrt(abs(displace*(maximum-minimum)/(avg-minimum)))
    #print stepLengths
    print (stepLengths.sum())
    
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