############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections

import common
import class_2D_pollution_state_creater
import class_3D_pollution_state_creater
import class_pollution_state_drawer_2D
import class_pollution_state_drawer_3D
import class_dimension_converter
import class_pollution_searcher
from class_2D_pollution_state_creater import Pollution_State_Creater_2D
from class_pollution_state_drawer_3D import Pollution_State_Drawer_3D
import Process_Visualizer


import importlib
importlib.reload(common)
importlib.reload(class_dimension_converter)
importlib.reload(class_2D_pollution_state_creater)
importlib.reload(class_3D_pollution_state_creater)
importlib.reload(class_pollution_state_drawer_2D)
importlib.reload(class_pollution_state_drawer_3D)
importlib.reload(class_pollution_searcher)
importlib.reload(Process_Visualizer)
############################################################################


#濃度探索過程を可視化するクラス
class ProcessVisualizer:

    def __init__(self, fig, drawingArea):
        self.__axes = fig.add_subplot(drawingArea)
        self.__drawingArea = drawingArea
        self.__colorOfPlotPoint = "black" #デフォルトのプロット色は黒
        self.__sizeOfPlotPoint = 20 #デフォルトのプロット点の大きさ

    def setColorOfPlotPoint(self, color):
        #色指定に文字列以外が来た場合はエラー
        if(not type(color) == str):
            print("Error setting plot color requires str argument")
            return

        self.__colorOfPlotPoint = color

    def setSizeOfPlotPoint(self, size):
        self.__sizeOfPlotPoint = size


    def  DrawSearchedPoints(self, xPositions, yPositions):
        #座標を示すリストは1次元リストでなければならない
        if(not common.DeriveListDimension(xPositions) == 1 or not common.DeriveListDimension(yPositions) == 1):
            print("dimensiton" + str(common.DeriveListDimension(xPositions)))
            print("Function DrawPathOfSearched require 1 dimension lists")
            return

        elementsCount = common.DeriveListElementsCount(xPositions) #yPositionsでもよい
        elementsCount = elementsCount[0] #タプル値をfor文で扱えるようにする
        for i in range(elementsCount):
            self.__axes.scatter(xPositions[i], yPositions[i], c = self.__colorOfPlotPoint, s = self.__sizeOfPlotPoint, alpha = 1)
