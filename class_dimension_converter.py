

############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
from abc import ABCMeta, abstractmethod


import importlib
############################################################################

class Dimension_Converter:

    def __init__(self, pollutions_3D):
        self.__pollutions_3D = pollutions_3D
        self.__upper_limit_3D = 0
        self.__upper_limit_3D = 0
        self.__upper_limit_3D = 0
        self.__upper_limit_3D = 0

    def Convert_Dimension(self, z_point_to_delete, upper_limit_3D, lower_limit_3D, upper_limit_2D, lower_limit_2D):

        range_of_concentration_3D = upper_limit_3D - lower_limit_3D
        range_of_concentration_2D = upper_limit_2D - lower_limit_2D

        # $$$$$$$$$$$$$$$$$$
        concentration_range_ratio = range_of_concentration_2D / range_of_concentration_3D

        #TODO 変数名を直す
        pollutions_converted_to_array = np.array(self.__pollutions_3D)
        x_limit, y_limit, no_used = pollutions_converted_to_array.shape

        #3次元から2次元への変換
        pollutions_2D = [[0.0 for j in range(y_limit)] for l in range(x_limit)]
        for x_count in range(x_limit):
            for y_count in range(y_limit):
                #濃度の範囲を変更
                pollutions_2D[x_count][y_count] = (self.__pollutions_3D[x_count][y_count][z_point_to_delete] - lower_limit_3D) * concentration_range_ratio + lower_limit_2D

        return pollutions_2D
