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
import time

import common
import common3d
import Pollution_Creater3D
import class_2D_pollution_state_creater
import class_3D_pollution_state_creater
import class_pollution_state_drawer_2D
import class_pollution_state_drawer_3D
import class_dimension_converter
import class_pollution_searcher
import Random_Searcher
from class_2D_pollution_state_creater import Pollution_State_Creater_2D
from class_pollution_state_drawer_3D import Pollution_State_Drawer_3D
import Process_Visualizer


import Data_Recorder


import importlib
importlib.reload(common)
importlib.reload(common3d)
importlib.reload(Pollution_Creater3D)
importlib.reload(class_dimension_converter)
importlib.reload(class_2D_pollution_state_creater)
importlib.reload(class_3D_pollution_state_creater)
importlib.reload(class_pollution_state_drawer_2D)
importlib.reload(class_pollution_state_drawer_3D)
importlib.reload(class_pollution_searcher)
importlib.reload(Random_Searcher)
importlib.reload(Process_Visualizer)

importlib.reload(Data_Recorder)
############################################################################


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


def ConfusePollutions(*pollutions):

    xlim, ylim, zlim = pollutions[0].shape
    pollutions_ = np.zeros((xlim, ylim, zlim))

    for pollutions_i in pollutions:
        for x in range(xlim):
            for y in range(ylim):
                for z in range(zlim):
                    pollutions_[x][y][z] += pollutions_i[x][y][z]

    return pollutions_







######################## main ###########################################
def main():

    field_x_length = 500
    field_y_length = 500
    field_z_length = 20

    #汚染源作成用パラメータ
    maxRadiusOfPollution = 100 #汚染源の、汚染が影響する範囲の半径
    max_pollution = 100 #濃度最大値
    min_pollution = 0

    #探索パラメータ
    targetConcentration = 85

    ###########################################################
    ##汚染状態の作成
    #############################################################


    pollutionCreater3D = Pollution_Creater3D.PollutionCreater3D(field_x_length, field_y_length, field_z_length)

    #特定汚染源を作成
    specifiablePollutions = pollutionCreater3D.CreateRandomPollutions(1, xRange = [0, 0], \
    yRange = [0, field_y_length], \
    zRange = [field_z_length - 6, field_z_length - 1], \
    rangeOfPollutionRadius = [round(field_y_length / 2), field_y_length], \
    rangeOfMaxPollution = [max_pollution, max_pollution]) #numberは作る濃度の個数

    #非特定汚染源を作成
    unspecifiablePollutions = pollutionCreater3D.CreateRandomPollutions(15, xRange = [0, 0], \
    yRange = [0, field_y_length], \
    zRange = [field_z_length - 6, field_z_length - 1], \
    rangeOfPollutionRadius = [round(field_y_length / 15), round(field_y_length / 10)], \
    rangeOfMaxPollution = [max_pollution, max_pollution]) #numberは作る濃度の個数


    #pollution_creater_3D.create_local_pollution(20, 20, 20, 20, 100)
    unspecifiablePollutions = AdjustPollutionRange(np.array(unspecifiablePollutions), upper_limit = 45, lower_limit = min_pollution)
    specifiablePollutions = AdjustPollutionRange(np.array(specifiablePollutions), upper_limit = 100, lower_limit = min_pollution)
    allPollutions = ConfusePollutions(specifiablePollutions, unspecifiablePollutions)
    allPollutions = AdjustPollutionRange(allPollutions, upper_limit = 100, lower_limit = 0)

    #濃度分布の描画
    figure_to_show_3d_pollutions_state = plt.figure()
    drawing_area_of_3d_all_pollutions_states = 121
    pollution_state_drawer_3D = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(figure_to_show_3d_pollutions_state, drawing_area_of_3d_all_pollutions_states)
    pollution_state_drawer_3D.setSizeOfPlotPoint(2) #0.1とかもちょうどいい
    pollution_state_drawer_3D.setAspectRatio([field_x_length, field_y_length, field_z_length])
    pollution_state_drawer_3D.draw_pollution_map(allPollutions, \
    concentration_limit_to_display = 25, xlim = field_x_length, \
    ylim = field_x_length, zlim = field_z_length)



    #ノイズなしの場合の濃度最高値と、濃度最高値を示す座標を表示
    xOfTrueMax, yOfTrueMax, zOfTrueMax, trueMaxConcentration = pollutionCreater3D.get_no_noise_max_pollution_point()
    print("\033[31m" + "真のx_max" + str(xOfTrueMax) + '\033[0m')
    print("\033[31m" + "真のy_max" + str(yOfTrueMax) + '\033[0m')
    print("\033[31m" + "真のz_max" + str(zOfTrueMax) + '\033[0m')
    print("\033[31m" + "真のpollution_max" + str(trueMaxConcentration) + '\033[0m')


    ############################################################
    ## 探索開始
    #############################################################


    pollutionSearcher = Random_Searcher.RandomSearcher()
    xOfMax, yOfMax, zOfMax, maxConcentration = pollutionSearcher.SearchTargetPollution(allPollutions, targetConcentration)



    #探索結果を表示
    print("探索結果")
    print("x = " + str(xOfMax))
    print("y = " + str(yOfMax))
    print("z = " + str(zOfMax))
    print("最高濃度値 = " + str(maxConcentration))

    print("探索距離" + str(pollutionSearcher.CalculateSearchingDistance()))







    ##################################################################
    ##オプション機能
    ##################################################################
    # #濃度分布の描画
    # figure_to_show_3d_pollutions_state = plt.figure()
    # drawing_area_of_3d_all_pollutions_states = 121
    # pollution_state_drawer_3D = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(figure_to_show_3d_pollutions_state, drawing_area_of_3d_all_pollutions_states)
    # pollution_state_drawer_3D.setSizeOfPlotPoint(2) #0.1とかもちょうどいい
    # pollution_state_drawer_3D.draw_pollution_map(pollutions3D, concentration_limit_to_display = 5)
    #
    # #得られた切り抜き濃度リストを2次元リストに変換
    # dimension_converter = class_dimension_converter.Dimension_Converter(pollutions3D)
    # #zBegin の値と同じ
    # convertedPollutions = dimension_converter.Convert_Dimension(z_point_to_delete = 19, upper_limit_3D = 100, lower_limit_3D = 0, \
    # upper_limit_2D = 1, lower_limit_2D = 0)
    #
    # #2次元に変換した切り抜き濃度リストを描画
    # fig2d = plt.figure()
    # # drawingArea2d221 = 221
    # # pollution_state_drawer_2D_area111 = class_pollution_state_drawer_2D.Pollution_State_Drawer_2D(fig2d, drawingArea2d221)
    # # pollution_state_drawer_2D_area111.draw_pollution_map(convertedPollutions)
    #
    # #探索結果を表示
    # # print("探索結果")
    # # print("x = " + str(xOfMax))
    # # print("y = " + str(yOfMax))
    # # print("z = " + str(zOfMax))
    # # print("最高濃度値 = " + str(maxConcentration))
    # #
    # # print(pollution_searcher.getPathOfSearchedZ())



####################### main ############################################

if __name__ == "__main__":
    main()
