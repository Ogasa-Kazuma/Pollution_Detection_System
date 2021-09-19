############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
from abc import ABCMeta, abstractmethod

import common

import class_pollution_state_drawer
from class_pollution_state_drawer import Pollution_State_Drawer
import importlib
importlib.reload(class_pollution_state_drawer)
importlib.reload(common)
############################################################################

class Pollution_State_Drawer_2D(Pollution_State_Drawer):

    def __init__(self, figure_object, drawing_area):

        self.__figure_object = figure_object.add_subplot(drawing_area)


    def draw_pollution_map(self, pollutions):

        pollutions_converted_to_array = np.array(pollutions)
        x_element_count, y_element_count = pollutions_converted_to_array.shape

        new_x = []
        new_y = []
        new_pollutions = []

        for x_count in range(x_element_count):
            for y_count in range(y_element_count):
                new_x.append(x_count)
                new_y.append(y_count)
                new_pollutions.append(pollutions[x_count][y_count])


        sc = self.__figure_object.scatter(new_x, new_y, c = new_pollutions, cmap='gray_r', linewidth = 0)












def main():



    fig = plt.figure()
    fig2 = plt.figure()
    pollution_state_drawer_2D = Pollution_State_Drawer_2D(fig, 131)
    pollution_state_drawer_2D_2 = Pollution_State_Drawer_2D(fig, 132)

    pollutions =  [[l for l in range(40)] for k in range(40)]
    for x_count in range(40):
        for y_count in range(40):
                pollutions[x_count][y_count] = 0.01 * x_count

    pollution_state_drawer_2D.draw_pollution_map(pollutions)
    pollution_state_drawer_2D_2.draw_pollution_map(pollutions)


if __name__ == "__main__":
    main()
