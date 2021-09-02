

############################## ライブラリ  #####################################
import numpy as np
import matplotlib.pyplot as plt
import random
import math
from mpl_toolkits.mplot3d.axes3d import Axes3D
from itertools import chain
import collections
###############################################################################



def ConvertListElementsToInt(list):

    array = np.array(list)
    if(not(array.ndim == 1)):
        print("This Function can multi dimension list, list must be only dimension")
        return
    else:
        for i in range(len(list)):
            list[i] = int(list[i])

    return list


def IsAllElementsEqual(collection):
    #TODO リスト以外のデータが引数として渡されたらどうするか考える
    #引数のデータ群（リストなど）の次元数を調べる
    array = np.array(collection)
    dimensionNumber = array.ndim

    #多次元のデータ群を1次元のリストに変換
    for i in range(dimensionNumber - 1):
        collection = list(chain(*collection))

    #先頭要素と比較し要素の変化があるか調べる
    for j in range(len(collection)):
        isUnchanged = (collection[j] == collection[0])
        if(isUnchanged):
            pass
        else:
            return False

    #要素の変化が無い = 全ての要素が同じ
    return True

#リストの次元数を求める
def DeriveListDimension(collection):
    #データ群をnumpy配列に変換したあとshape関数で次元数を求める。
    #FIXME なぜ空のリストをarrayに変換するとそのarrayの次元数は1になるのか
    arrayedCollection = np.array(collection)
    dimensionNumber = arrayedCollection.ndim
    return dimensionNumber

def MakeListOfAllTheSameElements(length, element):
    if(not type(length) == int):
        raise TypeError("make the list All of the same elements, specify length by int type variable ")

    sameElementsCollection = list()
    for i in range(length):
        sameElementsCollection.append(element)

    return sameElementsCollection



def AppendListIntoList(acceptanceList , ListToAdd):
    #リストの中にリストを追加する（2次元リストにする)
    acceptanceList.append(ListToAdd)
    return acceptanceList


#既存の1次元リストの末尾に要素を追加していく
def AppendNewElementsToList(listToAdd, collectionOfNewElements):
    #todo listToAddって名前直す。受け入れさきと追加される側が逆
    #追加先のリストと追加したい要素群リストの次元数が両方とも1でないならリストへの要素追加は行わない。
    isOneDimension = DeriveListDimension(listToAdd) == 1 and DeriveListDimension(collectionOfNewElements) == 1

    if(not isOneDimension):
        print("Error Function AppendNewElementToList")
        print("The both Two lists dimension is must 1 dimension ")
        return

    #リストに要素を追加
    for i in range(len(collectionOfNewElements)):
        listToAdd.append(collectionOfNewElements[i])

    return listToAdd

def DeriveListElementsCount(collection):
    #リストのそれぞれの次元の要素数を求める
    arrayedCollection = np.array(collection)
    return arrayedCollection.shape


def CropList(collection, xPositions, yPositions, zPositions):

    #切り抜きを行うリストの次元数の判別
    isTwoDimension = DeriveListDimension(collection) == 2
    isThreeDimension = DeriveListDimension(collection) == 3

    #2次元リストの場合
    if(isTwoDimension):
        #TODOどっちがiでどっちがjなのかわからない、
        collection_j, collection_i = DeriveListElementsCount(collection)
        croppedList = [[0 for i in range(collection_i)] for j in range(collection_j)]

        #切り抜きを行う
        for k in xPositions:
            for l in yPositions:
                croppedList[k][l] = collection[k][l]

        return croppedList

    #3次元リストの場合
    if(isThreeDimension):
        collection_o, collection_n, collection_m = DeriveListElementsCount(collection)

        croppedList = [[[0 for m in range(collection_m)] for n in range(collection_n)] for o in range(collection_o)]

        #切り抜き
        for p in xPositions:
            for q in yPositions:
                for r in zPositions:
                    croppedList[p][q][r] = collection[p][q][k]

        return croppedList

    #リストの次元か2か3以外である場合、エラーを返す。
    print("Error Function CropList can process 2 or 3 dimensional list.")
    return




def CalculateEulerAngles(points1, points2):
    #リストの要素が3次元でなければエラー
    isThreeDimension = DeriveListDimension(points1) == 3 and DeriveListDimension(points2) == 3
    if(not isThreeDimension):
        print("Error To Calculate euler angle, the function requires 2 dimensional lists")
        return

    xOfPoints1 = points1[0]
    yOfPoints1 = points1[1]
    zOfPoints1 = points1[2]

    xOfPoints2 = points2[0]
    yOfPoints2 = points2[1]
    zOfPoints2 = points2[2]

    #ロール　yz ピッチ xz ヨ― xy
    roll = CalculateTwoDimensionalAngle(yOfPoints2, yOfPoints1, zOfPoints2, zOfPoints1)
    pitch = CalculateTwoDimensionalAngle(xOfPoints2, xOfPoints1, zOfPoints2, zOfPoints1)
    yaw = CalculateTwoDimensionalAngle(xOfPoints2, xOfPoints1, yOfPoints2, yOfPoints1)

    return roll, pitch, yaw



def CalculateTwoDimensionalAngle(point1, referenceOfpoint1, point2, referenceOfpoint2):
    #referenceを基準点0とした時の座標から2点間の角度を求める
    #point1がx座標, point2がy座標である
    angle = math.degrees(math.atan2((point1 - referenceOfpoint1) , (point2 - referenceOfpoint2)))

    return angle


def ConvertSingleElementsToList(*elements):

    #引数の数 = つくるリストの要素数
    collection = list()
    for i in range(len(elements)):
        collection.append(elements[i])

    return collection
