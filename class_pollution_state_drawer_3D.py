############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
from abc import ABCMeta, abstractmethod
import time



import class_pollution_state_drawer
from class_pollution_state_drawer import Pollution_State_Drawer
import importlib
importlib.reload(class_pollution_state_drawer)
############################################################################


####################### start definition class Create_Density ############################
class Pollution_State_Drawer_3D(Pollution_State_Drawer):


    def __init__(self, figure_object, drawing_area):

        self.__figure_object = figure_object.add_subplot(drawing_area, projection = '3d')
        self.__sizeOfPlotPoint = 0.1
        self.__cmap = "binary"

    def setSizeOfPlotPoint(self, sizeOfPlotPoint):
        self.__sizeOfPlotPoint = sizeOfPlotPoint

    def setAspectRatio(self, ratios):
        self.__figure_object.set_box_aspect((ratios[0], ratios[1], ratios[2]))

    def setCmap(self, cmap):
        self.__cmap = str(cmap)



    def draw_pollution_map(self, pollutions, concentration_limit_to_display, xlim, ylim, zlim):


        # self.__figure_object = Axes3D(fig)
        # ax2 = Axes3D(fig)
        # 軸のラベルを設定する。
        self.__figure_object.set_xlabel('x')
        self.__figure_object.set_ylabel('y')
        self.__figure_object.set_zlabel('z')


        pollutions_converted_to_array = np.array(pollutions)
        x_element_count, y_element_count, z_element_count = pollutions_converted_to_array.shape


        new_x = []
        new_y = []
        new_z = []
        new_pollutions = []
        for x_count in range(x_element_count):
            for y_count in range(y_element_count):
                for z_count in range(z_element_count):
                    if(pollutions[x_count][y_count][z_count] > concentration_limit_to_display):
                        new_x.append(x_count)
                        new_y.append(y_count)
                        new_z.append(z_count)
                        new_pollutions.append(pollutions[x_count][y_count][z_count])



        #X, Y, Z, はfloatかarray-like、　カラーcはarray-likeなもの、つまりリストとかがいい。
        #リストとかではなく、単一の値を、for文を使って一つずつ当てはめていく方法は上手くいかない。
        #たぶん scatter3Dの文が一回しか使えないのか？最初の一回目の実行しか適用されてなかった。

        self.__figure_object.set_xlim(0, xlim)
        self.__figure_object.set_ylim(0, ylim)
        self.__figure_object.set_zlim(0, zlim)
        self.__sc = self.__figure_object.scatter3D(new_x, new_y, new_z, c = new_pollutions, s = self.__sizeOfPlotPoint, cmap = self.__cmap,alpha = 0.3, vmin= 0, vmax=100)



        plt.show()
