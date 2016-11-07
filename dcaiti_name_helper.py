import pandas as pd
import numpy as np
from enum import Enum

#define log file names for easier handling
static = 'logs/dcaiti_sensor_project/1448469804269_static/'
ts_static = '1448469804269'

forward = 'logs/dcaiti_sensor_project/1448470183909_forward/'
ts_forward = '1448470183909'

backward = 'logs/dcaiti_sensor_project/1448470221828_backwards/'
ts_backward = '1448470221828'

left = 'logs/dcaiti_sensor_project/1448470461047_left_turn/'
ts_left = '1448470461047'

right = 'logs/dcaiti_sensor_project/1448470522564_right_turn/'
ts_right = '1448470522564'

closed_loop = 'logs/dcaiti_sensor_project/1448470602786_fast_closed_loop/'
ts_closed_loop = '1448470602786'


class Approach(Enum):
    naive = 1
    corrected = 2
    mag_tresh = 3
    acc_tresh = 4
    odometry = 5

    @classmethod
    def tostring(cls, val):
        if (val == cls.naive):
          return "Naive Integration"
        elif (val == cls.corrected):
          return "Drift Corrected"
        elif (val == cls.mag_tresh):
          return "Magnetic Threshold"
        elif (val == cls.acc_tresh):
            return "Acceleration Threshold Integration"
        elif (val == cls.odometry):
            return "Odometry"
        else:
          return None


class Case(Enum):
    static = 1
    forward = 2
    backward = 3
    left_turn = 4
    right_turn = 5
    closed_loop = 6


def get_case_data(case):
    if case is Case.static:
        return static, ts_static, 'Static'
    elif case is Case.forward:
        return forward, ts_forward, 'Forward'
    elif case is Case.backward:
        return backward, ts_backward, 'Backward'
    elif case is Case.left_turn:
        return left, ts_left, 'Left Turn'
    elif case is Case.right_turn:
        return right, ts_right, 'Right Turn'
    else:
        return closed_loop, ts_closed_loop, 'Closed Loop'


def read_odo_from_csv(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    return array[:, 0], array[:, 1], array[:, 2]


def read_vectors_from_csv(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    return array[:, 0], array[:, 1:4]


def read_quads_from_csv(filename):
    data = pd.read_csv(filename)
    array = np.array(data)
    return array[:, 0], array[:, 1:5]