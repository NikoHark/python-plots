import numpy as np
import matplotlib.pyplot as plt
import dcaiti_name_helper as dc
from matplotlib import gridspec


#translation
def naive_approach(timestamps, measurements):
    velocity_from_accel = np.zeros(measurements.__len__())
    velocity_from_accel[0] = measurements[0]
    for i in range(measurements.__len__()):
        if i > 0:
            velocity_from_accel[i] = ((velocity_from_accel[i-1])+(measurements[i]*(timestamps[i]-timestamps[i-1])))
    return timestamps, velocity_from_accel


def correction_approach(timestamps, measurements):
    correction_factor = measurements[0:100].mean()
    velocity_from_accel_corrected = np.zeros(measurements.__len__())
    for i in range(measurements.__len__()):
        if i > 0:
            velocity_from_accel_corrected[i] = ((velocity_from_accel_corrected[i-1])+((measurements[i]-correction_factor)*(timestamps[i]-timestamps[i-1])))
    print correction_factor
    return timestamps, velocity_from_accel_corrected


def magnetic_threshhold_approach(timestamps, measurements):
    velocity_from_mag_treshhold = np.zeros(measurements.__len__())
    norm_1 = np.linalg.norm(measurements, ord=1, axis=1)
    for i in range(timestamps.__len__()):
        if i > 70:
            if np.abs(np.max(norm_1[i-70:i])-np.min(norm_1[i-70:i])) > 3.5:
                velocity_from_mag_treshhold[i] = 3
            else:
                velocity_from_mag_treshhold[i] = 0
    return timestamps, velocity_from_mag_treshhold


def acceleration_threshhold_approach(timestamps, measurements):
    length = measurements.__len__()
    #apply correction
    correction_factor = measurements[0:100, 1].mean()
    measurements -= correction_factor
    #threshold
    treshhold = np.zeros(length)
    velocity_from_threshhold = np.zeros(length)
    windowsize = 400
    for i in range(length):
        if i > windowsize:
            if np.abs(np.abs(np.max(measurements[i-windowsize:i, 1]))+np.abs(np.min(measurements[i-windowsize:i, 1]))) > 1.4:
                treshhold[i-windowsize:i] = 3
    for i in range(length):
        if i > 0:
            if treshhold[i] == 3:
                velocity_from_threshhold[i] = (velocity_from_threshhold[i-1]+(measurements[i, 1]*(timestamps[i]-timestamps[i-1])))
            else:
                velocity_from_threshhold[i] = velocity_from_threshhold[i-1]
    velocity_from_threshhold[velocity_from_threshhold < 0] = 0
    return timestamps, velocity_from_threshhold


def calculate_path(approach, case):
    file_name, timestamp, title = dc.get_case_data(case)

    timestamps_gyroscope, gyroscope_measurements = dc.read_vectors_from_csv(file_name + "gyroscopeLog" + timestamp + ".csv")
    timestamps_gyroscope -= timestamps_gyroscope[0]
    timestamps_gyroscope /= 1000000000

    timestamps_accelerometer, accelerometer_measurements = dc.read_vectors_from_csv(file_name + "accelLog" + timestamp + ".csv")
    timestamps_accelerometer -= timestamps_accelerometer[0]
    timestamps_accelerometer /= 1000000000

    timestamps_magnetometer, magnetometer_measurements = dc.read_vectors_from_csv(file_name + "magneticFieldLog" + timestamp + ".csv")
    timestamps_magnetometer -= timestamps_magnetometer[0]
    timestamps_magnetometer /= 1000000000

    timestamps_rotation, rotations = timestamps_gyroscope, gyroscope_measurements[:, 2]
    rotations *= (180/np.pi)
    if approach is dc.Approach.naive:
        timestamps_translation, translations = naive_approach(timestamps_accelerometer, accelerometer_measurements[:, 1])
    elif approach is dc.Approach.corrected:
        timestamps_translation, translations = correction_approach(timestamps_accelerometer, accelerometer_measurements[:, 1])
    elif approach is dc.Approach.mag_tresh:
        timestamps_translation, translations = magnetic_threshhold_approach(timestamps_magnetometer, magnetometer_measurements)
    elif approach is dc.Approach.acc_tresh:
        timestamps_translation, translations = acceleration_threshhold_approach(timestamps_accelerometer, accelerometer_measurements)
    else:
        timestamps_translation, translations, rotations = dc.read_odo_from_csv(file_name + "odoLog" + timestamp + ".csv")
        timestamps_translation -= timestamps_translation[0]
        timestamps_translation /= 1000
        timestamps_rotation = timestamps_translation
        rotations *= (-1)

    index_rotation = 1
    index_translation = 1
    counter = 1
    x_y_phi = np.zeros((3, timestamps_rotation.__len__()+timestamps_translation.__len__()))
    while index_rotation < timestamps_rotation.__len__() and index_translation < timestamps_translation.__len__():
        #rotate or translate, depending on current latest ts
        if timestamps_rotation[index_rotation] < timestamps_translation[index_translation]:
            x_y_phi[0, counter] = x_y_phi[0, counter-1]
            x_y_phi[1, counter] = x_y_phi[1, counter-1]
            x_y_phi[2, counter] = (x_y_phi[2, counter-1] + (rotations[index_rotation] * (timestamps_rotation[index_rotation] - timestamps_rotation[index_rotation-1])))
            index_rotation += 1
        elif timestamps_rotation[index_rotation] > timestamps_translation[index_translation]:
            distance = (translations[index_translation] * (timestamps_translation[index_translation]-timestamps_translation[index_translation-1]))
            x_y_phi[0, counter] = (x_y_phi[0, counter-1] + (np.cos(np.deg2rad(x_y_phi[2, counter-1])) * distance))
            x_y_phi[1, counter] = (x_y_phi[1, counter-1] + (np.sin(np.deg2rad(x_y_phi[2, counter-1])) * distance))
            x_y_phi[2, counter] = x_y_phi[2, counter-1]
            index_translation += 1
        else: #timestamps equal
            distance = (translations[index_translation] * (timestamps_translation[index_translation]-timestamps_translation[index_translation-1]))
            x_y_phi[0, counter] = (x_y_phi[0, counter-1] + (np.cos(np.deg2rad(x_y_phi[2, counter-1])) * distance))
            x_y_phi[1, counter] = (x_y_phi[1, counter-1] + (np.sin(np.deg2rad(x_y_phi[2, counter-1])) * distance))
            x_y_phi[2, counter] = (x_y_phi[2, counter-1] + (rotations[index_rotation] * (timestamps_rotation[index_rotation] - timestamps_rotation[index_rotation-1])))
            index_translation += 1
            index_rotation += 1
        counter += 1
        # print counter
    return x_y_phi


def plotXY(case, approach, color):
    xyphi = calculate_path(approach, case)
    xyphi[1, np.abs(xyphi[0])+np.abs(xyphi[1])+np.abs(xyphi[2]) == 0] = np.nan
    plt.plot(xyphi[0, :], xyphi[1, :], 'k', color=color, label=dc.Approach.tostring(approach))
    # plt.plot(xyphi[0, :], xyphi[1, :], 'x', color='black')


def benchmark(case):
    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(1, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    # plotXY(case, dc.Approach.odometry, 'black')
    xyphi = calculate_path(dc.Approach.odometry, case)
    xyphi[1, np.abs(xyphi[0])+np.abs(xyphi[1])+np.abs(xyphi[2]) == 0] = np.nan
    plt.plot(xyphi[0, :], xyphi[1, :], 'k', color='black', label=dc.Approach.tostring(dc.Approach.odometry))
    plt.plot(xyphi[0, :], xyphi[1, :], 'x', color='black')
    plotXY(case, dc.Approach.naive, 'red')
    plotXY(case, dc.Approach.corrected, 'green')
    plotXY(case, dc.Approach.mag_tresh, 'blue')
    plotXY(case, dc.Approach.acc_tresh, 'm')
    plt.xlabel('x [Meter]')
    plt.ylabel('y [Meter]')
    plt.axis('equal')
    plt.xlim(-5)
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


benchmark(dc.Case.static)
