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


    def get_no_noise_max_pollution_point(self):

        no_noise_base_pollution_list = [[[0.0 for j in range(self.__field_size)] for l in range(self.__field_size)] for k in range(self.__field_size)]

        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
                    no_noise_base_pollution_list[x_count][y_count][z_count] = self.__base_pollution_list[x_count][y_count][z_count] - self.__list_random_pollution[x_count][y_count][z_count]

        #selfを付けないと、クラス内でも関数内ローカル変数を定義することが出来る
        no_noise_x_max = 0
        no_noise_y_max = 0
        no_noise_z_max = 0


        #アスタリスクの作用について検証
        max_no_noise_pollution = max(chain(*chain(*no_noise_base_pollution_list)))
        print(chain(*chain(*no_noise_base_pollution_list)))


        print('max_no_noise_pollution' + str(max_no_noise_pollution))

        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                for z_count in range(self.__field_size):
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
            if(Alpha[index_count] < 80): #指定した濃度値より低い場合は、その要素と、対応する座標を削除する
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
        sc = ax1.scatter3D(X, Y, Z , c = Alpha, s = 0.1, cmap = 'binary',alpha = 0.3, vmin= 0, vmax=100)
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
                print("Func DM latest max = " + str(max_density))
        #次に探索する場所は今より、1進んだ場所なので探索する長さを伸ばす
        search_vector_length += 1

    #この関数の実行を行った結果、見つかった最高濃度値の座標を散布図に緑色の点で表示する。
    #ただし、測定不可域に入り、関数の処理がreturnにより終了した場合は、最高濃度値・座標は散布図に表示されない。
    print("Func DM max_pollution = " + str(max_density))
    print("----------------------------------------------------------")
    return x_max, y_max, z_max, max_density







def Detect_Square_Area_Max(pollution_list, x_now, y_now, z_now, search_deepness):


    x_max = 0
    y_max = 0
    z_max = 0
    max_value = 0




############## Function Update_Max #####################################
    def Update_Max(pollution_list, x, y, z, noise_threshold):
        nonlocal x_max
        nonlocal y_max
        nonlocal z_max
        nonlocal max_value
        if max_value < pollution_list[measure_x + x_1][measure_y + y_1][measure_z + z_1]:
            if(Distinguish_Noise_Pollution(pollution_list, x, y, z, noise_search_deepness, noise_threshold)):
                pass
            else:
                x_max = x
                y_max = y
                z_max = z
                max_value = pollution_list[x][y][z]

        return x_max, y_max, z_max, max_value

    x_now = abs(x_now)
    y_now = abs(y_now)
    z_now = abs(z_now)


    measure_x = x_now - search_deepness / 2
    measure_y = y_now - search_deepness / 2
    measure_z = z_now - search_deepness / 2

    #小数点以下切り捨て
    measure_x = math.ceil(measure_x)
    measure_y = math.ceil(measure_y)
    measure_z = math.ceil(measure_z)



    array_limit = np.array(pollution_list)
    x_limit, y_limit, z_limit = array_limit.shape

    print("z_limit = " + str(z_limit))

    for x_1 in range(search_deepness):
        for y_1 in range(search_deepness):
            for z_1 in range(search_deepness):
                if(0 < (measure_x + x_1) and 0 < (measure_y + y_1) and 0 < (measure_z + z_1)):
                    if((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
                        Update_Max(pollution_list, measure_x + x_1, measure_y + y_1, measure_z + z_1, noise_threshold)
                    elif((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and z_limit < (measure_z + z_1)):
                        Update_Max(pollution_list, measure_x + x_1, measure_y + y_1, measure_z + z_1 - (measure_z + z_1 - z_limit),  noise_threshold)
                    elif((measure_x + x_1) < x_limit and y_limit < (measure_y + y_1) and (measure_z + z_1) < z_limit):
                        Update_Max(pollution_list, measure_x + x_1, measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1,  noise_threshold)
                    elif((measure_x + x_1) < x_limit and y_limit < (measure_y + y_1) and z_limit < (measure_z + z_1)):
                        Update_Max(pollution_list, measure_x + x_1, measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1 - (measure_z + z_1 - z_limit), nnoise_threshold)
                    elif(x_limit < (measure_x + x_1) and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
                        Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1, measure_z + z_1, noise_threshold)
                    elif(x_limit < (measure_x + x_1) and (measure_y + y_1) < y_limit and z_limit < (measure_z + z_1)):
                        Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1, measure_z + z_1 - (measure_z + z_1 - z_limit),  noise_threshold)
                    elif(x_limit < (measure_x + x_1) and y_limit  < (measure_y + y_1)  and (measure_z + z_1) < z_limit):
                        Update_Max(pollution_list, measure_x + x_1 - (measure_x + x_1 - x_limit), measure_y + y_1 - (measure_y + y_1 - y_limit), measure_z + z_1,noise_threshold)
#[measure_y + y_1 - (measure_y + y_1 - y_limit)]
                    elif((measure_x + x_1) < x_limit and (measure_y + y_1) < y_limit and (measure_z + z_1) < z_limit):
                        break

                else:
                    pass

    return x_max, y_max, z_max, max_value







######################## main ###########################################
def main():
    pollution_state = Create_Density(50)



    pollution_state.Auto_Pollutions_Create(5, 100)
#    pollution_state.create_local_pollution(10,10,10,5,100)
#    pollution_state.create_local_pollution(10,10,40,5,100)
    pollution_state.Adjust_Pollution(100, 0)
    pollution_state.create_random_pollution(15, 0, 0, 0, 50, 50, 50, 100, 1)
    no_noise_x_max, no_noise_y_max, no_noise_z_max, max_pollution = pollution_state.get_no_noise_max_pollution_point()
    print("no_noise_x_max = " + str(no_noise_x_max))
    print("no_noise_y_max = " + str(no_noise_y_max))
    print("no_noise_z_max = " + str(no_noise_z_max))
    print("max_pollution = " + str(max_pollution))

    pollution_list = pollution_state.get_all_pollution_states()
    x,y,z,pollute = Detect_Square_Area_Max(pollution_list, 0, 0, 0, 100)
    print("square_area_max_x = " + str(x))
    print("square_area_max_y = " + str(y))
    print("square_area_max_z = " + str(z))
    print("square_area_max_pollution = " + str(pollute))

    Detect_Max(pollution_list, 1, 1, 1, 45, 45, 50)

    pollution_state.draw_pollution_map()

    Calculate_Degree(0, 0, 0, 10, 10, 14.141414)

####################### main ############################################

if __name__ == "__main__":
    main()
