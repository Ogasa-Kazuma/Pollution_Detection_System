############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
from itertools import chain
from class_pollution_state_creater import Pollution_State_Creater
############################################################################


####################### start definition class Create_Density ############################
class Pollution_State_Creater_2D(Pollution_State_Creater):

    def __init__(self, field_x_length, field_y_length):
        #インスタンス変数も privateにできる

        self.__field_x_length = field_x_length
        self.__field_y_length = field_y_length
        #x座標の数　→　y方向の数　→　テンソル方向の数
        self.__base_pollution_list = [[j for j in range(field_x_length)] for l in range(field_y_length)]
        #この文がなければfloatでもNoneでもないらしい。とりあえずはリストに要素を代入しろということかな？

        self.__list_local_pollution = [[j for j in range(field_x_length)] for l in range(field_y_length)]
        self.__list_random_pollution = [[j for j in range(field_x_length)] for l in range(field_y_length)]
        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                self.__base_pollution_list[x_count][y_count] = 0.0
                self.__list_local_pollution[x_count][y_count] = 0.0
                self.__list_random_pollution[x_count][y_count] = 0.0

    def create_local_pollution(self, x_begin, y_begin, scope_radius, max_pollution_density):


        #移動距離に対する濃度の減少量
        self.__pollution_decreasing_step = max_pollution_density / scope_radius


        for x_count in range(x_begin - scope_radius, x_begin + scope_radius, 1):
            for y_count in range(y_begin - scope_radius, y_begin + scope_radius, 1):
                if(0 <= x_count and 0 <= y_count and x_count < self.__field_x_length and y_count < self.__field_y_length):

                    self.__list_local_pollution[x_count][y_count] = max_pollution_density - self.__pollution_decreasing_step * np.sqrt(abs(x_begin - x_count) ** (2) + abs(y_begin - y_count) ** (2))
                    if(self.__list_local_pollution[x_count][y_count] < 0):
                        self.__list_local_pollution[x_count][y_count] = 0
                    self.__base_pollution_list[x_count][y_count] = self.__base_pollution_list[x_count][y_count] + self.__list_local_pollution[x_count][y_count]

        ret_list_local_pollution = self.__list_local_pollution
        for x_count in range(self.__field_x_length):
            for y_count in range(self.__field_y_length):
                self.__list_local_pollution[x_count][y_count] = 0.0

                return ret_list_local_pollution



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
            for x_count in range(self.__field_x_length):
                for y_count in range(self.__field_y_length):
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
            for x_count in range(self.__field_x_length):
                for y_count in range(self.__field_y_length):
                    self.__base_pollution_list[x_count][y_count] = self.__base_pollution_list[x_count][y_count] / division_ratio



    def Auto_Pollutions_Create(self, number, max_pollution):

        x = [self.__field_x_length + 1 for i in range(number)]
        y = [self.__field_y_length + 1 for i in range(number)]
        pollution_density = [1.1 for i in range(number)]
        radius = [0.0 for i in range(number)]


        for count in range(number):
            while(self.__field_x_length < x[count]):
                x[count] = random.random() * 100 + random.random() * 10
            while(self.__field_y_length < y[count]):
                y[count] = random.random() * 100 + random.random() * 10
            while(max_pollution < pollution_density[count]):
                pollution_density[count] = random.random() + random.random() * 0.1
            while(0 == radius[count] or (self.__field_x_length / 2) < radius[count]):
                radius[count] = random.random() * 100 + random.random() * 10


            self.create_local_pollution(int(x[count]), int(y[count]), int(radius[count]), pollution_density[count])

    def get_all_pollution_states(self):
        return self.__base_pollution_list
##################  end definition class Create_Density #####################################

def main():
    field_x_length = 40
    field_y_length = 40

    state = Pollution_State_Creater_2D(field_x_length, field_y_length)
    x_begin = 20
    y_begin = 20
    scope_radius = 10
    max_pollution_density = 0.8
    state.create_local_pollution(x_begin, y_begin, scope_radius, max_pollution_density)

    print(state.get_all_pollution_states())

if __name__ == "__main__":
    main()
