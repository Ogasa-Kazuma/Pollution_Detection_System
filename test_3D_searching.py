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

########################
##抽象クラスを使う
##数値の意味が分かりやすいようにもっと変数使う
##描画用の関数をもっと使いやすくする
##
##
##






########################### Global Variables ################################
field_x_length = 50
field_y_length = 50
noise_search_deepness = 15
noise_threshold = 0.3
#ノイズ閾値
#ノイズ最高値
#ノイズ最小値
#ノイズ発生確率
#探索深さ
#探索方向
#汚染源決定閾値




##########################################################################






def main():

    adjust_pol_upper = 100
    adjust_pol_lower = 0

    field_size_3D = 40
    search_deepness = 30

    num_auto_created_pol = 5
    auto_pol_max = 100

    pollution_state_3D = Pollution_State_3D_lib.Pollution_State_3D(field_size_3D)
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
    #search_deepnessの値が大きすぎると、ライブラリの方でlist out of rangeになる。直す
    max_pos_poll_list  = search_methods_3D.Detect_Square_Area_Max(pollution_list, 0, 0, 0, search_deepness, noise_threshold)


    pollution_state_3D.draw_pollution_map()


    # search_methods_3D.Detect_Max(pollution_list, 1, 1, 1, 45, 45, 50)

    start_position_list = list()
    start_position_list.append(0)
    start_position_list.append(30)
    start_position_list.append(0)

    rotate_direction = True
    searching_scope_radius = 20
    searching_start_angle = -45
    searching_end_angle = -30


    last_max_list = list()
    last_max_list.append(0)
    last_max_list.append(0)
    last_max_list.append(0)
    last_max_list.append(0)

    searching_range = 30 #探索開始点からの最大探索距離。この範囲を超えると探索打ち切り
    searching_length_now = 0




    while(True):
        moving_angle, no_use_data = search_methods_3D.Calculate_Degree(last_max_list, max_pos_poll_list)

        while(searching_length_now <= searching_range):

            now_pos_poll_list = search_methods_3D.Search_Pollution_On_Arc(pollution_list, max_pos_poll_list, True, searching_length_now, moving_angle - 90, moving_angle + 90)
            if(max_pos_poll_list[3] < now_pos_poll_list[3]):
                searching_length_now = 0
                last_max_list = max_pos_poll_list
                max_pos_poll_list = now_pos_poll_list
                isUpdated = True
                break

            if(searching_length_now < 5):
                searching_length_now += 1
            else:
                searching_length_now = searching_length_now + searching_range / 5

            if(searching_range < searching_length_now):
                break

        if(searching_range < searching_length_now):
            break






if __name__ == "__main__":
    main()
