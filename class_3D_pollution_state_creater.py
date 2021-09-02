############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
from abc import ABCMeta, abstractmethod

import class_pollution_state_creater
from class_pollution_state_creater import Pollution_State_Creater
import importlib
importlib.reload(class_pollution_state_creater)
############################################################################


####################### start definition class Create_Density ############################
class Pollution_State_Creater_3D(Pollution_State_Creater):


    def __init__(self, field_x_length, field_y_length, field_z_length):

        self.__field_x_length = field_x_length
        self.__field_y_length = field_y_length
        self.__field_z_length = field_z_length

        #x座標の数　→　y方向の数　→　z方向の数
        self.__base_pollution_list = [[[0.0 for z_element_count in range(field_z_length)] for y_element_count in range(field_y_length)]
        for x_element_count in range(field_x_length)]
        #この文がなければfloatでもNoneでもないらしい。とりあえずはリストに要素を代入しろということかな？

        self.__list_local_pollution = [[[0.0 for j in range(field_z_length)] for l in range(field_y_length)] for k in range(field_x_length)]
        self.__list_random_pollution = [[[0.0 for j in range(field_z_length)] for l in range(field_y_length)] for k in range(field_x_length)]
        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    self.__base_pollution_list[x_count][y_count][z_count] = 0.0
                    self.__list_local_pollution[x_count][y_count][z_count] = 0.0
                    self.__list_random_pollution[x_count][y_count][z_count] = 0.0



    def create_local_pollution(self, xBegin, yBegin, zBegin, scope_radius, max_pollution_density):


        #移動距離に対する濃度の減少量
        self.__pollution_decreasing_step = max_pollution_density / scope_radius


        for x_count in range(xBegin - scope_radius, xBegin + scope_radius, 1):
            for y_count in range(yBegin - scope_radius, yBegin + scope_radius, 1):
                for z_count in range(zBegin - scope_radius, zBegin + scope_radius, 1):
                    if(0 <= x_count and 0 <= y_count and 0 <= z_count and x_count < self.__field_x_length and y_count < self.__field_y_length and z_count < self.__field_z_length):

                        self.__list_local_pollution[x_count][y_count][z_count] = max_pollution_density - self.__pollution_decreasing_step * np.sqrt(abs(xBegin - x_count) ** (2) + abs(yBegin - y_count) ** (2) + abs(zBegin - z_count) ** (2))
                        if(self.__list_local_pollution[x_count][y_count][z_count] < 0):
                            self.__list_local_pollution[x_count][y_count][z_count] = 0
                        self.__base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] + self.__list_local_pollution[x_count][y_count][z_count]

        ret_list_local_pollution = self.__list_local_pollution
        for x_count in range(self.__field_x_length):
            for y_count  in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    self.__list_local_pollution[x_count][y_count][z_count] = 0.0

                    return ret_list_local_pollution


    def get_no_noise_max_pollution_point(self):

        no_noise_base_pollution_list = [[[0.0 for j in range(self.__field_z_length)] for l in range(self.__field_y_length)] for k in range(self.__field_x_length)]

        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    no_noise_base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] - self.__list_random_pollution[x_count][y_count][z_count]

        #selfを付けないと、クラス内でも関数内ローカル変数を定義することが出来る
        no_noise_x_max = 0
        no_noise_y_max = 0
        no_noise_z_max = 0


        #アスタリスクの作用について検証
        max_no_noise_pollution = max(chain(*chain(*no_noise_base_pollution_list)))
        print(chain(*chain(*no_noise_base_pollution_list)))


        print('max_no_noise_pollution' + str(max_no_noise_pollution))

        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    if(max_no_noise_pollution == no_noise_base_pollution_list[x_count][y_count][z_count]):
                        no_noise_x_max = x_count
                        no_noise_y_max = y_count
                        no_noise_z_max = z_count

        return no_noise_x_max, no_noise_y_max, no_noise_z_max, no_noise_base_pollution_list[no_noise_x_max][no_noise_y_max][no_noise_z_max]



    def create_random_pollution(self, probability, start_x, start_y, start_z, end_x, end_y, end_z, upper_limit, lower_limit):

        print(100 - probability)
        for x_count in range(end_x - start_x):
            for y_count in range(end_y - start_y):
                for z_count in range(end_z - start_z):
                    # ram_probability = random.random() * 95.0 # 95.0以下で発生しなくなる
                    # if((100.0 - probability) <= ram_probability):
                    #なんでrandrangeのところ,0-100なの？
                    #random.randrange(0, 100, 1)
                    if((100 - probability) <= random.randrange(0, 100, 1)):

                    # if((100.0 - probability) <= random.random() * 100 + random.random() * 10 - 10):
                        ram = 0
                        while(ram < lower_limit or upper_limit < ram):
                            ram = random.randrange(1, 100, 1) #この処理だと、最高濃度値は100にならない（つまり最高濃度値（ノイズ無しの場合の）を超えたり、等しい値になったりはしない）

                        self.__list_random_pollution[x_count][y_count][z_count] = ram
                        self.__base_pollution_list[x_count][y_count][z_count] = self.__list_random_pollution[x_count][y_count][z_count]
                    else:
                        self.__list_random_pollution[x_count][y_count][z_count] = 0



        return self.__list_random_pollution



    def Auto_Pollutions_Create(self, number, max_pollution, maxRadiusOfPollution):

        x = [self.__field_x_length + 1 for i in range(number)]
        y = [self.__field_y_length + 1 for i in range(number)]
        z = [self.__field_z_length + 1 for i in range(number)]
        pollution_density = [1.1 for i in range(number)]
        radius = [0.0 for i in range(number)]

        radius_limit = maxRadiusOfPollution
        print('radius_limit' + str(radius_limit))

        for count in range(number):
            while(self.__field_x_length < x[count]):
                x[count] = random.random() * 100 + random.random() * 10
            while(self.__field_y_length < y[count]):
                y[count] = random.random() * 100 + random.random() * 10
            while(self.__field_z_length < z[count]):
                z[count] = random.random() * 100 + random.random() * 10
            while(max_pollution < pollution_density[count]):
                pollution_density[count] = random.random() * 100 + random.random() * 10
            while(0 == int(radius[count]) or (radius_limit / 2) < radius[count]):
                radius[count] = random.random() * 100 + random.random() * 10

            print(str(int(radius[count])))
            self.create_local_pollution(int(x[count]), int(y[count]), int(z[count]), int(radius[count]), pollution_density[count])




    def Adjust_Pollution(self, upper_limit, lower_limit):

    #モード = Trueなら除算により、全ての濃度値(濃度値リストの全ての値)を一定の値で割る
        max_base_pollution = max(chain(*chain(*self.__base_pollution_list)))
        print('max_base_pollution = ' + str(max_base_pollution))
        division_ratio = max_base_pollution / upper_limit
        print(division_ratio)
        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    self.__base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] / division_ratio



    def get_all_pollution_states(self):
        return self.__base_pollution_list
##################  end definition class Create_Density #####################################
