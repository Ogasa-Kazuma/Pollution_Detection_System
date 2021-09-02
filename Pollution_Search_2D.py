

############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import Pollution_State_2D_lib
############################################################################


class Search_Methods_2D:

    def __init__(self,initial_value):
        #インスタンス変数も privateにできる
        self.__initial_value = initial_value


    def Calculate_Degree(self,start_x_value , start_y_value , end_x_value , end_y_value):
        angle = 0
        angle = math.degrees(math.atan2((end_y_value - start_y_value) , (end_x_value - start_x_value)))
        return angle


    ###########################################################################
    ## Detect_Max
    #
    #
    #
    #
    #
    #
    #　戻り値(濃度最高点のx座標、y座標、そしてその濃度値)
    # 濃度の最高値が、x_startとy_startの地点だった場合（つまり濃度値の初期値が最大値だった場合)、初期座標と初期濃度を返す
    # 最初に渡された座標が、測定範囲外(フィールドサイズを超えてた場合)、初期座標と初期濃度を返す
    # 初期濃度より高い濃度が更新された場合、その座標と濃度を返す
    #
    ###########################################################################


    def Detect_Max(self, pollution_list, x_start, y_start, direction_angle, search_deepness):

        x_now = x_start
        y_now = y_start
        start_density = pollution_list[x_start][y_start]

        near_x = 0
        near_y = 0

        x_max = x_start
        y_max = y_start
        max_density = pollution_list[x_start][y_start]

        array_limit = np.array(pollution_list)
        x_limit, y_limit = array_limit.shape

        first_vector_length = 1
        search_vector_length = first_vector_length

        #while(search_vector_length <= search_deepness): #現在の位置から指定した半径の円の距離だけ値を参照する
        while(abs(abs(x_now) - x_start) < search_deepness and abs(abs(y_now) - y_start) < search_deepness):
            near_x = x_start + search_vector_length * math.cos(math.radians(direction_angle))
            near_y = y_start + search_vector_length * math.sin(math.radians(direction_angle))

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

            # <= ではなく < にするとリストの容量を超える
            if(x_limit <= x_now or y_limit <= y_now):
                if(search_vector_length == first_vector_length):
                    return x_start, y_start, start_density
                else:
                    return x_max, y_max, max_density

            elif(x_now < 0 or y_now < 0):
                if(search_vector_length == first_vector_length):
                    return x_start, y_start, start_density
                else:
                    return x_max, y_max, max_density


            if(max_density < pollution_list[x_now][y_now]):
                #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                if(self.Distinguish_Noise_Pollution(pollution_list, x_now, y_now, 2, 0.3)):
                    pass
                else:
                    max_density = pollution_list[x_now][y_now]
                    x_max = x_now
                    y_max = y_now
                    plt.scatter(x_now, y_now, c='orange')

            #plt.scatter(x_max, y_max, c='green')
           # print(x_now, y_now)
            search_vector_length += 1


        plt.scatter(x_max, y_max, c='green')
        return x_max, y_max, max_density



    def Detect_Square_Area_Max(self, pollution_list, start_pos_poll_list, search_deepness):

        x_now = abs(start_pos_poll_list[0])
        y_now = abs(start_pos_poll_list[1])


        measure_x = x_now - search_deepness / 2
        measure_y = y_now - search_deepness / 2
    #    if  x_now < math.ceil(search_deepness / 2):
    #        measure_x = x_now
    #    else:
    #        measure_x = x_now - search_deepness / 2
    #
    #    if  y_now < math.ceil(search_deepness / 2):
    #        measure_y = y_now
    #    else:
    #        measure_y = y_now - search_deepness / 2

        #小数点以下切り捨て
        measure_x = math.ceil(measure_x)
        measure_y = math.ceil(measure_y)

        max_list = list()

        x_max = 0
        y_max = 0
        max_value = 0

        array_limit = np.array(pollution_list)
        x_limit, y_limit = array_limit.shape

        for x_1 in range(search_deepness):
            for y_1 in range(search_deepness):

                if(0 < (measure_x + x_1) and 0 < (measure_y + y_1)):
                    if((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit):
                        if max_value < pollution_list[measure_x + x_1][measure_y + y_1]:
                            if(self.Distinguish_Noise_Pollution(pollution_list, measure_x + x_1, measure_y + y_1, 2, 0.3)):
                                pass
                            else:
                                max_value = pollution_list[measure_x + x_1][measure_y + y_1]
                                x_max = measure_x + x_1
                                y_max = measure_y + y_1
                    elif(x_limit < (measure_x + x_1) and (measure_y + y_1) < y_limit):
                        if max_value < pollution_list[measure_x + x_1 - (measure_x + x_1 - x_limit)][measure_y + y_1]:
                            if(self.Distinguish_Noise_Pollution(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1, 2, 0.3)):
                                pass
                            else:
                                max_value = pollution_list[measure_x + x_1 - (measure_x + x_1 - x_limit)][measure_y + y_1]
                                x_max = measure_x + x_1 - (measure_x + x_1 - x_limit)
                                y_max = measure_y + y_1
                    elif((measure_x + x_1) < x_limit and y_limit < (measure_y + y_1)):
                        if max_value < pollution_list[measure_x + x_1][measure_y + y_1 - (measure_y + y_1 - y_limit)]:
                            if(self.Distinguish_Noise_Pollution(pollution_list, measure_x + x_1, measure_y + y_1 - (measure_y + y_1 - y_limit), 2, 0.3)):
                                pass
                            else:
                                max_value = pollution_list[measure_x + x_1][measure_y + y_1 - (measure_y + y_1 - y_limit)]
                                x_max = measure_x + x_1
                                y_max = measure_y + y_1 - (measure_y + y_1 - y_limit)
                    elif((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit):
                        break

                else:
                    pass

        max_list.append(x_max)
        max_list.append(y_max)
        max_list.append(max_value)

        return x_max, y_max, max_value




    def Distinguish_Noise_Pollution(self, use_list, x_center_point, y_center_point, measure_area_length, threshold):

        test_x_point = x_center_point
        test_y_point = y_center_point

        use_array = np.array(use_list)
        x_limit, y_limit = use_array.shape

        sum = 0

        for x_count in range(x_center_point - measure_area_length, x_center_point + measure_area_length, 1):
            for y_count in range(y_center_point - measure_area_length, y_center_point + measure_area_length, 1):
                if((x_count < x_limit) and (y_count < y_limit) and 0 <= x_count and 0 <= y_count):
                    sum += use_list[x_count][y_count]
                else:
                    pass

        ave = sum / ((1 + 2 *(measure_area_length)) ** (2))

        return use_list[x_center_point][y_center_point] - ave > threshold








    def Calculate_Distance(self, x_1, y_1, x_2, y_2):

        print('x座標の差' + str(x_2 - x_1))
        print('y座標の差' + str(y_2 - y_1))
        print('2点間の直線距離' + str(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)))


        return x_2 - x_1, y_2 - y_1

    ###########################################################################
    #
    #
    # angle_upper_limit base_angleから見て、時計回り方向に探索する最大の角度範囲
    # angle_lower_limit base_angleから見て、反時計回り方向に探索する最大の角度範囲
    # angle_step angle_upper_limitからangle_lower_limitに順に探索していくとき、どの程度の角度ステップで探索していくかを指定
    # search_deepness 探索深さ
    #
    # 戻り値(濃度最高点のx座標、　y座標、　濃度の値)
    # 初期値からの更新が無い場合、初期点の座標(関数呼び出しの際に渡されたx_start, y_start)とその濃度を返す
    #　最高値が更新された時点で関数の実行を打ち切る。
    #
    #
    #
    #
    ############################################################################
    def Search_Pollution(pollution_list, base_angle, x_start, y_start, angle_upper_limit, angle_lower_limit, angle_step, search_deepness):

        max_pollution = pollution_list[x_start][y_start]
        x_max = x_start
        y_max = y_start

        now_pollution = pollution_list[x_start][y_start]
        x_now = x_start
        y_now = y_start

        one_step_angle = (abs(angle_upper_limit) + abs(angle_lower_limit)) / angle_step
        print('step_angle' + str(one_step_angle))
        for count in range(angle_step):
            if((one_step_angle * count) <= angle_upper_limit):
                x_now, y_now, now_pollution = self.Detect_Max(pollution_list, x_start, y_start, base_angle + one_step_angle * count , search_deepness)
                print('angle plus' + str(base_angle + one_step_angle * count))
                if(max_pollution < now_pollution):
                    max_pollution = now_pollution
                    x_max = x_now
                    y_max = y_now

                    return x_max, y_max, max_pollution

            if((one_step_angle * count) <= angle_lower_limit):
                x_now, y_now, now_pollution = self.Detect_Max(pollution_list, x_start, y_start, base_angle - one_step_angle * count , search_deepness)
                if(max_pollution < now_pollution):
                    max_pollution = now_pollution
                    x_max = x_now
                    y_max = y_now

                    return x_max, y_max, max_pollution


        return x_max, y_max, max_pollution




    def Detect_Pollution_Origin(self, pollution_list, x_start, y_start, x_start_before, y_start_before, angle_upper_limit, angle_lower_limit, angle_step, search_deepness):

        x_max = x_start
        y_max = y_start
        max_pollution = pollution_list[x_start][y_start]

        last_x_max = x_start_before
        last_y_max = y_start_before

        loop_count = 0

        x_now = x_start
        y_now = y_start
        now_pollution = pollution_list[x_start][y_start]

        one_step_angle = (abs(angle_upper_limit) + abs(angle_lower_limit)) / angle_step

        while(True):
            base_angle = self.Calculate_Degree(x_max, y_max, last_x_max, last_y_max)
            while(True):

                if(angle_upper_limit < (one_step_angle * loop_count) and angle_lower_limit < (one_step_angle * loop_count)):
                    return x_max, y_max, pollution_list[x_max][y_max]
                else:
                    if((one_step_angle * loop_count) <= angle_upper_limit):
                        x_now, y_now, now_pollution = self.Detect_Max(pollution_list, x_max, y_max, base_angle + one_step_angle * loop_count, search_deepness)
                        if(max_pollution < now_pollution):
                            last_x_max = x_max
                            last_y_max = y_max
                            x_max = x_now
                            y_max = y_now
                            max_pollution = now_pollution
                            break
                    if((one_step_angle * loop_count) <= angle_lower_limit):
                        x_now, y_now, now_pollution = self.Detect_Max(pollution_list, x_max, y_max, base_angle - one_step_angle * loop_count, search_deepness)
                        if(max_pollution < now_pollution):
                            last_x_max = x_max
                            last_y_max = y_max
                            x_max = x_now
                            y_max = y_now
                            max_pollution = now_pollution
                            break

                loop_count += 1
