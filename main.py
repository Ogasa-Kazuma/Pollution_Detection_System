############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
############################################################################


########################### Global Variables ################################
field_x_length = 50
field_y_length = 50
#ノイズ閾値
#ノイズ最高値
#ノイズ最小値
#ノイズ発生確率
#探索深さ
#探索方向
#汚染源決定閾値




##########################################################################3



####################### start definition class Create_Density ############################
class Create_Density:

    def __init__(self,field_size):
        #インスタンス変数も privateにできる

        self.__field_size = field_size
        #x座標の数　→　y方向の数　→　z方向の数
        self.__base_pollution_list = [[[0.0 for j in range(field_size)] for l in range(field_size)] for k in range(field_size)]
        #この文がなければfloatでもNoneでもないらしい。とりあえずはリストに要素を代入しろということかな？

        self.__list_local_pollution = [[[0.0 for j in range(field_size)] for l in range(field_size)] for k in range(field_size)]
        self.__list_random_pollution = [[[0.0 for j in range(field_size)] for l in range(field_size)] for k in range(field_size)]
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
                    self.__base_pollution_list[x_count][y_count][z_count] = 0.0
                    self.__list_local_pollution[x_count][y_count][z_count] = 0.0
                    self.__list_random_pollution[x_count][y_count][z_count] = 0.0




    def create_local_pollution(self, x_center, y_center, z_center, scope_radius, max_pollution_density):


        #移動距離に対する濃度の減少量
        self.__pollution_decreasing_step = max_pollution_density / scope_radius


        for x_count in range(x_center - scope_radius, x_center + scope_radius, 1):
            for y_count in range(y_center - scope_radius, y_center + scope_radius, 1):
                for z_count in range(z_center - scope_radius, z_center + scope_radius, 1):
                    if(0 <= x_count and 0 <= y_count and 0 <= z_count and x_count < self.__field_size and y_count < self.__field_size and z_count < self.__field_size):

                        self.__list_local_pollution[x_count][y_count][z_count] = max_pollution_density - self.__pollution_decreasing_step * np.sqrt(abs(x_center - x_count) ** (2) + abs(y_center - y_count) ** (2) + abs(z_center - z_count) ** (2))
                        if(self.__list_local_pollution[x_count][y_count][z_count] < 0):
                            self.__list_local_pollution[x_count][y_count][z_count] = 0
                        self.__base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] + self.__list_local_pollution[x_count][y_count][z_count]

        ret_list_local_pollution = self.__list_local_pollution
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
                    self.__list_local_pollution[x_count][y_count][z_count] = 0.0

                    return ret_list_local_pollution


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





    def draw_pollution_map(self):
        # ここからグラフ描画
        # フォントの種類とサイズを設定する。


        # グラフの入れ物を用意する。
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1, projection='3d')
        ax2 = fig.add_subplot(1, 2, 2, projection='3d')
        # ax1 = Axes3D(fig)
        # ax2 = Axes3D(fig)
        # 軸のラベルを設定する。
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_zlabel('z')

        X = [[[j for j in range(0, self.__field_size, 1)] for l in range(0, self.__field_size, 1)] for k in range(0, self.__field_size, 1)]
        Y = [[[j for j in range(0, self.__field_size, 1)] for l in range(0, self.__field_size, 1)] for k in range(0, self.__field_size, 1)]
        Z = [[[j for j in range(0, self.__field_size, 1)] for l in range(0, self.__field_size, 1)] for k in range(0, self.__field_size, 1)]

        #X, Y, Zの値の順序を合わせる。この処理がないと、X, Y, Zの値の対応（組み合わせ？）がおかしくなる。
        #Xについて、この処理がないと、0,1,2 ・・・・ 0,1,2・・・0,1,2・・・となってしまうが
        #0,0,0,0・・・1,1,1,1,1・・・・・・19,19,19,19となるようにしたい。そのための処理が下記である。
        for x_count in range(self.__field_size):
                for y_count in range(self.__field_size):
                    for z_count in range(self.__field_size):
                            X[x_count][y_count][z_count] = x_count

        #Yについても同様。ただ、Xはfield * fieldの要素数がカウントされてから数値が増え始めるが
        #Yはfield_size分の要素数がカウントされてから数値が増え始める。つまりYの方が数値の上昇が早い
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
                        Y[x_count][y_count][z_count] = y_count


        #chainのあとに　* 掛け算のマーク？をつけないとリストの次元が下がらない
        Alpha = list(chain(*chain(*self.__base_pollution_list)))

        print(len(Alpha))
        del_index_list = list() #空のリストを生成
        del_count = 0

        for index_count in range(len(Alpha)):
            if(Alpha[index_count] < 70): #指定した濃度値より低い場合は、その要素と、対応する座標を削除する
                del_index_list.append(index_count)

        #delするときにAlphaと要素数を合わせるために一次元に
        X = list(chain(*chain(*X)))
        Y = list(chain(*chain(*Y)))
        Z = list(chain(*chain(*Z)))

        #指定した濃度より低い濃度だった場合、対応する濃度値とその座標を削除する
        for del_index in del_index_list:
            #要素を削除するたびに、対象のリストの、次に消したい要素のインデックスが1下がる ので　マイナス　del_count
            del Alpha[del_index - del_count]
            del X[del_index - del_count]
            del Y[del_index - del_count]
            del Z[del_index - del_count]

            del_count += 1




        print(len(Alpha))

        #X, Y, Z, はfloatかarray-like、　カラーcはarray-likeなもの、つまりリストとかがいい。
        #リストとかではなく、単一の値を、for文を使って一つずつ当てはめていく方法は上手くいかない。
        #たぶん scatter3Dの文が一回しか使えないのか？最初の一回目の実行しか適用されてなかった。
        sc = ax1.scatter3D(X, Y, Z , c = Alpha, s = 3, cmap = 'binary',alpha = 0.3, vmin= 0, vmax=100)
        sc2 = ax2.scatter3D(X, Y, Z , c = Alpha, cmap = 'binary',alpha = 0.3, vmin= 0, vmax=100)
        fig.colorbar(sc)
        fig.colorbar(sc2)

        plt.tight_layout()

        plt.show()


    def Auto_Pollutions_Create(self, number, max_pollution):

        x = [self.__field_size + 1 for i in range(number)]
        y = [self.__field_size + 1 for i in range(number)]
        z = [self.__field_size + 1 for i in range(number)]
        pollution_density = [1.1 for i in range(number)]
        radius = [0.0 for i in range(number)]


        for count in range(number):
            while(self.__field_size < x[count]):
                x[count] = random.random() * 100 + random.random() * 10
            while(self.__field_size < y[count]):
                y[count] = random.random() * 100 + random.random() * 10
            while(self.__field_size < z[count]):
                z[count] = random.random() * 100 + random.random() * 10
            while(max_pollution < pollution_density[count]):
                pollution_density[count] = random.random() * 100 + random.random() * 10
            while(0 == radius[count] or (self.__field_size / 2) < radius[count]):
                radius[count] = random.random() * 100 + random.random() * 10


            self.create_local_pollution(int(x[count]), int(y[count]), int(z[count]), int(radius[count]), pollution_density[count])




    def Adjust_Pollution(self, upper_limit, lower_limit):

    #モード = Trueなら除算により、全ての濃度値(濃度値リストの全ての値)を一定の値で割る
        max_base_pollution = max(chain(*chain(*self.__base_pollution_list)))
        print('max_base_pollution = ' + str(max_base_pollution))
        division_ratio = max_base_pollution / upper_limit
        print(division_ratio)
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
                    self.__base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] / division_ratio



    def get_all_pollution_states(self):
        return self.__base_pollution_list
##################  end definition class Create_Density #####################################


######################## main ###########################################
def main():
    pollution_state = Create_Density(50)



    pollution_state.Auto_Pollutions_Create(5, 100)
#    pollution_state.create_local_pollution(10,10,10,5,100)
#    pollution_state.create_local_pollution(10,10,40,5,100)
    pollution_state.Adjust_Pollution(100, 0)
    pollution_state.create_random_pollution(1, 0, 0, 0, 50, 50, 50, 90, 1)


    pollution_state.draw_pollution_map()

####################### main ############################################

if __name__ == "__main__":
    main()
