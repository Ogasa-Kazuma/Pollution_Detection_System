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
importlib.reload(Process_Visualizer)

importlib.reload(Data_Recorder)
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
## 濃度分布の作成に、確率的な偏りがある。座標の数字が大きいところに高濃度というか汚染源ができやすい


################ todo 9/2 #############################
## 特定のz座標だけを切り出して3d濃度をみれるようにする
## 初期座標を定める関数を実装する
## 目標濃度値に達していなかったらランダムで全く別の場所に移動して探索する方法を考える
##
##
###
##


#円形探索においての半径radiusの定め方を設定
def FunctionToSpecifyRadius(parameter):
    if(parameter <= 0):
        return parameter + 5

    elif(parameter > 0):
        return parameter * 20



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

def CreateDirectoryToDataLog():
    dt = datetime.datetime.now()
    new_dir_path_recursive = "DataLog/" + str(dt.year) + str("年") + str("/") + \
    str(dt.month) + "月/" + str(dt.day) + "日/" + str(dt.hour) + "時/" + str(dt.minute) + "分/" + str(dt.second) + "秒/"

    if(os.path.isdir(new_dir_path_recursive)):
        pass
    else:
        os.makedirs(new_dir_path_recursive)

    return new_dir_path_recursive


def NameFile():
    dt = datetime.datetime.now()

    pathName = str(dt.year) + str("_") + str(dt.month) + str("_") + str(dt.day) +str("_") + \
    str(dt.hour) + str(dt.minute) + str("_") + str(dt.second)

    return pathName


#todo 名前直す
def CreateNameFromDatetime():
    #現在の時間を表す情報を取得
    dt = datetime.datetime.now()
    #時間から秒数までの数字をただ羅列しただけの名前を作成
    name = str(dt.year) + str(dt.month) + str(dt.day)  +  \
    str(dt.hour) + str(dt.minute) + str(dt.second)

    return name



######################## main ###########################################
def main():

    #汚染源作成用パラメータ
    numberOfPollutions = 500 #生成する汚染源の個数
    maxRadiusOfPollution = 10 #汚染源の、汚染が影響する範囲の半径
    max_pollution = 100 #濃度最大値
    min_pollution = 0

    #maxRadius = 20, searchAngleRange = 120で成功率100
    #探索パラメータ
    maxRadius = 200  #探索最大半径
    searchAngleRange = 120 #2以上じゃないとエラー
    radiusToDecideStartMoving2D = 20   #10以上で成功率高い #todo 変数名直す　2Dで最初に動く方向を定めるための探索半径
    targetConcentration = 85

    #仮想フィールドのサイズ
    field_x_length = 100
    field_y_length = 20
    field_z_length = 20

    pathLocationToSave = CreateDirectoryToDataLog()

    #パラメータを変えるごとに、誤差の平均値がどうなるか保存するためのリスト
    meansOfErrorsX = list()
    meansOfErrorsY = list()
    meansOfErrorsZ = list()
    meansOfErrorsPollution = list()

    #処理回数（ループ回数）に影響を与える変数
    numberOfSearches = 5 #3Dフィールド上を何回探索するか
    countOfLoop = 3 #汚染状態作成、探索、保存の一連の処理を行う回数（つまりこのメインプログラムの実行回数)
    testParameterValues = [5, 30, 100, 200, 350, 500] #探索最大半径などのパラメータを変化させて実験するときどのような値とするか設定

    for radiusToDecideStartMoving2D in testParameterValues:
        #データ保存用リスト

        errorsList = list()

        for i in range(countOfLoop):

            ###########################################################
            ##汚染状態の作成
            #############################################################



            pollutionCreater3D = \
            Pollution_Creater3D.PollutionCreater3D(field_x_length, field_y_length, field_z_length)

            #3D濃度分布の作成
            pollutionCreater3D.CreateRandomPollutions(numberOfPollutions, xRange = [0, field_x_length - 1], \
            yRange = [0, field_y_length - 1], zRange = [0, field_z_length - 1], \
            rangeOfPollutionRadius = [2, maxRadiusOfPollution], pollutionRange = [0, maxRadiusOfPollution]) #numberは作る濃度の個数
            #pollution_creater_3D.create_local_pollution(20, 20, 20, 20, 100)
            pollutionCreater3D.AdjustPollutionRange(100, 0)

            #作成した3D濃度分布を取得
            pollutions3D = pollutionCreater3D.getPollutions()

            #濃度分布はリストではなくNumpy配列に変換
            pollutions3D = np.array(pollutions3D, dtype = "float64")


            #ノイズなしの場合の濃度最高値と、濃度最高値を示す座標を表示
            xOfTrueMax, yOfTrueMax, zOfTrueMax, trueMaxConcentration = pollutionCreater3D.get_no_noise_max_pollution_point()


            ############################################################
            ## 探索開始
            #############################################################


            pollution_searcher = class_pollution_searcher.PollutionSearcher()
            pollution_searcher.setRadiusToDecideStartMoving2D(radiusToDecideStartMoving2D)

            xOfMax, yOfMax, zOfMax, maxConcentration, isSuccess3DSearching = \
            pollution_searcher.SearchTargetPollutionConcentration(pollutions3D, targetConcentration, DecideStartPositions3D, \
            FunctionToSpecifyRadius, maxRadius, searchAngleRange, numberOfSearches)



            ###################################
            ##データ保存
            ###################################
            dataRecorder = Data_Recorder.DataRecorder("C:/Users/Kazuma/Documents/AS1/研究/Python/git_repository/Pollution_Detection_System/")

            xToSave, yToSave, zToSave, pollutionsToSave = common3d.MatchCorrespondenceOfEachCoordinate(pollutions3D)

            errors = [(xOfTrueMax - xOfMax), (yOfTrueMax - yOfMax), \
            (zOfTrueMax - zOfMax), (trueMaxConcentration - maxConcentration)]

            indexes = ["成功/失敗", "", "探索経路全長", "探索経路円弧長", "円弧半径による経路全長", "", \
            "x誤差", "y誤差" , "z誤差", "濃度誤差", \
            "汚染源数", "汚染源最大半径", "最高濃度", "最低濃度", "最高x", "最高y", "最高z", "", \
            "maxRadius", "searchAngleRange", "2D初期方向用半径", "目標濃度値", "探索回数", "",  \
            "探索x", "探索y", "探索z", "探索pollution", "", "フィールドx長さ", "フィールドy長さ", "フィールドz長さ", \
            "x", "y", "z", "pollution"]

            elementsToSave = [isSuccess3DSearching, None, pollution_searcher.CalculateSearchingLoadLength(), \
            sum(pollution_searcher.getLogOfRadius()), \
            sum(pollution_searcher.getLogOfArcOverallLength()), None, errors[0], \
            errors[1], errors[2], errors[3], \
            numberOfPollutions, maxRadiusOfPollution, \
            max_pollution, min_pollution, \
            xOfTrueMax, yOfTrueMax, zOfTrueMax, None, maxRadius, searchAngleRange, radiusToDecideStartMoving2D, \
            targetConcentration, numberOfSearches, None, xOfMax, yOfMax, zOfMax, maxConcentration, None, field_x_length, \
            field_y_length, field_z_length, xToSave, \
            yToSave, zToSave, pollutionsToSave]


            pollution_searcher.ClearHistoryOfSearchedLoad()

            dataRecorder.Record(indexes, elementsToSave)


            dataRecorder.SaveAsPickle(pathLocationToSave + NameFile())
            

            dataRecorder.DropAll()

            #真の濃度最高点との誤差をリストに保存
            errorsList.append(errors)



            ###################### forループ　終了 ######################################################

        #真の濃度最高点との誤差について平均を取る
        #todo 関数名直す
        errorsAve = common.CalculateAbsoluteAveOfErrors(errorsList)

        indexesOfResultSummary = ["変更パラメータ", "xの差", "yの差", "zの差", "濃度差", "x誤差平均", "y誤差平均", "z誤差平均", "濃度差平均"]
        valuesOfResultSummary = ["maxRadius", errors[0], errors[1], errors[2], errors[3], \
        errorsAve[0], errorsAve[1], errorsAve[2], errorsAve[3]]
        dataRecorder.Record(indexesOfResultSummary, valuesOfResultSummary)
        dataRecorder.SaveAsPickle(pathLocationToSave + "summary_of_result" + "_" + NameFile())
        dataRecorder.DropAll()


        #パラメータを変えるごとの、真の濃度最高点との誤差についての平均を保存

        meansOfErrorsX.append(errorsAve[0])
        meansOfErrorsY.append(errorsAve[1])
        meansOfErrorsZ.append(errorsAve[2])
        meansOfErrorsPollution.append(errorsAve[3])

        ####################　外側forループ終了 ########################################

    #結果の総括（全体の処理結果のまとめ）。上記までのプログラムにより何度も探索が行われたが、その結果の総括。
    indexesOfResultSummary = ["変更パラメータ名", "パラメータ値", "x誤差平均", "y誤差平均", "z誤差平均", "濃度誤差平均"]
    valuesOfResultSummary = ["2D初期方向決定用探索半径", testParameterValues, meansOfErrorsX, \
    meansOfErrorsY, meansOfErrorsZ, meansOfErrorsPollution]
    dataRecorder.Record(indexesOfResultSummary, valuesOfResultSummary)
    dataRecorder.SaveAsPickle(pathLocationToSave + "summary_of_result" + CreateNameFromDatetime())

    #パラメータと、結果の関係を折れ線グラフに表示
    plt.plot(testParameterValues, meansOfErrorsX, c = "red")
    plt.plot(testParameterValues, meansOfErrorsY, c = "blue")
    plt.plot(testParameterValues, meansOfErrorsZ, c = "green")
    plt.plot(testParameterValues, meansOfErrorsPollution, c = "orange")

    plt.show()



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
