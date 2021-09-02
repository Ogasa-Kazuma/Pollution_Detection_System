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
import Navigator_


import importlib
importlib.reload(common)
importlib.reload(class_dimension_converter)
importlib.reload(class_2D_pollution_state_creater)
importlib.reload(class_3D_pollution_state_creater)
importlib.reload(class_pollution_state_drawer_2D)
importlib.reload(class_pollution_state_drawer_3D)
importlib.reload(class_pollution_searcher)
importlib.reload(Process_Visualizer)
importlib.reload(Navigator_)
############################################################################


##################







#######################################################################
##### TODO リスト
####
# 1. xy平面状で「最初に進む方向を定める」関数をつくる櫃よう。今はとりあえず最初は45度方向に進むようになっている
# 2.ナビゲータークラス消す
# 探索者クラスの引数とか戻り値が、2Dと3Dが混在しててモヤモヤする（z座標が必要だったりそうじゃなかったり)
# ノイズ判定のあたり、xyz座標の探索可能域？の境界値
# 探索者クラスがあるのにわざわざメインで探索処理を記述するなああああああ！！！！！
# commonの、リストに新しい要素を加えるAppendNewElementsToListが、リスト & リストだけでなく
# リスト & 数値単体（要素単体？）でも使えるようにする
# z_to_delete_って変数名どうにかする
# figure_to_show_3d_pollutions_state って長すぎ
# 探索精度と探索時間を決めるのはmaxRadius、searchAngleRangeとRadiusの定め方の関数である
# SpecifyRadiusって名前を変える
# limitとかbeginとかstartあたりの変数名が気になる
#　インスタンス名、関数名、変数名のキャメル記法とかが統一されてない。
# mainの部分の、使ってないコメントとか処理とか消す
# create_random_pollutionまだ試してないけどたぶん上手く動かない
# figではなくaxesをコンストラクタに渡すようにする
#リストのコピー(deepcopyとか)についてちゃんと勉強する
#コメント足りてないモジュールにコメント足していく
##################################################






##########################################
##もともとの濃度リストのx座標とy座標を逆にしてたからいろいろ不安
## common のCropListの次元を逆に変更x y zがぐちゃぐちゃになってた？
##


################ todo 9/2 #############################
## 特定のz座標だけを切り出して3d濃度をみれるようにする
## 初期座標を定める関数を実装する
## 目標濃度値に達していなかったらランダムで全く別の場所に移動して探索する方法を考える
##
##
###
##


#円形探索においての半径radiusの定め方を設定
def SpecifyRadius(parameter):
    if(parameter <= 0):
        return parameter + 5

    elif(parameter > 0):
        return parameter * 4



def DecideStartPositions3D(pollutions):
    """ 3次元探索において、どの点から探索を開始するか決定する  """
    #要素数から1を引いたものが座標値の上限である
    maxX, maxY, maxZ = common.DeriveListElementsCount(pollutions)
    maxX = maxX - 1
    maxY = maxY - 1
    maxZ = maxZ - 1

    #ランダムな座標を生成したあとリストにまとめて返す
    xOfStart = random.randint(0, maxX)
    yOfStart = random.randint(0, maxY)
    zOfStart = random.randint(0, maxZ)

    beginPositions = common.ConvertSingleElementsToList(xOfStart, yOfStart, zOfStart)
    return beginPositions






######################## main ###########################################
def main():

    #インスタンス生成
    pollution_creater_3D = \
    class_3D_pollution_state_creater.Pollution_State_Creater_3D(field_x_length = 40, field_y_length = 50, field_z_length = 20)

    #3D濃度分布の作成
    pollution_creater_3D.Auto_Pollutions_Create(number = 200, max_pollution = 100, maxRadiusOfPollution = 30) #numberは作る濃度の個数
    pollution_creater_3D.Adjust_Pollution(upper_limit = 100, lower_limit = 0)

    #作成した3D濃度分布を取得
    pollutions3D = pollution_creater_3D.get_all_pollution_states()

    #ノイズなしの場合の濃度最高値と、濃度最高値を示す座標を表示
    x, y, z, maxConcentration = pollution_creater_3D.get_no_noise_max_pollution_point()
    print("ノイズなしx" + str(x))
    print("ノイズなしy" + str(y))
    print("ノイズなしz" + str(z))
    print("ノイズなし最高濃度値" + str(maxConcentration))


    #濃度分布の描画
    figure_to_show_3d_pollutions_state = plt.figure()
    drawing_area_of_3d_all_pollutions_states = 121
    pollution_state_drawer_3D = class_pollution_state_drawer_3D.Pollution_State_Drawer_3D(figure_to_show_3d_pollutions_state, drawing_area_of_3d_all_pollutions_states)
    pollution_state_drawer_3D.draw_pollution_map(pollutions3D, concentration_limit_to_display = 5)







    #得られた切り抜き濃度リストを2次元リストに変換
    dimension_converter = class_dimension_converter.Dimension_Converter(pollutions3D)
    #zBegin の値と同じ
    convertedPollutions = dimension_converter.Convert_Dimension(z_point_to_delete = 19, upper_limit_3D = 100, lower_limit_3D = 0, \
    upper_limit_2D = 1, lower_limit_2D = 0)

    #2次元に変換した切り抜き濃度リストを描画
    fig2d = plt.figure()
    drawingArea2d221 = 221
    pollution_state_drawer_2D_area111 = class_pollution_state_drawer_2D.Pollution_State_Drawer_2D(fig2d, drawingArea2d221)
    pollution_state_drawer_2D_area111.draw_pollution_map(convertedPollutions)

    drawingArea2d222 = 222
    #探索した点を描画
    processVisualizer = Process_Visualizer.ProcessVisualizer(fig2d, drawingArea2d222)
    processVisualizer.setColorOfPlotPoint("orange")
    #processVisualizer.DrawSearchedPoints(searchedX, searchedY)
    processVisualizer.setColorOfPlotPoint("red")
    #processVisualizer.DrawSearchedPoints(searchedX, searchedY)

    ############################################################
    ## 探索開始
    #############################################################

    #TODO 初期座標の定め方について考える

    #maxRadius = 20, searchAngleRange = 120で成功率100
    #探索パラメータ
    maxRadius = 20  #探索最大半径
    searchAngleRange = 120
    #2Dでの最初の進行方向の定め方および探索半径rasius
    #
    #
    #

    #初期点
    #いまはmain関数に記述しているがクラス内で初期点を定める関数などを実装する

    xOfStart = 0
    yOfStart = 0
    zOfStart = 0 #pollutions_converterのz_to_delete と同じ値にしなければ上手くいかない

    beginPositions = common.ConvertSingleElementsToList(xOfStart, yOfStart, zOfStart)

    pollution_searcher = class_pollution_searcher.PollutionSearcher()
    pollution_searcher.setRadiusToDecideStartMoving2D(8)


    xOfMax, yOfMax, zOfMax, maxConcentration = \
    pollution_searcher.SearchMaxPollutionOn3dField(pollutions3D, DecideStartPositions3D, \
    SpecifyRadius, maxRadius, searchAngleRange)

    print("探索結果")
    print("x = " + str(xOfMax))
    print("y = " + str(yOfMax))
    print("z = " + str(zOfMax))
    print("最高濃度値 = " + str(maxConcentration))

    print(pollution_searcher.getPathOfSearchedZ())






####################### main ############################################

if __name__ == "__main__":
    main()
