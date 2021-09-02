
############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
import common
###############################################################################




def IsInSearchableArea(pollutions, xPosition, yPosition, zPosition):
    pollutions_converted_to_array = np.array(pollutions)
    max_x, max_y, max_z = pollutions_converted_to_array.shape
    max_x = max_x - 1
    max_y = max_y - 1
    max_z = max_z - 1
    for i in range(max_x):
        isInSearchableArea = \
        (xPosition >= 0) and (xPosition <= max_x) and (yPosition >= 0) and (yPosition <= max_y) and (zPosition >= 0) and (zPosition <= max_z)
        if(isInSearchableArea):
            return True
        else:
            return False


def isNoiseDetectedByCompareSurroundings(pollutions, xPosition, yPosition, zPosition, scopeOfSearch, noiseThreshold):

    use_array = np.array(pollutions)
    max_x, max_y, max_z = use_array.shape

    max_x = max_x - 1
    max_y = max_y - 1
    max_z = max_z - 1


    sum = 0
    scopeOfSearch = int(scopeOfSearch)
    xPosition = int(xPosition)
    yPosition = int(yPosition)
    zPosition = int(zPosition)

    #対象座標の周囲の濃度値の合計を求める
    for x_i in range(xPosition - scopeOfSearch, xPosition + scopeOfSearch, 1):
        for y_i in range(yPosition - scopeOfSearch, yPosition + scopeOfSearch, 1):
            for z_i in range(zPosition - scopeOfSearch, zPosition + scopeOfSearch, 1):
                #todo 変数名直す
                isXInSearchableArea = x_i <= max_x and x_i >= 0
                isYInSearchableArea = y_i <= max_y and y_i >= 0
                isZInSearchableArea = z_i <= max_z and z_i >= 0
                # x, y, zのうちいずれかが探索可能範囲外の場合、濃度合計値の更新は行わない。
                if(isXInSearchableArea and isYInSearchableArea and isZInSearchableArea):
                    sum += pollutions[x_i][y_i][z_i]
                else:
                    pass

    #濃度合計値を面積で割り、平均を算出
    ave = sum / ((1 + (2 * scopeOfSearch)) ** (2))

    #対象濃度値と周囲の平均濃度値の差が、しきい値を超えるなら、ノイズであると判定
    return pollutions[xPosition][yPosition][zPosition] - ave > noiseThreshold

def FindMaxConcentration(pollutions):
    dimension = common.DeriveListDimension(pollutions)
    if(not dimension == 3):
        print("Error common3d FindMaxConcentration requires 3 dimensional list only")
        return

    #リストを1次元に変換し最大濃度値を取り出す
    maxConcentration = max(chain(*chain(*pollutions)))

    return maxConcentration

def getElementCountZ(collection):
    #渡された濃度リストが3次元でなければエラー
    if(not common.DeriveListDimension(collection) == 3):
        print("this list is not 3D list, can't get element count of Z")
        return

    #Z方向の要素数のみを返す
    arrayedCollection = np.array(collection)
    x, y, zDimensionNumber = arrayedCollection.shape
    print("z dimension num" + str(zDimensionNumber))
    return zDimensionNumber

#todo 関数名変える
# x, y座標は固定で、z座標のみを変化させながら最高濃度値を探す
def FindMaxConcentrationOnZ(collection, fixedX, fixedY):
    #渡されたリストが3次元でなければエラー
    if(not common.DeriveListDimension(collection) == 3):
        print("FindMaxConcentrationOnZ requires 3D lists")
        return

    #最高濃度値を示すz座標を見つける
    indexOfMax = 0
    maxConcentration = 0
    for i in range(getElementCountZ(collection)):
        if(collection[fixedX][fixedY][i] > maxConcentration):
            indexOfMax = i
            maxConcentration = collection[fixedX][fixedY][i]

    return indexOfMax, maxConcentration
