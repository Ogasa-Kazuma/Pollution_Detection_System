
############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
import common_of_searcher
import common
import common3d
import importlib
importlib.reload(common_of_searcher)
importlib.reload(common)
importlib.reload(common3d)
######################################


def CalculateAllPositions(xBegin, yBegin, zBegin, radius, referenceAngle, searchAngleRange):

    #探索可能範囲を決定
    maxCanSearchAngle = referenceAngle + (searchAngleRange / 2)
    minCanSearchAngle = referenceAngle - (searchAngleRange / 2)

    searchingAngle = minCanSearchAngle
    angle_i = 0

    xPositions = list()
    yPositions = list()

    #探索範囲内の座標を全て計算
    while searchingAngle <= maxCanSearchAngle :

        xPositions.append(xBegin + radius * math.cos(math.radians(searchingAngle)))
        yPositions.append(yBegin + radius * math.sin(math.radians(searchingAngle)))
        searchingAngle += 1 #1ループごとに探索角度を1degreeずつUP

    return xPositions, yPositions



def ConvertPositionsToApproximatePositions(xPositions, yPositions):
    xPositionsAfterConverted = list()
    yPositionsAfterConverted = list()

    for i in range(len(xPositions)):
        xPositionsAfterConverted.append(round(xPositions[i]))

    for j in range(len(yPositions)):
        yPositionsAfterConverted.append(round(yPositions[j]))

    return xPositionsAfterConverted, yPositionsAfterConverted



def DeletePositionInUnsearchableArea(pollutions, xPositions, yPositions, zPoint):

    indexToDelete = list()

    #探索予定の座標のうち、探索不可領域を示す座標を抽出
    for i in range(len(xPositions)): #xとyの要素数は同じ
        if(common3d.IsInSearchableArea(pollutions, xPositions[i], yPositions[i], zPoint)):
            pass
        else:
            indexToDelete.append(i)

    #探索不可領域の座標を削除し、探索を行わないようにする
    CountOfIndexChange = 0  #要素を削除するたびにインデックス数が変わることを考慮
    for j in indexToDelete:
        del xPositions[j - CountOfIndexChange]
        del yPositions[j - CountOfIndexChange]
        CountOfIndexChange += 1

    return xPositions, yPositions



def DeleteNoise(pollutions, xPositions, yPositions, zPoint, scopeOfNoiseSearch, noiseThreshold):

    #ノイズだと判定すれば、ノイズ値を示す座標を削除
    #TODO 要素を削除するごとに要素数が変化することを考慮するように変更

    indexToDelete = list()

    for i in range(len(xPositions)):
        if(common3d.isNoiseDetectedByCompareSurroundings(pollutions, xPositions[i], yPositions[i], zPoint, scopeOfNoiseSearch, noiseThreshold)):
            indexToDelete.append(i)
        else:
            pass

    #ノイズと判定した濃度値を示す座標を削除し、探索を行わないようにする
    CountOfIndexChange = 0  #要素を削除するたびにインデックス数が変わることを考慮
    for j in indexToDelete:
        del xPositions[j - CountOfIndexChange]
        del yPositions[j - CountOfIndexChange]
        CountOfIndexChange += 1

    return xPositions, yPositions


def FindMaxConcentrationAndPosition(pollutions, xBegin, yBegin, zBegin, xPositions, yPositions, zPoint):

    #forループにfloat型を使えないのでintに変換
    xPositions = common.ConvertListElementsToInt(xPositions)
    yPositions = common.ConvertListElementsToInt(yPositions)

    concentrations = list()

    #探索する座標点のみの濃度値を抽出
    for i in xPositions:
        for j in yPositions:
            concentrations.append(pollutions[i][j][zPoint])




    #探索範囲の濃度値が全て同じであれば最大濃度値と座標が
    #分からないので関数の処理を終了
    if(common.IsAllElementsEqual(concentrations)):
        print("All of elements is equal, can't find max_concentration")
        return xBegin, yBegin, zBegin, pollutions[xBegin][yBegin][zBegin]

    xOfMax = 0
    yOfMax = 0
    zOfMax = zPoint


    #探索する範囲の最大濃度値を見つける
    maxConcentration = max(concentrations)

    #最大濃度値の座標を見つける
    for i in xPositions:
        for j in yPositions:
            #最大濃度値と一致する濃度リストの座標を求める
            if(pollutions[i][j][zPoint] == maxConcentration):
                xOfMax = i
                yOfMax = j
                zOfMax = zPoint
                return xOfMax, yOfMax, zOfMax, maxConcentration

    #最大濃度値の濃度値が見つからなかった場合、エラー出力
    print("Error Function FindMaxConcentrationAndPosition")
