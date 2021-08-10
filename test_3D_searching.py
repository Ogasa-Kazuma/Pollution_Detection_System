############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections

import Pollution_State_3D_lib
import Pollution_State_2D_lib
import Pollution_Search_2D
import Pollution_Search_3D

import importlib
importlib.reload(Pollution_Search_2D)
importlib.reload(Pollution_Search_3D)
importlib.reload(Pollution_State_2D_lib)
importlib.reload(Pollution_State_3D_lib)
############################################################################



def main():

    adjust_pol_upper = 100
    adjust_pol_lower = 0

    field_size_3D = 40
    search_deepness = 30

    num_auto_created_pol = 5
    auto_pol_max = 100

    pollution_state_2D.Pollution_State_3D_lib.pollution_state_3D(field_size_3D)
    search_methods_3D = Pollution_Search_3D.Search_Methods_3D(search_deepness)


    pollution_state_3D.Auto_Pollutions_Create(num_auto_created_pol, auto_pol_max)

    pollution_state_3D.Adjust_Pollution(adjust_pol_upper, adjust_pol_lower)
#    pollution_state_3D.create_random_pollution(15, 0, 0, 0, 50, 50, 50, 100, 1)
    no_noise_x_max, no_noise_y_max, no_noise_z_max, max_pollution = pollution_state_3D.get_no_noise_max_pollution_point()
    print("no_noise_x_max = " + str(no_noise_x_max))
    print("no_noise_y_max = " + str(no_noise_y_max))
    print("no_noise_z_max = " + str(no_noise_z_max))
    print("max_pollution = " + str(max_pollution))

    pollution_list = pollution_state_3D.get_all_pollution_states()
    x,y,z,pollute = Detect_Square_Area_Max(pollution_list, 0, 0, 0, 100)
    print("square_area_max_x = " + str(x))
    print("square_area_max_y = " + str(y))
    print("square_area_max_z = " + str(z))
    print("square_area_max_pollution = " + str(pollute))

    Detect_Max(pollution_list, 1, 1, 1, 45, 45, 50)

    start_position_list = list()
    start_position_list.append(0)
    start_position_list.append(30)
    start_position_list.append(0)

    Search_Pollution_On_Arc(pollution_list, start_position_list,1, 20, -45, -30)

    pollution_state_3D.draw_pollution_map()

    Calculate_Degree(0, 0, 0, 10, 10, 14.141414)




if __name__ == "__main__":
    main()
