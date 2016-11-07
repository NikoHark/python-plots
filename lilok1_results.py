import sys
import numpy as np
import pandas as pd
import matplotlib.pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math as m

def read_lidar_from_csv(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    return array[:,0], array[:,1], array[:,2], array[:,3], array[:,4], array[:,5], array[:,6]

def subplot_histogram( plot_size,subplot_index, array, array_label):
    plt.subplot(plot_size, 1, subplot_index)
    plt.hist(array, )
    plt.xlabel(array_label)
    plt.tight_layout()
    plt.grid()


def plot_histograms(filename):
    timestamp, total_error, angular_error, lat_error1, long_error1, lat_error2, long_error2 = read_lidar_from_csv(filename)
    print "number of timestamps:", np.size(timestamp)
    print "tot: ", total_error
    print "ang", angular_error
    print "lat1", lat_error1
    print "lat2", lat_error2
    print "long1", long_error1
    print "long2", long_error2
    fig = plt.figure(figsize=(16.0, 9.0))
    plt.title(filename)
    subplot_histogram(6, 1, total_error, "Total Translation Error [Meter]")
    subplot_histogram(6, 2, angular_error, "Total Rotation Error [Grad]")
    subplot_histogram(6, 3,lat_error1, "Latitude Error (Reference Point 1)")
    subplot_histogram(6, 4, long_error1, "Longitude Error (Reference Point 1)")
    subplot_histogram(6, 5,lat_error2, "Latitude Error (Reference Point 2)")
    subplot_histogram(6, 6, long_error2, "Longitude Error (Reference Point 2)")
    plt.show()


def plot_2d(filename):
    timestamp, total_error, angular_error, lat_error1, long_error1, lat_error2, long_error2 = read_lidar_from_csv(filename)
    fig = plt.figure(figsize=(10.0, 10.0))
    plt.plot(lat_error1, long_error1, "x", color="black", label="error1")
    plt.plot(lat_error2, long_error2, 'x', color='blue', label="error2")
    # plt.plot(lat_error1.mean(), long_error1.mean(), "o", color="red", label="mean1")
    # plt.plot(lat_error2.mean(), long_error2.mean(), "o", color="orange", label="mean2")
    # xerr=[(lat_error1.mean()-lat_error1.min()), (lat_error1.mean()-lat_error1.min())],
    plt.errorbar(lat_error1.mean(), long_error1.mean(), fmt='o', color="red",  label="mean1")
    plt.errorbar(lat_error2.mean(), long_error2.mean(), fmt='o', color="red",  label="mean2")
    plt.xlabel('Latitude Error')
    plt.ylabel('Longitude Error')
    plt.tight_layout()
    plt.grid()
    plt.legend()
    plt.title(filename)
    plt.show()

def plot_3d(filename):
    data = pd.read_csv(filename, ";")

    array = np.array(data)
    print(array.size)
    timestamp, lat, long = array[:, 0], array[:, 1], array[:, 2]
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    plt.scatter(lat, long, label="ground truth")
    plt.xlabel("angle offset")
    plt.ylabel("distance offset")
    # plt.clabel("longitude")
    plt.grid()
    plt.legend()
    plt.title(filename)
    plt.show()



# plot_histograms(sys.argv[1])
plot_3d("/home/niko/dev/workspaces/python/plots/logs/lilok_results/lilok1-a.txt")

#pl.savefig('sensor.pdf')


