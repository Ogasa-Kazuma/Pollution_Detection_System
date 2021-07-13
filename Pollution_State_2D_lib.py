############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
from itertools import chain
############################################################################


####################### start definition class Create_Density ############################
class Pollution_State_2D:

    def __init__(self,measurement_distance,field_size):
        #インスタンス変数も privateにできる
        self.__measurement_distance = measurement_distance
        self.__field_size = field_size
        #x座標の数　→　y方向の数　→　テンソル方向の数
        self.__base_pollution_list = [[[0.0 for i in range(1)] for j in range(field_size)] for l in range(field_size)]
        #この文がなければfloatでもNoneでもないらしい。とりあえずはリストに要素を代入しろということかな？

        self.__list_local_pollution = [[[0.0 for i in range(1)] for j in range(field_size)] for l in range(field_size)]
        self.__list_random_pollution = [[[0.0 for i in range(1)] for j in range(field_size)] for l in range(field_size)]
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                self.__base_pollution_list[x_count][y_count] = 0.0
                self.__list_local_pollution[x_count][y_count] = 0.0
                self.__list_random_pollution[x_count][y_count] = 0.0

    def create_local_pollution(self, x_center, y_center, scope_radius, max_pollution_density):


        #移動距離に対する濃度の減少量
        self.__pollution_decreasing_step = max_pollution_density / scope_radius


        for x_count in range(x_center - scope_radius, x_center + scope_radius, 1):
            for y_count in range(y_center - scope_radius, y_center + scope_radius, 1):
                if(0 <= x_count and 0 <= y_count and x_count < self.__field_size and y_count < self.__field_size):

                    self.__list_local_pollution[x_count][y_count] = max_pollution_density - self.__pollution_decreasing_step * np.sqrt(abs(x_center - x_count) ** (2) + abs(y_center - y_count) ** (2))
                    if(self.__list_local_pollution[x_count][y_count] < 0):
                        self.__list_local_pollution[x_count][y_count] = 0
                    self.__base_pollution_list[x_count][y_count] = self.__base_pollution_list[x_count][y_count] + self.__list_local_pollution[x_count][y_count]

        ret_list_local_pollution = self.__list_local_pollution
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                self.__list_local_pollution[x_count][y_count] = 0.0

                return ret_list_local_pollution




    def draw_pollution_map(self, row, column, graph_number):
        plt.subplot(row,column,graph_number)
        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                plt.scatter(x_count, y_count,c = "red", alpha = self.__base_pollution_list[x_count][y_count], linewidth = 0)


    def create_random_pollution(self, probability, start_x, start_y, end_x, end_y, upper_limit, lower_limit):

        for x_count in range(end_x - start_x):
            for y_count in range(end_y - start_y):
                if((100 - probability) <= random.random() * 100):
                    ram = 0
                    while(ram < lower_limit or upper_limit < ram):
                        ram = random.random()

                    self.__list_random_pollution[x_count][y_count] = ram
                    self.__base_pollution_list[x_count][y_count] = self.__list_random_pollution[x_count][y_count]
                else:
                    self.__list_random_pollution[x_count][y_count] = 0



        return self.__list_random_pollution


    def Adjust_Pollution(self, mode, upper_limit, lower_limit):
    #モード = Falseなら、上限1、下限0の濃度値に調整を行う(切り捨てなど)
        if(not mode):
            for x_count in range(self.__field_size):
                for y_count in range(self.__field_size):
                    if(self.__base_pollution_list[x_count][y_count] < lower_limit):
                        self.__base_pollution_list[x_count][y_count] = lower_limit
                    elif(upper_limit < self.__base_pollution_list[x_count][y_count]):
                        self.__base_pollution_list[x_count][y_count] = upper_limit
        else:
        #モード = Trueなら除算により、全ての濃度値(濃度値リストの全ての値)を一定の値で割る


            max_base_pollution = max(chain(*self.__base_pollution_list)) #多次元リストをフラットなリストに変更する。ここミスってmax(max(list))とかにすると大惨事
            #max_base_pollution = max(max(li) for li in self.__base_pollution_list)
            #max_base_pollution = (max(max(self.__base_pollution_list)))
            print('max_base_pollution = ' + str(max_base_pollution))
            division_ratio = max_base_pollution / upper_limit
            print(division_ratio)
            for x_count in range(self.__field_size):
                for y_count in range(self.__field_size):
                    self.__base_pollution_list[x_count][y_count] = self.__base_pollution_list[x_count][y_count] / division_ratio



    def Auto_Pollutions_Create(self, number, max_pollution):

        x = [self.__field_size + 1 for i in range(number)]
        y = [self.__field_size + 1 for i in range(number)]
        pollution_density = [1.1 for i in range(number)]
        radius = [0.0 for i in range(number)]


        for count in range(number):
            while(self.__field_size < x[count]):
                x[count] = random.random() * 100 + random.random() * 10
            while(self.__field_size < y[count]):
                y[count] = random.random() * 100 + random.random() * 10
            while(max_pollution < pollution_density[count]):
                pollution_density[count] = random.random() + random.random() * 0.1
            while(0 == radius[count] or (self.__field_size / 2) < radius[count]):
                radius[count] = random.random() * 100 + random.random() * 10


            self.create_local_pollution(int(x[count]), int(y[count]), int(radius[count]), pollution_density[count])



    def get_no_noise_max_pollution_point(self):

        no_noise_base_pollution_list = [[[0.0 for i in range(1)] for j in range(self.__field_size)] for l in range(self.__field_size)]



        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                no_noise_base_pollution_list[x_count][y_count] = self.__base_pollution_list[x_count][y_count] - self.__list_random_pollution[x_count][y_count]

        #selfを付けないと、クラス内でも関数内ローカル変数を定義することが出来る
        no_noise_x_max = 0
        no_noise_y_max = 0



        #test_list = np.ravel(no_noise_base_pollution_list)

        #print(sorted(test_list))
        max_no_noise_pollution = max(chain(*no_noise_base_pollution_list))
        print(chain(*no_noise_base_pollution_list))
        #max_no_noise_pollution = max(max(no_noise_base_pollution_list))
        print('max_no_noise_pollution' + str(max_no_noise_pollution))
        #print('opfkepowk' + str(sorted(test_list)[-1]))
        #print(max(test_list))



        for x_count in range(self.__field_size):
            for y_count in range(self.__field_size):
                if(max_no_noise_pollution == no_noise_base_pollution_list[x_count][y_count]):
                    no_noise_x_max = x_count
                    no_noise_y_max = y_count

        return no_noise_x_max, no_noise_y_max, no_noise_base_pollution_list[no_noise_x_max][no_noise_y_max]


    def get_all_pollution_states(self):
        return self.__base_pollution_list
##################  end definition class Create_Density #####################################


state = Pollution_State_2D(20, 50)
state.draw_pollution_map(2, 2, 1)
