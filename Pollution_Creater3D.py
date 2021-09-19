
############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
import pandas as pd
import datetime
import os
from pathlib import Path
import statistics
import copy

import common
import common3d
import class_2D_pollution_state_creater
import class_3D_pollution_state_creater
import class_pollution_state_drawer_2D
import class_pollution_state_drawer_3D
import class_dimension_converter
import class_pollution_searcher
from class_2D_pollution_state_creater import Pollution_State_Creater_2D
from class_pollution_state_drawer_3D import Pollution_State_Drawer_3D
import Process_Visualizer
import Data_Recorder


import importlib
importlib.reload(common)
importlib.reload(common3d)
importlib.reload(class_dimension_converter)
importlib.reload(class_2D_pollution_state_creater)
importlib.reload(class_3D_pollution_state_creater)
importlib.reload(class_pollution_state_drawer_2D)
importlib.reload(class_pollution_state_drawer_3D)
importlib.reload(class_pollution_searcher)
importlib.reload(Process_Visualizer)
importlib.reload(Data_Recorder)
############################################################################

class PollutionCreater3D:

    def __init__(self, field_x_length, field_y_length, field_z_length):

        self.__field_x_length = field_x_length
        self.__field_y_length = field_y_length
        self.__field_z_length = field_z_length

        #x座標の数　→　y方向の数　→　z方向の数
        # self.__base_pollution_list = np.zeros((field_x_length, field_y_length, field_z_length), dtype = "float64")
        self.__base_pollution_list = [[[0.0 for z_element_count in range(field_z_length)] for y_element_count in range(field_y_length)]
        for x_element_count in range(field_x_length)]
        #この文がなければfloatでもNoneでもないらしい。とりあえずはリストに要素を代入しろということかな？
        # self.__list_local_pollution = np.zeros((field_x_length, field_y_length, field_z_length), dtype = "float64")
        self.__list_local_pollution = [[[0.0 for j in range(field_z_length)] for l in range(field_y_length)] for k in range(field_x_length)]

        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    self.__base_pollution_list[x_count][y_count][z_count] = 0.0
                    self.__list_local_pollution[x_count][y_count][z_count] = 0.0




    def CreateRoundPollution(self, xBegin, yBegin, zBegin, scope_radius, max_pollution_density):


        #移動距離に対する濃度の減少量
        self.__pollution_decreasing_step = max_pollution_density / scope_radius


        for x_count in range(xBegin - scope_radius, xBegin + scope_radius, 1):
            for y_count in range(yBegin - scope_radius, yBegin + scope_radius, 1):
                for z_count in range(zBegin - scope_radius, zBegin + scope_radius, 1):
                    if(0 <= x_count and 0 <= y_count and 0 <= z_count and x_count < self.__field_x_length and y_count < self.__field_y_length and z_count < self.__field_z_length):

                        self.__list_local_pollution[x_count][y_count][z_count] = max_pollution_density - self.__pollution_decreasing_step * math.sqrt((xBegin - x_count) ** (2) + (yBegin - y_count) ** (2) + (zBegin - z_count) ** (2))

                        if(self.__list_local_pollution[x_count][y_count][z_count] < 0):
                            self.__list_local_pollution[x_count][y_count][z_count] = 0
                        self.__base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] + self.__list_local_pollution[x_count][y_count][z_count]
                        self.__list_local_pollution[x_count][y_count][z_count] = 0.0

        # ret_list_local_pollution = self.__list_local_pollution
        # for x_count in range(self.__field_x_length):
        #     for y_count in range(self.__field_y_length):
        #         for z_count in range(self.__field_z_length):
        #             self.__list_local_pollution[x_count][y_count][z_count] = 0.0
        #
        #             return ret_list_local_pollution


    def get_no_noise_max_pollution_point(self):

        no_noise_base_pollution_list = copy.deepcopy(self.__base_pollution_list)#[[[0.0 for j in range(self.__field_z_length)] for l in range(self.__field_y_length)] for k in range(self.__field_x_length)]



        #selfを付けないと、クラス内でも関数内ローカル変数を定義することが出来る
        no_noise_x_max = 0
        no_noise_y_max = 0
        no_noise_z_max = 0


        #アスタリスクの作用について検証
        max_no_noise_pollution = max(chain(*chain(*no_noise_base_pollution_list)))



        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                for z_count in range(self.__field_z_length):
                    if(max_no_noise_pollution == no_noise_base_pollution_list[x_count][y_count][z_count]):
                        no_noise_x_max = x_count
                        no_noise_y_max = y_count
                        no_noise_z_max = z_count

        return no_noise_x_max, no_noise_y_max, no_noise_z_max, no_noise_base_pollution_list[no_noise_x_max][no_noise_y_max][no_noise_z_max]







    def CreateRandomPollutions(self, number, xRange, yRange, zRange, rangeOfPollutionRadius, rangeOfMaxPollution):
        if(not(len(xRange) == 2 and len(yRange) == 2 and len(zRange) == 2 and \
        len(rangeOfPollutionRadius) == 2 and len(rangeOfMaxPollution) == 2)):
            raise ValueError("CreateRandomPollutions Pollution_Creater3D.py requires 2 elements lists")

        pollutions = [[[0.0 for z in range(self.__field_z_length)] for y in range(self.__field_y_length)]
        for x in range(self.__field_x_length)]

        for i in range(number):
            x = random.randint(xRange[0], xRange[1])
            y = random.randint(yRange[0], yRange[1])
            z = random.randint(zRange[0], zRange[1])

            pollutionRadius = random.randint(rangeOfPollutionRadius[0], rangeOfPollutionRadius[1])
            maxConcentration = random.uniform(rangeOfMaxPollution[0], rangeOfMaxPollution[1])

            #移動距離に対する濃度の減少量
            decreasingRatio = maxConcentration / pollutionRadius

            for x_ in range(x - pollutionRadius, x + pollutionRadius, 1):
                for y_ in range(y - pollutionRadius, y + pollutionRadius, 1):
                    for z_ in range(z - pollutionRadius, z + pollutionRadius, 1):
                        if(0 <= x_ and 0 <= y_ and 0 <= z_ and x_ < self.__field_x_length and y_ < self.__field_y_length and z_ < self.__field_z_length):

                            addValue = maxConcentration - decreasingRatio * \
                            math.sqrt((x - x_) ** (2) + (y - y_) ** (2) + (z - z_) ** (2))

                            if(addValue < 0):
                                addValue = 0
                            pollutions[x_][y_][z_] += addValue


        return pollutions

            #self.CreateRoundPollution(x, y, z, pollutionRadius, concentration)





def AdjustPollutionRange(pollutions, upper_limit, lower_limit):

    pollutions_ = pollutions.copy()
    maxConcentration = max(pollutions_.flatten())
    division_ratio = maxConcentration / upper_limit

    xlim, ylim, zlim = pollutions.shape
    for x in range(xlim):
        for y in range(ylim):
            for z in range(zlim):
                pollutions_[x][y][z] = pollutions_[x][y][z] / division_ratio

    return pollutions_

#
#
# field_x_length = 100
# field_y_length = 100
# field_z_length = 30
#
#
# pollutionCreater3D = PollutionCreater3D(100, 100, 30)
#
# #特定汚染源を生成。規模は大きめ
# pollutions = pollutionCreater3D.CreateRandomPollutions(number = 10, xRange = [0, 0], yRange = [0, field_y_length - 1], \
# zRange = [field_z_length - 6, field_z_length - 1], rangeOfPollutionRadius = [10, 30], rangeOfMaxPollution =[0, 100])
#
#
# fig = plt.figure()
# pollutionDrawer3D = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(fig, 221)
# pollutionDrawer3D.draw_pollution_map(AdjustPollutionRange(np.array(pollutions), 100, 0), 10, 100, 100, 100)
#



#
#
#
#
#
#
# field_x_length = 100
# field_y_length = 100
# field_z_length = 30
#
#
# pollutionCreater3D = PollutionCreater3D(100, 100, 30)
#
# #特定汚染源を生成。規模は大きめ
# pollutionCreater3D.CreateRandomPollutions(number = 4, xRange = [0, 0], yRange = [0, field_y_length - 1], \
# zRange = [field_z_length - 6, field_z_length - 1], rangeOfPollutionRadius = [70, 70], pollutionRange =[0, 100])
#
# #非特定汚染源を生成。規模は小さめ
# pollutionCreater3D.CreateRandomPollutions(number = 40, xRange = [0, 0], yRange = [0, field_y_length - 1], \
# zRange = [field_z_length - 6, field_z_length - 1], rangeOfPollutionRadius = [20, 20], pollutionRange = [0, 100])
#
# #溶出による汚染モデルを生成
# # pollutionCreater3D.CreateRandomPollutions(number = 20, xRange = [0, field_x_length - 1], yRange = [0, field_y_length - 1], \
# # zRange = [0, 0], rangeOfPollutionRadius = [50, 50], pollutionRange = [0, 50])
#
# #濃度値を最大100, 最低0の範囲に設定
# pollutionCreater3D.AdjustPollutionRange(100, 0)
#
#
#
#
# fig = plt.figure()
# pollutionDrawer3D = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(fig, 221)
# pollutionDrawer3D.draw_pollution_map(pollutionCreater3D.getPollutions(), 10, 100, 100, 100)
#
#
#
# extractedList = common.ExtractList(pollutionCreater3D.getPollutions(), [0, 50], [0, 50], [0, 30])
#
# fig2 = plt.figure()
# pollutionDrawer3D_2 = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(fig2, 221)
# pollutionDrawer3D_2.draw_pollution_map(extractedList, 3, 50, 50, 30)
#
# fig3 = plt.figure()
# pollutionDrawer3D_2 = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(fig3, 221)
# pollutionDrawer3D_2.draw_pollution_map(extractedList, 3, 20, 50, 30)






#
# dimensionConverter = class_dimension_converter.Dimension_Converter(pollutionCreater3D.getPollutions())
# convertedPollutions = dimensionConverter.Convert_Dimension(3, 100, 0, 1, 0)
#
# fig2 = plt.figure()
# pollutionDrawer2D = class_pollution_state_drawer_2D.Pollution_State_Drawer_2D(fig2, 221)
# pollutionDrawer2D.draw_pollution_map(convertedPollutions)
