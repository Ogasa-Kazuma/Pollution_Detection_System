############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
from abc import ABCMeta, abstractmethod

import class_pollution_state_drawer
from class_pollution_state_drawer import Pollution_State_Drawer
import importlib
importlib.reload(class_pollution_state_drawer)
############################################################################


####################### start definition class Create_Density ############################
class Pollution_State_Drawer_3D(Pollution_State_Drawer):


    def __init__(self, figure_object, drawing_area):

        self.__figure_object = figure_object.add_subplot(drawing_area, projection = '3d')

    def draw_pollution_map(self, pollutions, concentration_limit_to_display):


        # self.__figure_object = Axes3D(fig)
        # ax2 = Axes3D(fig)
        # 軸のラベルを設定する。
        self.__figure_object.set_xlabel('x')
        self.__figure_object.set_ylabel('y')
        self.__figure_object.set_zlabel('z')

        pollutions_converted_to_array = np.array(pollutions)
        x_element_count, y_element_count, z_element_count = pollutions_converted_to_array.shape

        X = [[[j for j in range(0, z_element_count, 1)] for l in range(0, y_element_count, 1)] for k in range(0, x_element_count, 1)]
        Y = [[[j for j in range(0, z_element_count, 1)] for l in range(0, y_element_count, 1)] for k in range(0, x_element_count, 1)]
        Z = [[[j for j in range(0, z_element_count, 1)] for l in range(0, y_element_count, 1)] for k in range(0, x_element_count, 1)]

        #X, Y, Zの値の順序を合わせる。この処理がないと、X, Y, Zの値の対応（組み合わせ？）がおかしくなる。
        #Xについて、この処理がないと、0,1,2 ・・・・ 0,1,2・・・0,1,2・・・となってしまうが
        #0,0,0,0・・・1,1,1,1,1・・・・・・19,19,19,19となるようにしたい。そのための処理が下記である。
        for x_count in range(x_element_count):
                for y_count in range(y_element_count):
                    for z_count in range(z_element_count):
                            X[x_count][y_count][z_count] = x_count

        #Yについても同様。ただ、Xはfield * fieldの要素数がカウントされてから数値が増え始めるが
        #Yはfield_size分の要素数がカウントされてから数値が増え始める。つまりYの方が数値の上昇が早い
        for x_count in range(x_element_count):
            for y_count in range(y_element_count):
                for z_count in range(z_element_count):
                        Y[x_count][y_count][z_count] = y_count


        #chainのあとに　* 掛け算のマーク？をつけないとリストの次元が下がらない
        pollutions = list(chain(*chain(*pollutions)))

        index_list_of_element_delete_to = list() #空のリストを生成
        del_count = 0

        for index_count in range(len(pollutions)):
            if(pollutions[index_count] < concentration_limit_to_display): #指定した濃度値より低い場合は、その要素と、対応する座標を削除する
                index_list_of_element_delete_to.append(index_count)

        #delするときにAlphaと要素数を合わせるために一次元に
        X = list(chain(*chain(*X)))
        Y = list(chain(*chain(*Y)))
        Z = list(chain(*chain(*Z)))

        #指定した濃度より低い濃度だった場合、対応する濃度値とその座標を削除する
        for del_index in index_list_of_element_delete_to:
            #要素を削除するたびに、対象のリストの、次に消したい要素のインデックスが1下がる ので　マイナス　del_count
            del pollutions[del_index - del_count]
            del X[del_index - del_count]
            del Y[del_index - del_count]
            del Z[del_index - del_count]

            del_count += 1


        #X, Y, Z, はfloatかarray-like、　カラーcはarray-likeなもの、つまりリストとかがいい。
        #リストとかではなく、単一の値を、for文を使って一つずつ当てはめていく方法は上手くいかない。
        #たぶん scatter3Dの文が一回しか使えないのか？最初の一回目の実行しか適用されてなかった。
        self.__sc = self.__figure_object.scatter3D(X, Y, Z, c = pollutions, s = 0.1, cmap = 'binary',alpha = 0.3, vmin= 0, vmax=100)


        # fig.colorbar(sc)

        # plt.tight_layout()

        plt.show()


def main():




    pollutions =  [[[j for j in range(40)] for l in range(40)] for k in range(40)]
    for x_count in range(40):
        for y_count in range(40):
            for z_count in range(40):
                pollutions[x_count][y_count][z_count] = 60



    fig = plt.figure()


    test_plt = Pollution_State_Drawer_3D(fig, 111)
    test_plt.draw_pollution_map(pollutions, 60)


    fig2 = plt.figure()


    test_plt2 = Pollution_State_Drawer_3D(fig2, 122)
    test_plt2.draw_pollution_map(pollutions, 60)


    fig3 = plt.figure()

    test_plt3 = Pollution_State_Drawer_3D(fig3, 122)
    test_plt3.draw_pollution_map(pollutions, 60)


    plt.scatter(1,1)


if __name__ == "__main__":
    main()
