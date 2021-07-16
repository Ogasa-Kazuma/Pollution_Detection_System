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

import importlib
importlib.reload(Pollution_Search_2D)
importlib.reload(Pollution_State_2D_lib)
importlib.reload(Pollution_State_3D_lib)
############################################################################


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




##########################################################################3










################# Functions #############################################

def Distinguish_Noise_Pollution(use_list, x_center_point, y_center_point, z_center_point, measure_area_length, threshold):

    use_array = np.array(use_list)
    x_limit, y_limit, z_limit = use_array.shape

    sum = 0

    for x_count in range(x_center_point - measure_area_length, x_center_point + measure_area_length, 1):
        for y_count in range(y_center_point - measure_area_length, y_center_point + measure_area_length, 1):
            for z_count in range(z_center_point - measure_area_length, z_center_point + measure_area_length, 1):
                if((x_count < x_limit) and (y_count < y_limit) and (z_count < z_limit) and 0 <= x_count and 0 <= y_count and 0 <= z_count):
                    sum += use_list[x_count][y_count][z_count]
                else:
                    pass

    ave = sum / ((1 + 2 *(measure_area_length)) ** (2))

    return use_list[x_center_point][y_center_point][z_center_point] - ave > threshold



def Calculate_Degree(start_x_value , start_y_value , start_z_value, end_x_value , end_y_value, end_z_value):
    two_dimension_angle = 0
    two_dimension_angle = math.degrees(math.atan2((end_y_value - start_y_value) , (end_x_value - start_x_value)))
    two_dimension_length = math.sqrt((end_y_value - start_y_value) ** (2) + (end_x_value - start_x_value) ** (2))
    three_dimension_angle = math.degrees(math.atan2((end_z_value - start_z_value) , two_dimension_length))
    return two_dimension_angle, three_dimension_angle

def Calculate_Degree_2D(start_pos_poll_list, end_pos_poll_list):

    two_dimension_angle = math.degrees(math.atan2((end_pos_poll_list[1] - start_pos_poll_list[1]) , (end_pos_poll_list[0] - start_pos_poll_list[0])))

    return two_dimension_angle



###########################################################################
# Detect_Max
#
# 指定された線上の、濃度を計測し、最高濃度値とその座標を返す。
# ただし引数により求まる初期濃度値より高い濃度値を得られなければ、初期濃度値をそのまま返す
# 濃度値の更新があれば、その時点での値と座標を散布図にオレンジ色で表示する
# 関数を実行して求まった最高濃度の座標を散布図に緑色で表示する
#
#　戻り値(濃度最高点のx座標、y座標、そしてその濃度値)
# 濃度の最高値が、x_startとy_startの地点だった場合（つまり濃度値の初期値が最大値だった場合)、初期座標と初期濃度を返す
# 最初に渡された座標が、測定範囲外(フィールドサイズを超えてた場合)、初期座標と初期濃度を返す
# 初期濃度より高い濃度が更新された場合、その座標と濃度を返す
#
###########################################################################

def Detect_Max(pollution_list, x_start, y_start, z_start, xy_angle, xz_angle, search_deepness):

    print("--------------------------- Func Detect_Max -----------------------------------------")
    x_now = x_start
    y_now = y_start
    z_now = z_start
    start_density = pollution_list[x_start][y_start][z_start]

    print(start_density)
    near_x = 0
    near_y = 0
    near_z = 0

    #X_startやy_startを代入しているのは、引数で与えられた座標(つまり測定の初期座標)が測定不可域であった場合に
    #濃度の最大値の更新が行われていないので、戻り値として初期座標を返すためである
    x_max = x_start
    y_max = y_start
    z_max = z_start
    max_density = pollution_list[x_start][y_start][z_start]

    #pollution_listのx方向、y方向それぞれの要素数を取得する。探索不可域の設定に用いる(x_limit, y_limitの外側は探索できない)
    array_limit = np.array(pollution_list)
    x_limit, y_limit, z_limit = array_limit.shape
    print(array_limit.shape)

    first_vector_length = 1
    search_vector_length = first_vector_length

    #while(search_vector_length <= search_deepness):
    #x_now - x_startなどは、探索を行った深さを表す。その深さが決められた長さ(search_deepness)を超えない限り、探索ループは続く。
    while(abs(abs(x_now) - x_start) < search_deepness and abs(abs(y_now) - y_start) < search_deepness and abs(abs(z_now) - z_start) < search_deepness):
        #進行方向の座標計算
        #初期座標　+  初期座標からの x(もしくはy)座標の変化量
        near_x = x_start + search_vector_length * math.cos(math.radians(xy_angle))
        near_y = y_start + search_vector_length * math.sin(math.radians(xy_angle))
        near_z = z_start + search_vector_length * math.sin(math.radians(xz_angle))

        #座標値は小数なし（整数）なので、近傍のどのx,y座標が最も近いか比較し、最も近い値に座標値を設定する。
        #例えば8.6は、 7, 8, 9のなかで最も9に近いため、探索に用いる座標も9にする
        if(abs(x_now - near_x) < abs((x_now + 1) - near_x)):
            if(abs((x_now - 1) - near_x) < abs(x_now - near_x)):
                x_now = x_now - 1
            else:
                x_now = x_now
        else:
            x_now += 1

        if(abs(y_now - near_y) < abs((y_now + 1) - near_y)):
            if(abs((y_now - 1) - near_y) < abs(y_now - near_y)):
                y_now = y_now - 1
            else:
                y_now = y_now
        else:
            y_now += 1

        if(abs(z_now - near_z) < abs((z_now + 1) - near_z)):
            if(abs((z_now - 1) - near_z) < abs(z_now - near_z)):
                z_now = z_now - 1
            else:
                z_now = z_now
        else:
            z_now += 1


        #初めから、探索不可能領域にx座標、y座標の少なくともどちらかが入っていた場合、最高値は更新せず、引数で渡されたx,yと濃度値を返す
        if(x_limit <= x_now or y_limit <= y_now or z_limit <= z_now): # <= ではなく < にするとリストの容量を超える
            if(search_vector_length == first_vector_length):
                return x_start, y_start, z_start, start_density
            #初めから探索不可能領域に入っていた場合ではなく、探索を続けているうちに探索不可能領域に入った場合、その時点での最高濃度値とその座標を返す
            else:
                return x_max, y_max, z_max, max_density
            #引数で渡された初期座標が0より小さい場合（探索不可能）、その座標と、その座標での濃度値をそのまま返す。ただ、濃度リストにはマイナス座標での値は存在しないため、このifが実行される前にエラーとなる
        elif(x_now < 0 or y_now < 0 or z_now < 0):
                if(search_vector_length == first_vector_length):
                    return x_start, y_start, z_start, start_density
                #探索を続けるうちにx,y座標がマイナスになった場合は処理を終了し、その座標と、その地点での濃度値を返す
                else:
                    return x_max, y_max, z_max, max_density

        #濃度最高値を発見した場合の処理。その最高濃度値がノイズによるものかどうかをif-elseで判断
        if(max_density < pollution_list[x_now][y_now][z_now]):
            #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
            if(Distinguish_Noise_Pollution(pollution_list, x_now, y_now, z_now, noise_search_deepness, noise_threshold)):
                pass
            #新たな最高濃度がノイズによるものでないと判断した場合、座標と最高濃度値を更新
            else:

                max_density = pollution_list[x_now][y_now][z_now]
                x_max = x_now
                y_max = y_now
                z_max = z_now
                print("Func DM lapollution_state_2D max = " + str(max_density))
        #次に探索する場所は今より、1進んだ場所なので探索する長さを伸ばす
        search_vector_length += 1

    #この関数の実行を行った結果、見つかった最高濃度値の座標を散布図に緑色の点で表示する。
    #ただし、測定不可域に入り、関数の処理がreturnにより終了した場合は、最高濃度値・座標は散布図に表示されない。
    print("Func DM max_pollution = " + str(max_density))
    print("----------------------------------------------------------")
    return x_max, y_max, z_max, max_density







# def Detect_Square_Area_Max(pollution_list, x_now, y_now, z_now, search_deepness):
#
#
#     x_max = 0
#     y_max = 0
#     z_max = 0
#     max_value = 0
#
#
#
#
# ############## Function Update_Max #####################################
#     def Update_Max(pollution_list, x, y, z, noise_threshold):
#         nonlocal x_max
#         nonlocal y_max
#         nonlocal z_max
#         nonlocal max_value
#         if max_value < pollution_list[measure_x + x_1][measure_y + y_1][measure_z + z_1]:
#             if(Distinguish_Noise_Pollution(pollution_list, x, y, z, noise_search_deepness, noise_threshold)):
#                 pass
#             else:
#                 x_max = x
#                 y_max = y
#                 z_max = z
#                 max_value = pollution_list[x][y][z]
#
#         return x_max, y_max, z_max, max_value
#
#     x_now = abs(x_now)
#     y_now = abs(y_now)
#     z_now = abs(z_now)
#
#
#     measure_x = x_now - search_deepness / 2
#     measure_y = y_now - search_deepness / 2
#     measure_z = z_now - search_deepness / 2
#
#     #小数点以下切り捨て
#     measure_x = math.ceil(measure_x)
#     measure_y = math.ceil(measure_y)
#     measure_z = math.ceil(measure_z)
#
#
#
#     array_limit = np.array(pollution_list)
#     x_limit, y_limit, z_limit = array_limit.shape
#
#     print("z_limit = " + str(z_limit))
#
#     for x_1 in range(search_deepness):
#         for y_1 in range(search_deepness):
#             for z_1 in range(search_deepness):
#                 if(0 < (measure_x + x_1) and 0 < (measure_y + y_1) and 0 < (measure_z + z_1)):
#                     if((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
#                         Update_Max(pollution_list, measure_x + x_1, measure_y + y_1, measure_z + z_1, noise_threshold)
#                     elif((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and z_limit < (measure_z + z_1)):
#                         Update_Max(pollution_list, measure_x + x_1, measure_y + y_1, measure_z + z_1 - (measure_z + z_1 - z_limit),  noise_threshold)
#                     elif((measure_x + x_1) < x_limit and y_limit < (measure_y + y_1) and (measure_z + z_1) < z_limit):
#                         Update_Max(pollution_list, measure_x + x_1, measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1,  noise_threshold)
#                     elif((measure_x + x_1) < x_limit and y_limit < (measure_y + y_1) and z_limit < (measure_z + z_1)):
#                         Update_Max(pollution_list, measure_x + x_1, measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1 - (measure_z + z_1 - z_limit), nnoise_threshold)
#                     elif(x_limit < (measure_x + x_1) and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
#                         Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1, measure_z + z_1, noise_threshold)
#                     elif(x_limit < (measure_x + x_1) and (measure_y + y_1) < y_limit and z_limit < (measure_z + z_1)):
#                         Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1, measure_z + z_1 - (measure_z + z_1 - z_limit),  noise_threshold)
#                     elif(x_limit < (measure_x + x_1) and y_limit  < (measure_y + y_1)  and (measure_z + z_1) < z_limit):
#                         Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1,noise_threshold)
# #[measure_y + y_1 - (measure_y + y_1 - y_limit)]
#                     elif((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
#                         break
#
#                 else:
#                     pass
#
#     return x_max, y_max, z_max, max_value


def Search_Pollution_On_Arc(pollution_list, start_position_list, rotate_direction, radius, start_angle, end_angle):

    print("--------------------------- Func Search_Pollution_On_Arc -----------------------------------------")
    x_now = start_position_list[0]
    y_now = start_position_list[1]
    z_now = start_position_list[2]
    start_density = pollution_list[x_now][y_now][z_now]

    x_start = start_position_list[0]
    y_start = start_position_list[1]
    z_start = start_position_list[2]

    print(start_density)
    near_x = 0
    near_y = 0
    near_z = 0

    #X_startやy_startを代入しているのは、引数で与えられた座標(つまり測定の初期座標)が測定不可域であった場合に
    #濃度の最大値のstart_position_list[0]更新が行われていないので、戻り値として初期座標を返すためである
    x_max = start_position_list[0]
    y_max = start_position_list[1]
    z_max = start_position_list[2]
    max_density = pollution_list[x_max][y_max][z_max]

    max_list = list()
    max_list.append(x_max)
    max_list.append(y_max)
    max_list.append(z_max)
    max_list.append(max_density)



    #pollution_listのx方向、y方向それぞれの要素数を取得する。探索不可域の設定に用いる(x_limit, y_limitの外側は探索できない)
    array_limit = np.array(pollution_list)
    x_limit, y_limit, z_limit = array_limit.shape


    search_angle = start_angle
    angle_change_amount = 1

    #探索開始点と終了点の間の角度が0もしくは0に近いならば探索をしない
    if(math.floor(end_angle - start_angle) == 0):
        return

    #Trueなら時計周りに探索を進め、Falseなら反時計回り
    #rotate_direction = True if 0 < (end_angle - start_angle) else False


    while(start_angle <= search_angle and search_angle <= end_angle):


        #進行方向の座標計算
        #初期座標　+  初期座標からの x(もしくはy)座標の変化量
        near_x = x_start + radius * math.cos(math.radians(search_angle))
        near_y = y_start + radius * math.sin(math.radians(search_angle))



        if(abs(x_now - near_x) < abs((x_now + 1) - near_x)):
            if(abs((x_now - 1) - near_x) < abs(x_now - near_x)):
                x_now = x_now - 1
            else:
                x_now = x_now
        else:
            x_now += 1

        if(abs(y_now - near_y) < abs((y_now + 1) - near_y)):
            if(abs((y_now - 1) - near_y) < abs(y_now - near_y)):
                y_now = y_now - 1
            else:
                y_now = y_now
        else:
            y_now += 1

        if(x_now < 0 or x_limit < x_now or y_now < 0 or y_limit < y_now):
            pass
        else:
            if(max_list[3] < pollution_list[x_now][y_now][z_now]):
                print("in loop")
                max_list[0] = x_now
                max_list[1] = y_now
                max_list[2] = z_now
                max_list[3] = pollution_list[x_now][y_now][z_now]


        if(rotate_direction == True):
            search_angle = search_angle + angle_change_amount
        else:
            search_angle = search_angle - angle_change_amount



    print(max_list)


    return max_list





def Search_Pollution_On_Arc_2D(pollution_list, start_position_list, rotate_direction, radius, start_angle, end_angle):

    print("--------------------------- Func Search_Pollution_On_Arc -----------------------------------------")
    x_now = round(start_position_list[0] + radius * math.cos(math.radians(start_angle)))
    y_now = round(start_position_list[1] + radius * math.sin(math.radians(start_angle)))

    x_start = start_position_list[0]
    y_start = start_position_list[1]
    start_density = pollution_list[x_start][y_start]

    print(start_density)
    near_x = 0
    near_y = 0

    #X_startやy_startを代入しているのは、引数で与えられた座標(つまり測定の初期座標)が測定不可域であった場合に
    #濃度の最大値のstart_position_list[0]更新が行われていないので、戻り値として初期座標を返すためである
    x_max = start_position_list[0]
    y_max = start_position_list[1]
    max_density = pollution_list[x_max][y_max]

    max_list = list()
    max_list.append(x_max)
    max_list.append(y_max)
    max_list.append(max_density)



    #pollution_listのx方向、y方向それぞれの要素数を取得する。探索不可域の設定に用いる(x_limit, y_limitの外側は探索できない)
    array_limit = np.array(pollution_list)
    x_limit, y_limit = array_limit.shape


    search_angle = start_angle
    angle_change_amount = 1

    #探索開始点と終了点の間の角度が0もしくは0に近いならば探索をしない
    if(math.floor(end_angle - start_angle) == 0):
        return

    #Trueなら時計周りに探索を進め、Falseなら反時計回り
    #rotate_direction = True if 0 < (end_angle - start_angle) else False


    while(start_angle <= search_angle and search_angle <= end_angle):


        #進行方向の座標計算
        #初期座標　+  初期座標からの x(もしくはy)座標の変化量
        near_x = x_start + radius * math.cos(math.radians(search_angle))
        near_y = y_start + radius * math.sin(math.radians(search_angle))



        if(abs(x_now - near_x) < abs((x_now + 1) - near_x)):
            if(abs((x_now - 1) - near_x) < abs(x_now - near_x)):
                x_now = x_now - 1
            else:
                x_now = x_now
        else:
            x_now += 1

        if(abs(y_now - near_y) < abs((y_now + 1) - near_y)):
            if(abs((y_now - 1) - near_y) < abs(y_now - near_y)):
                y_now = y_now - 1
            else:
                y_now = y_now
        else:
            y_now += 1

        if(0 < x_now and x_now  <= x_limit and 0 < y_now and y_now <= y_limit):
            plt.scatter(x_now, y_now, c = 'orange', alpha = 0.1)

        if(x_now < 0 or x_limit <= x_now or y_now < 0 or y_limit <= y_now):
            pass
        else:
            if(max_list[2] < pollution_list[x_now][y_now]):
                print("in loop")
                max_list[0] = x_now
                max_list[1] = y_now
                max_list[2] = pollution_list[x_now][y_now]
                plt.scatter(x_now, y_now, c = "yellow")


        if(rotate_direction == True):
            search_angle = search_angle + angle_change_amount
        else:
            search_angle = search_angle - angle_change_amount



    print(max_list)
    plt.scatter(max_list[0], max_list[1], c = 'blue', alpha = 1)


    return max_list



def Circular_Survey(pollution_state_2D, searching_methods_2D):

    pollution_state_2D.Auto_Pollutions_Create(15, 0.5)

    pollution_state_2D.Adjust_Pollution(1, 0.5, 0)
    no_noise_x_max, no_noise_y_max, no_noise_max_pollution = pollution_state_2D.get_no_noise_max_pollution_point()

    no_noise_pos_poll_list = list()
    no_noise_pos_poll_list.append(no_noise_x_max)
    no_noise_pos_poll_list.append(no_noise_y_max)
    no_noise_pos_poll_list.append(no_noise_max_pollution)


    print(no_noise_max_pollution)
    pollution_state_2D.draw_pollution_map(2,2,1)

    plt.scatter(no_noise_x_max, no_noise_y_max, c = 'red', alpha = no_noise_max_pollution)

    pollution_state_2D.draw_pollution_map(2,2,2)

    pollution_list = pollution_state_2D.get_all_pollution_states()
    pollution_list = tuple(pollution_list)

    search_deepness = 10
    x_start = 25
    y_start = 25
    x_max = 0
    y_max = 0

    max_pollution_density = 0


    start_pos_poll_list = list()
    start_pos_poll_list.append(x_start)
    start_pos_poll_list.append(y_start)
    start_pos_poll_list.append(max_pollution_density)

    last_max_list = start_pos_poll_list
    
    plt.scatter(x_start, y_start, c = 'aqua')

    searching_range = 30 #探索開始点からの最大探索距離。この範囲を超えると探索打ち切り
    searching_length_now = 0

    max_pos_poll_list = searching_methods_2D.Detect_Square_Area_Max(pollution_list, start_pos_poll_list, search_deepness)

    while(True):
        moving_angle = Calculate_Degree_2D(last_max_list, max_pos_poll_list)

        while(searching_length_now <= searching_range):
            now_pos_poll_list = Search_Pollution_On_Arc_2D(pollution_list, max_pos_poll_list, True, searching_length_now, moving_angle - 90, moving_angle + 90)
            if(max_pos_poll_list[2] < now_pos_poll_list[2]):
                searching_length_now = 0
                last_max_list = max_pos_poll_list
                max_pos_poll_list = now_pos_poll_list
                plt.scatter(now_pos_poll_list[0], now_pos_poll_list[1], c = "green", alpha = 1)
                break

            if(searching_length_now < 5):
                searching_length_now += 1
            else:
                searching_length_now = searching_length_now + searching_range / 5

            if(searching_range < searching_length_now):
                return max_pos_poll_list, no_noise_pos_poll_list






######################################################
## Func Execute_2D_Search
##
##
##
##
########################################################3
def Execute_2D_Search():

    pollution_state_2D = Pollution_State_2D_lib.Pollution_State_2D(20,50)
    searching_methods_2D = Pollution_Search_2D.Search_Methods_2D(30)


    max_list, no_noise_pos_poll_list = Circular_Survey(pollution_state_2D, searching_methods_2D)





    # pollution_state_2D.Auto_Pollutions_Create(15, 0.5)
    #
    # pollution_state_2D.Adjust_Pollution(1, 0.5, 0)
    # no_noise_x_max, no_noise_y_max, no_noise_max_pollution = pollution_state_2D.get_no_noise_max_pollution_point()
    #
    # print(no_noise_max_pollution)
    # pollution_state_2D.draw_pollution_map(2,2,1)
    #
    # plt.scatter(no_noise_x_max, no_noise_y_max, c = 'red', alpha = no_noise_max_pollution)
    #
    # pollution_state_2D.draw_pollution_map(2,2,2)




    # pollution_list = pollution_state_2D.get_all_pollution_states()
    # pollution_list = tuple(pollution_list)



    # search_deepness = 20
    # x_start = 0
    # y_start = 0
    # x_max = 0
    # y_max = 0
    #
    # max_pollution_density = 0
    #
    #
    # position_list = list()
    # position_list.append(x_start)
    # position_list.append(y_start)
    #
    # max_list = list()
    # max_list = Search_Pollution_On_Arc_2D(pollution_list, position_list, True, 20, 10, 180)

    # Search_Pollution_On_Arc_2D(pollution_list, position_list, True, 40, 10, 180)
######################################################3
#     x_max, y_max, max_pollution_density = searching_methods_2D.Detect_Square_Area_Max(pollution_list, x_start, y_start,search_deepness)
#     plt.scatter(x_max, y_max, c = 'blue')
#     moving_angle = searching_methods_2D.Calculate_Degree(x_start, y_start, x_max, y_max)
#
#     #Search_Pollution(濃度リスト、基準方向、始点x座標、始点y座標、時計回り上限角度、反時計周り上限角度、角度ステップ、探索深さ)
#     x_max, y_max, max_pollution_density = searching_methods_2D.Detect_Pollution_Origin(pollution_list, x_max, y_max, 0, 0, 135, 135, 6, 15)
# #####################################################

    x_max, y_max, max_pollution_density = max_list[0], max_list[1], max_list[2]
    no_noise_x_max, no_noise_y_max, no_noise_max_pollution = no_noise_pos_poll_list[0],  no_noise_pos_poll_list[1], no_noise_pos_poll_list[2]

    print('真の濃度最高点 x座標  ' + str(no_noise_x_max))
    print('真の濃度最高点 y座標  ' + str(no_noise_y_max))
    print('真の濃度最高値  ' + str(no_noise_max_pollution))

    print('\n')
    print('final x_max = ' + str(x_max))
    print('final y_max = ' + str(y_max))
    print('final max_pollution_density = ' + str(max_pollution_density))

    plt.scatter(x_max, y_max, c = 'purple')

    searching_methods_2D.Calculate_Distance(x_max, y_max, no_noise_x_max, no_noise_y_max)


######################## main ###########################################
def main():

    Execute_2D_Search()
#     #Execute_3D_Search()
#
#
#     pollution_state_3D.Auto_Pollutions_Create(5, 100)
# #    pollution_state.create_local_pollution(10,10,10,5,100)
# #    pollution_state.create_local_pollution(10,10,40,5,100)
#     pollution_state_3D.Adjust_Pollution(100, 0)
#     pollution_state_3D.create_random_pollution(15, 0, 0, 0, 50, 50, 50, 100, 1)
#     no_noise_x_max, no_noise_y_max, no_noise_z_max, max_pollution = pollution_state_3D.get_no_noise_max_pollution_point()
#     print("no_noise_x_max = " + str(no_noise_x_max))
#     print("no_noise_y_max = " + str(no_noise_y_max))
#     print("no_noise_z_max = " + str(no_noise_z_max))
#     print("max_pollution = " + str(max_pollution))
#
#     pollution_list = pollution_state_3D.get_all_pollution_states()
#     x,y,z,pollute = Detect_Square_Area_Max(pollution_list, 0, 0, 0, 100)
#     print("square_area_max_x = " + str(x))
#     print("square_area_max_y = " + str(y))
#     print("square_area_max_z = " + str(z))
#     print("square_area_max_pollution = " + str(pollute))
#
#     Detect_Max(pollution_list, 1, 1, 1, 45, 45, 50)
#
#     start_position_list = list()
#     start_position_list.append(0)
#     start_position_list.append(30)
#     start_position_list.append(0)
#
#     Search_Pollution_On_Arc(pollution_list, start_position_list,1, 20, -45, -30)
#
#     pollution_state_3D.draw_pollution_map()
#
#     Calculate_Degree(0, 0, 0, 10, 10, 14.141414)

####################### main ############################################

if __name__ == "__main__":
    main()
