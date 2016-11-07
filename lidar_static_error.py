import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def read_lidar_from_csv(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    return array[:, 0], array[:, 1], array[:, 2], array[:, 3], array[:, 4] * 100, array[:, 5]


def plot_scan_points(filename):
    timestamp_header, layer, echo, angle, distance, echo_width = read_lidar_from_csv(filename)

    # first read to get number of scans
    file_line_size = timestamp_header.size
    number_of_scans = 0
    last_timestamp = timestamp_header[0]
    for i in range(file_line_size):
        # count timestamps
        if timestamp_header[i] != last_timestamp:
            number_of_scans += 1
            last_timestamp = timestamp_header[i]
    print "number of scans:", number_of_scans
    frequencies = np.zeros(number_of_scans)
    timestamps = np.zeros(number_of_scans)
    last_timestamp = timestamp_header[0]
    timestamps[0] = timestamp_header[0]
    counter = 0
    # count echo per layer
    echo_counter = np.zeros((number_of_scans, 4, 4))
    first_index = 0
    for i in range(file_line_size):
        if counter < number_of_scans:
            echo_counter[counter][layer[i]][echo[i]] += 1
        if timestamp_header[i] != last_timestamp and counter < number_of_scans:
            frequencies[counter] = (1000 / (timestamp_header[i] - last_timestamp))
            timestamps[counter] = timestamp_header[i]
            last_timestamp = timestamp_header[i]
            counter += 1
            first_index = i
    echo_counter[:, :, 3] = echo_counter[:, :, 0] + echo_counter[:, :, 1] + echo_counter[:, :, 2]
    fig = plt.figure(figsize=(16.0, 16.0))

    plt.title(filename)
    # stacked barplots for the echos
    subplot_echo(echo_counter[:, :, 0], 1, "echo 0", number_of_scans)
    subplot_echo(echo_counter[:, :, 1], 2, "echo 1", number_of_scans)
    subplot_echo(echo_counter[:, :, 2], 3, "echo 2", number_of_scans)
    subplot_echo(echo_counter[:, :, 3], 4, "echo 0 + echo 1 + echo 2", number_of_scans)

    # bar plot for the frequency
    plt.subplot(5, 1, 5)
    plt.title('frequencies')
    plt.bar(np.arange(number_of_scans), frequencies, color='y', edgecolor="none")
    plt.xlabel('scan number')
    plt.ylabel('[Hz]')
    plt.grid()
    verticalalignment = 'bottom'
    plt.tight_layout()
    plt.show()


def subplot_echo(echo_points, subplot_number, title, number_of_scans):
    plt.subplot(5, 1, subplot_number)
    plt.title(title)
    layer0 = tuple(echo_points[:, 0])
    layer1 = tuple(echo_points[:, 1])
    layer2 = tuple(echo_points[:, 2])
    layer3 = tuple(echo_points[:, 3])
    l0 = plt.bar(np.arange(number_of_scans), layer0, color='r', bottom=0, edgecolor="none")
    l1 = plt.bar(np.arange(number_of_scans), layer1, color='y', bottom=layer0, edgecolor="none")
    l2 = plt.bar(np.arange(number_of_scans), layer2, color='g', bottom=tuple(echo_points[:, 0] + echo_points[:, 1]),
                 edgecolor="none")
    l3 = plt.bar(np.arange(number_of_scans), layer3, color='b',
                 bottom=tuple(echo_points[:, 0] + echo_points[:, 1] + echo_points[:, 2]), edgecolor="none")
    plt.xlabel('scan number')
    plt.ylabel('scan points in package')
    plt.legend((l0[0], l1[0], l2[0], l3[0]), ("layer0", "layer1", "layer2", "layer3"))


def plot_distances(filename):
    timestamp_header, layer, echo, angle, distance, echo_width = read_lidar_from_csv(filename)
    file_line_size = timestamp_header.size
    number_of_scans = 0
    last_timestamp = timestamp_header[0]
    min_angle = np.zeros(4)
    max_angle = np.zeros(4)
    for i in range(file_line_size):
        # count timestamps
        if angle[i] < min_angle[layer[i]]:
            min_angle[layer[i]] = angle[i]
        if angle[i] > max_angle[layer[i]]:
            max_angle[layer[i]] = angle[i]
        if timestamp_header[i] != last_timestamp:
            number_of_scans += 1
            last_timestamp = timestamp_header[i]
    print "number of scans:", number_of_scans
    print "minimal angles per layer: \n", min_angle[0], ", ", min_angle[1], ", ", min_angle[2], ", ", min_angle[
        3], "\n "
    print "maximal angles per layer: \n", max_angle[0], ", ", max_angle[1], ", ", max_angle[2], ", ", max_angle[
        3], "\n "
    timestamps = np.zeros(number_of_scans)
    last_timestamp = timestamp_header[0]
    timestamps[0] = timestamp_header[0]
    counter = 0

    echo_counter = np.zeros((number_of_scans, 4, 4))
    distances = np.zeros((number_of_scans, 4, ((int)(-(np.min(min_angle) - np.max(max_angle)) * 2))))
    angles = np.zeros((4, ((int)(-(np.min(min_angle) - np.max(max_angle)) * 2))))
    first_index = 0
    for i in range(file_line_size):
        if counter < number_of_scans:
            distances[counter][layer[i]][(angle[i] - min_angle[layer[i]]) * 2] = distance[i]
            angles[layer[i]][(angle[i] - min_angle[layer[i]]) * 2] = angle[i]
        if timestamp_header[i] != last_timestamp and counter < number_of_scans:
            timestamps[counter] = timestamp_header[i]
            last_timestamp = timestamp_header[i]
            counter += 1
            first_index = i

    means = np.zeros((4, np.size(angles[0, :])))
    mins = np.zeros((4, np.size(angles[0, :])))
    maxs = np.zeros((4, np.size(angles[0, :])))
    for i in range(4):  # each layer
        for j in range(np.size(angles[0, :])):  # each angle
            means[i][j] = np.mean(distances[:, i, j])
            mins[i][j] = np.min(distances[:, i, j])
            maxs[i][j] = np.max(distances[:, i, j])
    fig = plt.figure(figsize=(16.0, 16.0))
    plt.title(filename)
    subplot_distances(np.trim_zeros(means[0]), np.trim_zeros(mins[0]), np.trim_zeros(maxs[0]), np.trim_zeros(angles[0]),
                      "layer 0", 1, color='r')
    subplot_distances(np.trim_zeros(means[1]), np.trim_zeros(mins[1]), np.trim_zeros(maxs[1]), np.trim_zeros(angles[1]),
                      "layer 1", 2, color='y')
    subplot_distances(np.trim_zeros(means[2]), np.trim_zeros(mins[2]), np.trim_zeros(maxs[2]), np.trim_zeros(angles[2]),
                      "layer 2", 3, color='g')
    subplot_distances(np.trim_zeros(means[3]), np.trim_zeros(mins[3]), np.trim_zeros(maxs[3]), np.trim_zeros(angles[3]),
                      "layer 3", 4, color='b')
    plt.show()
    return angles, mins, means, maxs


def subplot_distances(distance_means, distance_mins, distance_maxs, angles, title, layer_number, color):
    plt.subplot(4, 1, layer_number)
    plt.errorbar(angles, distance_means, yerr=[distance_means - distance_mins, distance_maxs - distance_means], fmt='x',
                 color=color)
    plt.plot(angles, distance_means, 'k', color=color)
    plt.xlabel('relative scanner angle [degree]')
    plt.ylabel('distance [cm]')
    plt.tight_layout()
    plt.grid()


# pl.savefig('result_plots.pdf')
# plot_scan_points(sys.argv[1])
plot_distances("logs/lidar_static_against_wall/mid_const.csv")
