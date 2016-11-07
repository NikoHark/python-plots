import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import dcaiti_name_helper as dc


def plot_test_drive(case):
    folder_name, timestamp, title = dc.get_case_data(case)
    #get odometry measurements and transform timestamps from milliseconds to seconds
    ts_odo, velocity, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    #get smartphone measurements and transform timestamps from nanoseconds to seconds
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_gravity, vector_gravity = dc.read_vectors_from_csv(folder_name + "gravityLog" + timestamp + ".csv")
    ts_lin_accel, vector_lin_accel = dc.read_vectors_from_csv(folder_name + "linearAccelerationLog" + timestamp + ".csv")
    ts_gyro, vector_gyro = dc.read_vectors_from_csv(folder_name + "gyroscopeLog" + timestamp + ".csv")
    ts_mag, vector_mag = dc.read_vectors_from_csv(folder_name + "magneticFieldLog" + timestamp + ".csv")
    ts_orientation, quad_orientation = dc.read_quads_from_csv(folder_name + "orientationLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000000
    ts_gravity -= ts_gravity[0]
    ts_gravity /= 1000000000
    ts_lin_accel -= ts_lin_accel[0]
    ts_lin_accel /= 1000000000
    ts_gyro -= ts_gyro[0]
    ts_gyro /= 1000000000
    ts_mag -= ts_mag[0]
    ts_mag /= 1000000000
    ts_orientation -= ts_orientation[0]
    ts_orientation /= 1000000000
    #plot all data
    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(4, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    plt.plot(ts_odo, velocity, 'k', color='b')
    plt.ylabel('velocity [m/s]')
    plt.tight_layout()
    plt.grid()
    ax2 = fig.add_subplot(gs[0, 1])
    plt.plot(ts_odo, yawrate, 'k', color='g')
    plt.ylabel('yawrate [degree/s]')
    plt.tight_layout()
    plt.grid()
    ax2 = fig.add_subplot(gs[1, 0])
    plt.plot(ts_accel, vector_accel[:, 0], 'k', color='r', label='x')
    plt.plot(ts_accel, vector_accel[:, 1], 'k', color='g', label='y')
    plt.plot(ts_accel, vector_accel[:, 2], 'k', color='b', label='z')
    plt.ylabel('acceleration [m/s^2]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax3 = fig.add_subplot(gs[2, 0])
    plt.plot(ts_lin_accel, vector_lin_accel[:, 0], 'k', color='r', label='x')
    plt.plot(ts_lin_accel, vector_lin_accel[:, 1], 'k', color='g', label='y')
    plt.plot(ts_lin_accel, vector_lin_accel[:, 2], 'k', color='b', label='z')
    plt.ylabel('linear_acceleration [m/s^2]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax4 = fig.add_subplot(gs[3, 0])
    plt.plot(ts_gravity, vector_gravity[:, 0], 'k', color='r', label='x')
    plt.plot(ts_gravity, vector_gravity[:, 1], 'k', color='g', label='y')
    plt.plot(ts_gravity, vector_gravity[:, 2], 'k', color='b', label='z')
    plt.xlabel('time [s]')
    plt.ylabel('gravity [m/s^2]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax5 = fig.add_subplot(gs[1, 1])
    plt.plot(ts_gyro, vector_gyro[:, 0], 'k', color='r', label='x')
    plt.plot(ts_gyro, vector_gyro[:, 1], 'k', color='g', label='y')
    plt.plot(ts_gyro, vector_gyro[:, 2], 'k', color='b', label='z')
    plt.ylabel('gyroscope [rad/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax6 = fig.add_subplot(gs[3, 1])
    plt.plot(ts_mag, vector_mag[:, 0], 'k', color='r', label='x')
    plt.plot(ts_mag, vector_mag[:, 1], 'k', color='g', label='y')
    plt.plot(ts_mag, vector_mag[:, 2], 'k', color='b', label='z')
    plt.ylabel('magnetic field [micro tesla]')
    plt.xlabel('time [s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax7 = fig.add_subplot(gs[2, 1])
    plt.plot(ts_orientation, quad_orientation[:, 0], 'k', color='black', label='w')
    plt.plot(ts_orientation, quad_orientation[:, 1], 'k', color='r', label='x')
    plt.plot(ts_orientation, quad_orientation[:, 2], 'k', color='g', label='y')
    plt.plot(ts_orientation, quad_orientation[:, 3], 'k', color='b', label='z')
    plt.ylabel('orientation [quaternion]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


def show_acceleration_problematic(case):
    folder_name, timestamp, title = dc.get_case_data(case)
    #odo
    ts_odo, velocity_from_odo, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    #smartphone
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000000

    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(3, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    plt.title(title)
    plt.plot(ts_accel, vector_accel[:, 1], 'k', color='g', label='y accel')
    plt.ylabel('acceleration [m/s^2]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    #calculating velocity from linear acceleration data
    velocity_from_accel = np.zeros(vector_accel.__len__())
    velocity_from_accel[0] = vector_accel[0, 1]
    for i in range(vector_accel.__len__()):
        if(i > 0):
            velocity_from_accel[i] = ((velocity_from_accel[i-1])+(vector_accel[i, 1]*(ts_accel[i]-ts_accel[i-1])))

    ax1 = fig.add_subplot(gs[1, 0])
    plt.plot(ts_accel, velocity_from_accel, 'k', color='b', label='smartphone')
    plt.plot(ts_odo, velocity_from_odo, 'k', color='black', label='odometry')
    plt.plot(ts_odo, velocity_from_odo, 'x', color='black')
    plt.ylabel('velocity [m/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()

    #calculating distance from odometry
    odo_distance = np.zeros(ts_odo.__len__())
    for i in range(ts_odo.__len__()):
        if(i > 0):
            odo_distance[i] = (odo_distance[i-1]+(velocity_from_odo[i]*(ts_odo[i]-ts_odo[i-1])))
    ax2 = fig.add_subplot(gs[2, 0])
    #calculating distance from acceleration data
    distance_from_accel = np.zeros(vector_accel.__len__())
    distance_from_accel[0] = vector_accel[0, 1]
    for i in range(vector_accel.__len__()):
        if(i > 0):
            distance_from_accel[i] = ((distance_from_accel[i-1])+(velocity_from_accel[i]*(ts_accel[i]-ts_accel[i-1])))

    plt.plot(ts_odo, odo_distance, 'k', color='black', label='odometry')
    plt.plot(ts_odo, odo_distance, 'x', color='black')
    plt.plot(ts_accel, distance_from_accel, 'k', color='b', label='smartphone')
    plt.ylabel('distance [m]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


def detailed_accel_noise(case):
    folder_name, timestamp, title = dc.get_case_data(case)
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000000
    ts_odo, velocity, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    last_index_before_start = 0
    for i in range(ts_odo.__len__()):
        if(velocity[i] == 0):
            if(velocity[last_index_before_start] < ts_odo[i]):
                last_index_before_start = i
        else:
            break
    first_index_after_end = ts_odo.__len__()
    for i in range(last_index_before_start+1, ts_odo.__len__()):
        if(velocity[i] == 0):
            first_index_after_end = i
            break
    accels_while_steady = []
    ts_accels_while_steady = []
    for i in range(ts_accel.__len__()):
        if(ts_accel[i] < ts_odo[last_index_before_start]-1 or ts_accel[i] > ts_odo[first_index_after_end-1]+1):
            accels_while_steady.append(vector_accel[i, 1])
            ts_accels_while_steady.append(ts_accel[i])
    #print(accels_while_steady)
    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(2, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    print np.mean(accels_while_steady)
    plt.title(title)
    plt.plot(ts_odo, velocity, 'k', color='black', label='velocity from odometry')
    plt.plot(ts_odo[last_index_before_start], velocity[last_index_before_start], 'x', color='black')
    #plt.plot(ts_odo[first_index_after_end], velocity[first_index_after_end], 'x', color='black')
    plt.plot(ts_accel, vector_accel[:, 1], 'k', color='green', label='acceleration from smartphone')
    plt.plot(ts_accels_while_steady, accels_while_steady, 'x', color='blue', label='acceleration from smartphone, v = 0')
    plt.grid()
    plt.ylabel('acceleration [m/s^2] | velocity [m/s]')
    plt.tight_layout()
    plt.legend()
    ax2 = fig.add_subplot(gs[1, 0])
    #print ts_accel.__len__()
    label1 = 'n = ' + str(ts_accels_while_steady.__len__())
    n, bins, patches = plt.hist(accels_while_steady, 50, normed=1, histtype='bar', rwidth=0.8, label=label1)
    plt.axvline(np.mean(accels_while_steady), color='green', linestyle='dashed', linewidth=2)
    plt.xlabel('acceleration [m/s^2]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


def show_good_rotation(case1, case2):
    folder_name1, timestamp1, title1 = dc.get_case_data(case1)
    folder_name2, timestamp2, title2 = dc.get_case_data(case2)
    #odo
    ts_odo, velocity, yawrate = dc.read_odo_from_csv(folder_name1 + "odoLog" + timestamp1 + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    ts_odo1, velocity1, yawrate1 = dc.read_odo_from_csv(folder_name2 + "odoLog" + timestamp2 + ".csv")
    ts_odo1 -= ts_odo1[0]
    ts_odo1 /= 1000
    #smartphone
    ts_gyro, vector_gyro = dc.read_vectors_from_csv(folder_name1 + "gyroscopeLog" + timestamp1 + ".csv")
    #ts_mag, vector_mag = read_vectors_from_csv(foldername1 + "magneticFieldLog" + timestamp1 + ".csv")
    #ts_orientation, quad_orientation = read_quads_from_csv(foldername1 + "orientationLog" + timestamp1 + ".csv")
    ts_gyro1, vector_gyro1 = dc.read_vectors_from_csv(folder_name2 + "gyroscopeLog" + timestamp2 + ".csv")

    #zero timestamp and convert to seconds
    ts_gyro -= ts_gyro[0]
    ts_gyro /= 1000000000
    #ts_mag -= ts_mag[0]
    #ts_mag /= 1000000000
    #ts_orientation -= ts_orientation[0]
    #ts_orientation /= 1000000000

    ts_gyro1 -= ts_gyro1[0]
    ts_gyro1 /= 1000000000

    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(2, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    #convert odometry yawrate to rad/s
    #yawrate *= (2*np.pi/360)
    vector_gyro[:, 2] *= -(360/(2*np.pi))
    vector_gyro1[:, 2] *= -(360/(2*np.pi))
    #print(2*np.pi/360)
    plt.plot(ts_odo, yawrate, 'k', color='black', label='yawrate left turn')
    plt.plot(ts_odo, yawrate, 'x', color='black')
    plt.plot(ts_gyro, vector_gyro[:, 2], 'k', color='b', label='z gyro left turn')

    plt.plot(ts_odo1, yawrate1, 'k', color='black', label='yawrate right turn')
    plt.plot(ts_odo1, yawrate1, 'x', color='black')
    plt.plot(ts_gyro1, vector_gyro1[:, 2], 'k', color='g', label='z gyro right turn')
    plt.ylabel('yawrate [rad/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    #calculating rotation from yawrate
    odo_rotation = np.zeros(ts_odo.__len__())
    for i in range(ts_odo.__len__()):
        if(i > 0):
            odo_rotation[i] = (odo_rotation[i-1]+(yawrate[i]*(ts_odo[i]-ts_odo[i-1])))
    odo_rotation1 = np.zeros(ts_odo1.__len__())
    for i in range(ts_odo1.__len__()):
        if(i > 0):
            odo_rotation1[i] = (odo_rotation1[i-1]+(yawrate1[i]*(ts_odo1[i]-ts_odo1[i-1])))
    ax2 = fig.add_subplot(gs[1, 0])
    #calculating distance from acceleration data
    rotation_from_gyro = np.zeros(vector_gyro.__len__())
    rotation_from_gyro[0] = vector_gyro[0, 2]
    rotation_from_gyro1 = np.zeros(vector_gyro1.__len__())
    rotation_from_gyro1[0] = vector_gyro1[0, 2]
    for i in range(vector_gyro.__len__()):
        if(i > 0):
            rotation_from_gyro[i] = ((rotation_from_gyro[i-1])+(vector_gyro[i, 2]*(ts_gyro[i]-ts_gyro[i-1])))

    for i in range(vector_gyro1.__len__()):
        if(i > 0):
            rotation_from_gyro1[i] = ((rotation_from_gyro1[i-1])+(vector_gyro1[i, 2]*(ts_gyro1[i]-ts_gyro1[i-1])))

    plt.plot(ts_odo, odo_rotation, 'k', color='black', label='odometry left turn')
    plt.plot(ts_odo, odo_rotation, 'x', color='black')
    plt.plot(ts_gyro, rotation_from_gyro, 'k', color='b', label='smartphone left turn')

    plt.plot(ts_odo1, odo_rotation1, 'k', color='black', label='odometry right turn')
    plt.plot(ts_odo1, odo_rotation1, 'x', color='black')
    plt.plot(ts_gyro1, rotation_from_gyro1, 'k', color='g', label='smartphone right turn')
    plt.ylabel('rotation [degree]')
    plt.xlabel('time [s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


def rotation_algorithm():
    #odo
    ts_odo_static, velocity_static, yawrate_static = dc.read_odo_from_csv(dc.static + "odoLog" + dc.ts_static + ".csv")
    ts_odo_static -= ts_odo_static[0]
    ts_odo_static /= 1000
    ts_odo_forward, velocity_forward, yawrate_forward = dc.read_odo_from_csv(dc.forward + "odoLog" + dc.ts_forward + ".csv")
    ts_odo_forward -= ts_odo_forward[0]
    ts_odo_forward /= 1000
    ts_odo_backward, velocity_backward, yawrate_backward = dc.read_odo_from_csv(dc.backward + "odoLog" + dc.ts_backward + ".csv")
    ts_odo_backward -= ts_odo_backward[0]
    ts_odo_backward /= 1000
    ts_odo_left, velocity_left, yawrate_left = dc.read_odo_from_csv(dc.left + "odoLog" + dc.ts_left + ".csv")
    ts_odo_left -= ts_odo_left[0]
    ts_odo_left /= 1000
    ts_odo_right, velocity_right, yawrate_right = dc.read_odo_from_csv(dc.right + "odoLog" + dc.ts_right + ".csv")
    ts_odo_right -= ts_odo_right[0]
    ts_odo_right /= 1000
    ts_odo_closed_loop, velocity_closed_loop, yawrate_closed_loop = dc.read_odo_from_csv(dc.closed_loop + "odoLog" + dc.ts_closed_loop + ".csv")
    ts_odo_closed_loop -= ts_odo_closed_loop[0]
    ts_odo_closed_loop /= 1000

    #smartphone
    ts_gyro_static, vector_gyro_static = dc.read_vectors_from_csv(dc.static + "gyroscopeLog" + dc.ts_static + ".csv")
    ts_gyro_static -= ts_gyro_static[0]
    ts_gyro_static /= 1000000000
    ts_gyro_forward, vector_gyro_forward = dc.read_vectors_from_csv(dc.forward + "gyroscopeLog" + dc.ts_forward + ".csv")
    ts_gyro_forward -= ts_gyro_forward[0]
    ts_gyro_forward /= 1000000000
    ts_gyro_backward, vector_gyro_backward = dc.read_vectors_from_csv(dc.backward + "gyroscopeLog" + dc.ts_backward + ".csv")
    ts_gyro_backward -= ts_gyro_backward[0]
    ts_gyro_backward /= 1000000000
    ts_gyro_left, vector_gyro_left = dc.read_vectors_from_csv(dc.left + "gyroscopeLog" + dc.ts_left + ".csv")
    ts_gyro_left -= ts_gyro_left[0]
    ts_gyro_left /= 1000000000
    ts_gyro_right, vector_gyro_right = dc.read_vectors_from_csv(dc.right + "gyroscopeLog" + dc.ts_right + ".csv")
    ts_gyro_right -= ts_gyro_right[0]
    ts_gyro_right /= 1000000000
    ts_gyro_closed_loop, vector_gyro_closed_loop = dc.read_vectors_from_csv(dc.closed_loop + "gyroscopeLog" + dc.ts_closed_loop + ".csv")
    ts_gyro_closed_loop -= ts_gyro_closed_loop[0]
    ts_gyro_closed_loop /= 1000000000


    #convert gyro yawrate to degree/s
    #yawrate *= (2*np.pi/360)
    vector_gyro_static[:, 2] *= -(360/(2*np.pi))
    vector_gyro_forward[:, 2] *= -(360/(2*np.pi))
    vector_gyro_backward[:, 2] *= -(360/(2*np.pi))
    vector_gyro_left[:, 2] *= -(360/(2*np.pi))
    vector_gyro_right[:, 2] *= -(360/(2*np.pi))
    vector_gyro_closed_loop[:, 2] *= -(360/(2*np.pi))
    #print(2*np.pi/360)

    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(1, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    #plt.plot(ts_odo_static, yawrate_static, 'k', color='black', label='odo static')
    #plt.plot(ts_gyro_static, vector_gyro_static[:, 2], 'x', color='b', label='gyro static')

    plt.plot(ts_odo_forward, yawrate_forward, 'x', color='black', label='straight odometry')
    plt.plot(ts_odo_forward, yawrate_forward, 'k', color='black')
    plt.plot(ts_gyro_forward, vector_gyro_forward[:, 2], 'k', color='black', label='straight')

    #plt.plot(ts_odo_backward, yawrate_backward, 'k', color='black', label='odo backwards')
    #plt.plot(ts_gyro_backward, vector_gyro_backward[:, 2], 'x', color='b', label='gyro backwards')

    plt.plot(ts_odo_left, yawrate_left, 'x', color='b', label='left odometry')
    plt.plot(ts_odo_left, yawrate_left, 'k', color='b')
    plt.plot(ts_gyro_left, vector_gyro_left[:, 2], 'k', color='b', label='left turn')

    plt.plot(ts_odo_right, yawrate_right, 'x', color='green', label='right odometry')
    plt.plot(ts_odo_right, yawrate_right, 'k', color='green')
    plt.plot(ts_gyro_right, vector_gyro_right[:, 2], 'k', color='green', label='right turn')

    #plt.plot(ts_odo_closed_loop, yawrate_closed_loop, 'k', color='black', label='odo closed loop')
    #plt.plot(ts_gyro_closed_loop, vector_gyro_closed_loop[:, 2], 'k', color='b', label='gyro closed loop')

    plt.ylabel('yawrate [degree/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    #calculating rotation from yawrate
    # odo_rotation = np.zeros(ts_odo_static.__len__())
    # for i in range(ts_odo_static.__len__()):
    #     if(i > 0):
    #         odo_rotation[i] = (odo_rotation[i-1]+(yawrate_static[i]*(ts_odo_static[i]-ts_odo_static[i-1])))
    # odo_rotation1 = np.zeros(ts_odo_forward.__len__())
    # for i in range(ts_odo_forward.__len__()):
    #     if(i > 0):
    #         odo_rotation1[i] = (odo_rotation1[i-1]+(yawrate_forward[i]*(ts_odo_forward[i]-ts_odo_forward[i-1])))
    #
    # #calculating rotation from gyro data
    # rotation_from_gyro = np.zeros(vector_gyro_static.__len__())
    # rotation_from_gyro[0] = vector_gyro_static[0, 2]
    # rotation_from_gyro1 = np.zeros(vector_gyro_forward.__len__())
    # rotation_from_gyro1[0] = vector_gyro_forward[0, 2]
    # for i in range(vector_gyro_static.__len__()):
    #     if(i > 0):
    #         rotation_from_gyro[i] = ((rotation_from_gyro[i-1])+(vector_gyro_static[i, 2]*(ts_gyro_static[i]-ts_gyro_static[i-1])))
    #
    # for i in range(vector_gyro_forward.__len__()):
    #     if(i > 0):
    #         rotation_from_gyro1[i] = ((rotation_from_gyro1[i-1])+(vector_gyro_forward[i, 2]*(ts_gyro_forward[i]-ts_gyro_forward[i-1])))
   # ax2 = fig.add_subplot(gs[1, 0])
    # plt.plot(ts_odo_static, odo_rotation, 'k', color='black', label='odometry left turn')
    # plt.plot(ts_odo_static, odo_rotation, 'x', color='black')
    # plt.plot(ts_gyro_static, rotation_from_gyro, 'k', color='b', label='smartphone left turn')
    #
    # plt.plot(ts_odo_forward, odo_rotation1, 'k', color='black', label='odometry right turn')
    # plt.plot(ts_odo_forward, odo_rotation1, 'x', color='black')
    # plt.plot(ts_gyro_forward, rotation_from_gyro1, 'k', color='g', label='smartphone right turn')
    # plt.ylabel('rotation [degree]')
    # plt.xlabel('time [s]')
    # plt.tight_layout()
    # plt.legend()
    # plt.grid()
    plt.show()


def calc_ts_offset(folder_name, timestamp):
    #odo
    ts_odo, velocity_from_odo, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo *= 1000000
    #smartphone
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_lin_accel, vector_lin_accel = dc.read_vectors_from_csv(folder_name + "linearAccelerationLog" + timestamp + ".csv")
    #ts_accel -= ts_accel[0]
    #ts_accel /= 1000000000
    #ts_lin_accel -= ts_lin_accel[0]
    #ts_lin_accel /= 1000000000
    print('first_ts_accel:')
    print ts_accel[0]
    print('first_ts_odo')
    print(ts_odo[0])
    print('ts_diff_nano')
    print(ts_accel[0]-ts_odo[0])
    print('ts_diff_milli')
    print((ts_accel[0]-ts_odo[0])/1000000)


def accel_correction_window_sizes(folder_name, timestamp):#odo
    ts_odo, velocity, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    #ts_odo /= 1000
    ts_mag, vector_mag = dc.read_vectors_from_csv(folder_name + "magneticFieldLog" + timestamp + ".csv")
    ts_mag -= ts_mag[0]
    ts_mag /= 1000000
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000
    velocity_from_accel = np.zeros(vector_accel.__len__())
    velocity_from_accel[0] = vector_accel[0, 1]
    for i in range(vector_accel.__len__()):
        if(i > 0):
            velocity_from_accel[i] = ((velocity_from_accel[i-1])+(vector_accel[i, 1]*(ts_accel[i]-ts_accel[i-1])))
    fig = plt.figure(figsize=(12.8, 7.2))
    gs = gridspec.GridSpec(2, 1)
    ax2 = fig.add_subplot(gs[0, 0])

    plt.ylabel('magnetic field [micro tesla]')
    plt.xlabel('time [s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    plt.show()


def mean_ts_diffs():
    diffs_tuple = (82875534.1499, 82876067.3144, 82875625.0606, 82875796.053, 82875486.9076, 82875918.5208, 82875794.8022, 82875974.6194)
    print type(diffs_tuple)
    diffs = np.array(diffs_tuple)
    print diffs
    print diffs.mean()


def accel_means():
    mean_names = ('Static', 'Forward', 'Backward', 'Left Turn', 'Right Turn', 'Closed Loop')
    diffs_tuple = (-0.0736007801508, -0.080294913216, -0.0978803954004, -0.106039402467, -0.053761334518, -0.0702029308243)
    fig = plt.figure(figsize=(16.0, 16.0))
    gs = gridspec.GridSpec(1, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    ind = np.arange(6)  # the x locations for the groups
    width = 1      # the width of the bars
    ax2.bar(ind + width, diffs_tuple, color='blue', align='center')
    #ax2.bar(8, np.mean(diffs_tuple), color='green', align='center')
    # add some text for labels, title and axes ticks
    ax2.set_ylabel('Drift Correction Factors [m/s^2]')
    ax2.set_title('Variance in Drifts')
    #ax2.set_xticks(ind + width)
    ax2.set_xticklabels(('', 'Static', 'Forward', 'Backward', 'Left Turn', 'Right Turn', 'Closed Loop'))
    plt.axhline(np.mean(diffs_tuple), color='green')
    plt.grid()
    plt.show()


def show_accel_correction_step(case):
    folder_name, timestamp, title = dc.get_case_data(case)
    #odo
    ts_odo, velocity_from_odo, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    ts_mag, vector_mag = dc.read_vectors_from_csv(folder_name + "magneticFieldLog" + timestamp + ".csv")
    ts_mag -= ts_mag[0]
    ts_mag /= 1000000000
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000000
    #norm_accel = np.sqrt(np.power(vector_accel[:, 0], 2)+np.power(vector_accel[:, 1], 2)+np.power(vector_accel[:, 2], 2))
    #calculating velocity from linear acceleration data
    velocity_from_accel = np.zeros(vector_accel.__len__())
    velocity_from_accel[0] = vector_accel[0, 1]
    for i in range(vector_accel.__len__()):
        if i > 0:
            velocity_from_accel[i] = ((velocity_from_accel[i-1])+(vector_accel[i, 1]*(ts_accel[i]-ts_accel[i-1])))
    correction_factor = vector_accel[0:100, 1].mean()
    velocity_from_accel_corrected = np.zeros(vector_accel.__len__())
    for i in range(vector_accel.__len__()):
        if i > 0:
            velocity_from_accel_corrected[i] = ((velocity_from_accel_corrected[i-1])+((vector_accel[i, 1]-correction_factor)*(ts_accel[i]-ts_accel[i-1])))
    print correction_factor
    fig = plt.figure(figsize=(12.8, 7.2))
    gs = gridspec.GridSpec(3, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    plt.title(title)
    plt.plot(ts_accel[100], velocity_from_accel[100], 'x', color='black')
    plt.plot(ts_accel, velocity_from_accel, 'k', color='b', label='smartphone')
    plt.plot(ts_accel, velocity_from_accel_corrected, 'k', color='green', label='smartphone corrected')
    plt.plot(ts_odo, velocity_from_odo, 'k', color='black', label='odometry')
    plt.plot(ts_odo, velocity_from_odo, 'x', color='black')
    plt.ylabel('velocity [m/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax3 = fig.add_subplot(gs[1, 0])
    norm_2 = np.linalg.norm(vector_mag, ord=2, axis=1)
    norm_1 = np.linalg.norm(vector_mag, ord=1, axis=1)
    mean_cumulative = np.zeros(ts_mag.__len__())
    diff = np.zeros(ts_mag.__len__())
    for i in range(ts_mag.__len__()):
        if i > 0:
            mean_cumulative[i] = norm_1[0:i].mean()
            diff[i] = (mean_cumulative[i]-norm_1[i])
    #np.sqrt(np.power(vector_mag[:, 0], 2)+np.power(vector_mag[:, 1], 2)+np.power(vector_mag[:, 2], 2))

    plt.plot(ts_mag, vector_mag[:, 0], 'k', color='black', label='x')
    plt.plot(ts_mag, vector_mag[:, 1], 'k', color='black', label='y')
    plt.plot(ts_mag, vector_mag[:, 2], 'k', color='black', label='z')

    #plt.plot(ts_mag, mean_cumulative, 'k', color='r', label='norm0')
    plt.plot(ts_mag, norm_1, 'k', color='g', label='1 norm')
    plt.plot(ts_mag, norm_2, 'k', color='b', label='2 norm')
    plt.ylabel('magnetic field [micro tesla]')
    plt.xlabel('time [s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    #calculating mag diffs to get more inside in mag data
    vector_mag_diffs = np.zeros((4, vector_mag.__len__()))
    #print np.size(vector_mag_diffs)
    #print np.size(vector_mag)
    for i in range(ts_mag.__len__()):
        if i > 70:
            if np.abs(np.max(norm_1[i-70:i])-np.min(norm_1[i-70:i])) > 3.5:
                vector_mag_diffs[0, i] = 30
            else:
                vector_mag_diffs[0, i] = 0
    ax4 = fig.add_subplot(gs[2, 0])
    plt.plot(ts_mag, vector_mag_diffs[0, :], 'k', color='r', label='detected vehicle state')
    plt.plot(ts_mag[70], vector_mag_diffs[0, 70], 'x', color='black')
    #plt.plot(ts_mag, vector_mag_diffs[1, :], 'k', color='g', label='mag_diff y')
    #plt.plot(ts_mag, vector_mag_diffs[2, :], 'k', color='b', label='mag_diff z')
    #plt.plot(ts_mag, vector_mag_diffs[3, :], 'k', color='black', label='mag_diff norm')
    plt.plot(ts_mag, diff, 'k', color='black', label='1 norm diff')
    plt.tight_layout()
    ##plt.legend()
    plt.grid()
    plt.show()


def show_accel_treshhold(case):
    folder_name, timestamp, title = dc.get_case_data(case)
    #odo
    ts_odo, velocity_from_odo, yawrate = dc.read_odo_from_csv(folder_name + "odoLog" + timestamp + ".csv")
    ts_odo -= ts_odo[0]
    ts_odo /= 1000
    ts_mag, vector_mag = dc.read_vectors_from_csv(folder_name + "magneticFieldLog" + timestamp + ".csv")
    ts_mag -= ts_mag[0]
    ts_mag /= 1000000000
    ts_accel, vector_accel = dc.read_vectors_from_csv(folder_name + "accelLog" + timestamp + ".csv")
    ts_accel -= ts_accel[0]
    ts_accel /= 1000000000
    ### calculations
    length = ts_accel.__len__()
    norm_2 = np.linalg.norm(vector_accel, ord=2, axis=1)
    norm_1 = np.linalg.norm(vector_accel, ord=1, axis=1)
    lpf40 = np.zeros(length)
    diff = np.zeros(length)
    #apply correction
    correction_factor = vector_accel[0:100, 1].mean()
    vector_accel[:,1] -= correction_factor
    for i in range(length):
        if i > 5:
            lpf40[i] = vector_accel[i-5:i, 1].mean()
            diff[i] = (lpf40[i]-norm_1[i])
    treshhold = np.zeros(length)
    velocity_from_threshhold = np.zeros(length)
    #treshhold
    windowsize = 400
    for i in range(length):
        if i > windowsize:
            if np.abs(np.abs(np.max(vector_accel[i-windowsize:i, 1]))+np.abs(np.min(vector_accel[i-windowsize:i, 1]))) > 1.4:
                treshhold[i-windowsize:i] = 3
    # for i in reversed(xrange(length)):
    #     if i < length-windowsize:
    #         if np.abs(np.abs(np.max(vector_accel[i:i+windowsize, 1]))+np.abs(np.min(vector_accel[i:i+windowsize, 1]))) >= 1.4:
    #             treshhold[i:i+10] = 3
    #velocity
    for i in xrange(length):
        if i > 0:
            if treshhold[i] == 3:
                velocity_from_threshhold[i] = (velocity_from_threshhold[i-1]+(vector_accel[i, 1]*(ts_accel[i]-ts_accel[i-1])))
            else:
                velocity_from_threshhold[i] = velocity_from_threshhold[i-1]
    velocity_from_threshhold[velocity_from_threshhold < 0] = 0

    ### plotting
    fig = plt.figure(figsize=(12.8, 7.2))
    gs = gridspec.GridSpec(3, 1)
    ax2 = fig.add_subplot(gs[0, 0])
    plt.title(title)
    plt.plot(ts_odo, velocity_from_odo, 'k', color='black', label='odometry')
    plt.plot(ts_odo, velocity_from_odo, 'x', color='black')
    plt.plot(ts_accel, velocity_from_threshhold, 'k', color='green', label='velo')
    plt.ylabel('velocity [m/s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax3 = fig.add_subplot(gs[1, 0])
    # plt.plot(ts_accel, vector_accel[:, 0], 'k', color='black', label='x')
    plt.plot(ts_accel, vector_accel[:, 1], 'k', color='black', label='y')
    # plt.plot(ts_accel, vector_accel[:, 2], 'k', color='black', label='z')
    plt.plot(ts_accel, lpf40, 'k', color='green', label='lpf40')
    #plt.plot(ts_mag, mean_cumulative, 'k', color='r', label='norm0')
    plt.plot(ts_accel, norm_1, 'k', color='g', label='1 norm')
    plt.plot(ts_accel, norm_2, 'k', color='b', label='2 norm')
    plt.ylabel('acceleration [m/s^2]')
    plt.xlabel('time [s]')
    plt.tight_layout()
    plt.legend()
    plt.grid()
    ax4 = fig.add_subplot(gs[2, 0])
    plt.plot(ts_accel, treshhold, 'k', color='r', label='detected vehicle state')
    plt.plot(ts_accel, velocity_from_threshhold, 'k', color='green', label='detected vehicle state')
    plt.plot(ts_accel, diff, 'k', color='black', label='1 norm diff')
    plt.tight_layout()
    # plt.legend()
    plt.grid()
    plt.show()


plot_test_drive(dc.Case.closed_loop)

