
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
import copy
importlib.reload(common_of_searcher)
importlib.reload(common)
importlib.reload(common3d)
######################################33



class PollutionSearcher():

    def __init__(self):
        self.__noiseThreshold = 0.5 #デフォルトノイズ閾値
        self.__scopeOfNoiseSearch = 2 #デフォルトノイズ判定探索領域
        self.__pathOfSearchedX = list()
        self.__pathOfSearchedY = list()
        self.__pathOfSearchedZ = list()
        self.__maxPointOf2dFieldX = list()
        self.__maxPointOf2dFieldY = list()
        #todo 名前直す
        self.__centerPointsOfArcX = list()
        self.__centerPointsOfArcY = list()
        self.__centerPointsOfArcZ = list()

        self.__radiusToDecideStartMoving2D = 0







    def getPathOfSearchedX(self):
        return self.__pathOfSearchedX

    def getPathOfSearchedY(self):
        return self.__pathOfSearchedY

    def getPathOfSearchedZ(self):
        return self.__pathOfSearchedZ

    def getMaxPointOf2dFieldX(self):
        return self.__maxPointOf2dFieldX

    def getMaxPointOf2dFieldY(self):
        return self.__maxPointOf2dFieldY

    #todo　名前直す。連続する円弧状の濃度の探索の経路
    def getCenterPointsOfArcX(self):
        return self.__centerPointsOfArcX

    def getCenterPointsOfArcY(self):
        return self.__centerPointsOfArcY

    def setRadiusToDecideStartMoving2D(self, radius):
        self.__radiusToDecideStartMoving2D = radius


    def setNoiseThreshold(self, threshold):
        self.__noiseThreshold = threshold

    def setScopeOfNoiseSearch(self, scopeOfNoiseSearch):
        self.__scopeOfNoiseSearch = scopeOfNoiseSearch

    def DecideStartMovingDirection2D(self, pollutions, xBegin, yBegin, zBegin, radius, referenceAngle, searchAngleRange):
        #探索半径が1未満ならエラー
        if(radius < 1):
            raise ValueError("must set radius by setting function to decide start moving direction on 2d field ")
            print("must set radius by setting function to decide start moving direction on 2d field ")
            return

        xOfMax, yOfMax, _, _, = self.SearchMaxPollutionOnArc(pollutions, xBegin, yBegin, zBegin, \
        self.__radiusToDecideStartMoving2D, 0, 360)
        directionToNextMoving = common.CalculateTwoDimensionalAngle(xOfMax, xBegin, yOfMax, yBegin)
        return directionToNextMoving





    #円弧状の経路の最大濃度値を見つける関数
    def SearchMaxPollutionOnArc(self, pollutions, xBegin, yBegin, zBegin, radius, referenceAngle, searchAngleRange):
        #searchAngleRangeはreferenceAngleを基準とした角度
        #searchAngleRange = 60 とすれば、referenceAngleより左に30度、右に30度の範囲を探索する

        #探索する範囲と半径が1より小さければ関数の処理を終了（エラー出力)
        IsSearchable = (searchAngleRange >= 2) or (radius >= 1)
        if(not IsSearchable):
            print("too small SearchRange or too small SearchRadius")
            return

        #z座標が探索可能範囲外なら関数の処理を終了(エラー出力)
        pollutions_converted_to_array = np.array(pollutions)
        not_used, not_used, max_z = pollutions_converted_to_array.shape #z座標の探索限界範囲を取得

        IsSearchable = (zBegin >= 0) and (zBegin <= max_z)
        if(not IsSearchable):
            print("z Position is out of searchable area")
            return


        #1.探索する座標を計算 2.座標を最も近い整数値の座標に変換 3.探索可能範囲外の座標を削除
        #4.ノイズだと判断された座標を削除 5.最高濃度値と、最高濃度の座標を見つける
        xPositions, yPositions = common_of_searcher.CalculateAllPositions(xBegin, yBegin, zBegin, radius, referenceAngle, searchAngleRange)
        xPositions, yPositions = common_of_searcher.ConvertPositionsToApproximatePositions(xPositions, yPositions)
        xPositions, yPositions = common_of_searcher.DeletePositionInUnsearchableArea(pollutions, xPositions, yPositions, zBegin)
        xPositions, yPositions = common_of_searcher.DeleteNoise(pollutions, xPositions, yPositions, zBegin, self.__scopeOfNoiseSearch, self.__noiseThreshold)

        self.__pathOfSearchedX = common.AppendListIntoList(self.__pathOfSearchedX, xPositions)
        self.__pathOfSearchedY = common.AppendListIntoList(self.__pathOfSearchedY, yPositions)
        zPositions = common.MakeListOfAllTheSameElements(len(xPositions), zBegin) #x, y座標の数とz座標の数を合わせる（z座標は固定だがx、y座標と同じ数だけそんざい　する必要がある）
        self.__pathOfSearchedZ = common.AppendListIntoList(self.__pathOfSearchedZ, zPositions)

        xPosition, yPosition, zPosition, MaxConcentration = common_of_searcher.FindMaxConcentrationAndPosition(pollutions, xBegin, yBegin, zBegin, xPositions, yPositions, zBegin)
        return xPosition, yPosition, zPosition, MaxConcentration


    #todo 関数名直す
    #しきい値を超える濃度値と座標を探す関数
    def SearchThresholdPollutionOnContinuousArc(self, pollutions, beginPositions, Radius, max_radius, referenceAngle, searchAngleRange, threshold):

        #探索円の中心座標
        xBegin = beginPositions[0]
        yBegin = beginPositions[1]
        zBegin = beginPositions[2]

        #濃度リストの最大値。ループ終了条件
        #todo 変数名直す
        limitOfConcentration = common3d.FindMaxConcentration(pollutions)

        i = 0

        #探索深さradiusが限界値 max_radiusを超えたときか、濃度の限界値に達したときか、しきい値以上の濃度値を発見できたら関数の処理を終了
        while(1):
            #探索する半径が指定値以上なら処理を終了。濃度値と座標は更新せず返す
            isOut = Radius(i) > max_radius
            if(isOut):
                return xBegin, yBegin, zBegin, pollutions[xBegin][yBegin][zBegin]

            #しきい値を超える場所と濃度値を探索
            xOfMax, yOfMax, zOfMax, maxConcentration = \
            self.SearchMaxPollutionOnArc(pollutions, xBegin, yBegin, zBegin, Radius(i), referenceAngle, searchAngleRange)

            #目標とする濃度しきい値より高い値を検出できたら終了
            if(maxConcentration > threshold):
                self.__centerPointsOfArcX.append(xOfMax)
                self.__centerPointsOfArcY.append(yOfMax)
                # self.__pathOfSearchedX = common.AppendNewElementsToList(self.__pathOfSearchedX, xPositions)
                # self.__pathOfSearchedY = common.AppendNewElementsToList(self.__pathOfSearchedY, yPositions)
                return xOfMax, yOfMax, zOfMax, maxConcentration

            #濃度の限界値に達した場合も終了
            if(maxConcentration == limitOfConcentration):
                self.__centerPointsOfArcX.append(xOfMax)
                self.__centerPointsOfArcY.append(yOfMax)
                # self.__pathOfSearchedX = common.AppendNewElementsToList(self.__pathOfSearchedX, xPositions)
                # self.__pathOfSearchedY = common.AppendNewElementsToList(self.__pathOfSearchedY, yPositions)
                return xOfMax, yOfMax, zOfMax, maxConcentration


            i += 1



    def SearchMaxPollutionOn2dField(self, pollutions, beginPositions, FunctionToSpecifyRadius, maxRadius, searchAngleRange):

        # 1.どこを探索の初期点とするか定める 2.最初はまずどの方向に向かうか決定する
        # 3. 波経路探索開始。初期点の濃度よりも高い濃度が見つかる場所を探す
        # 4.xy座標を替えながら波経路探索を繰り返す

        #1. 探索開始点を定める
        xOfLastMax = beginPositions[0]  #探索初期点 x座標
        yOfLastMax = beginPositions[1]  #探索初期点　y座標
        zOfLastMax = beginPositions[2]  #探索初期点　z座標


        #2. 最初の移動方向を定める
        #xOfLastMax等はxBegin、つまり初期方向を定める探索の開始点の座標を示す
        #todo 引数の意味が分かりづらいのでなおす　
        directionToNextMoving = self.DecideStartMovingDirection2D(pollutions, xOfLastMax, yOfLastMax, zOfLastMax, \
        self.__radiusToDecideStartMoving2D, 0, 360) #360度全方位を探索するので基準角0で360回転


        #探索の途中経過を保存するための変数
        positionsOfMax = common.ConvertSingleElementsToList(xOfLastMax, yOfLastMax, zOfLastMax)
        xOfLastMax = positionsOfMax[0]
        yOfLastMax = positionsOfMax[1]
        lastMaxConcentration = pollutions[xOfLastMax][yOfLastMax][zOfLastMax]


        #4. xy座標を変えながら探索
        while(1):
            xOfMax, yOfMax, zOfMax, maxConcentration = \
            self.SearchThresholdPollutionOnContinuousArc(pollutions, positionsOfMax, \
            FunctionToSpecifyRadius, maxRadius, directionToNextMoving, searchAngleRange, threshold = lastMaxConcentration)

            #より高い濃度の場所が見つかる見込みがない場合、関数の処理を終了
            if(maxConcentration <= lastMaxConcentration):
                self.__maxPointOf2dFieldX.append(xOfLastMax)
                self.__maxPointOf2dFieldY.append(yOfLastMax)
                return xOfMax, yOfMax, zOfMax, maxConcentration

            #濃度限界値に達したら終了
            if(maxConcentration >= common3d.FindMaxConcentration(pollutions)):
                self.__maxPointOf2dFieldX.append(xOfMax)
                self.__maxPointOf2dFieldY.append(yOfMax)
                return xOfMax, yOfMax, zOfMax, maxConcentration

            #濃度値の更新があれば、次に進む方向やパラメータの更新

            #次に進むべき方向を定める
            directionToNextMoving = common.CalculateTwoDimensionalAngle(xOfMax, xOfLastMax, yOfMax, yOfLastMax)
            positionsOfMax = common.ConvertSingleElementsToList(xOfMax, yOfMax, zOfMax)
            xOfLastMax = xOfMax
            yOfLastMax = yOfMax
            lastMaxConcentration = maxConcentration


    def SearchMaxPollutionOn3dField(self, pollutions, DecideStartPositions3D, FunctionToSpecifyRadius, maxRadius, searchAngleRange):

        #1.スタート地点の座標を決定　2.2D平面上での最高濃度点を探す
        #3. 2で見つかった、最高濃度値を示す座標のうち、xとyは固定し、zだけを変化させる
        #最も高い濃度値を示すz座標を見つける
        #4.更新したx, y, z座標について2D平面上で最高濃度値を示す点を見つける
        #5. 2-4を繰り返す

        #最初の進行方向と座標を決定
        beginPositions = DecideStartPositions3D(pollutions)


        while(1):
            #2D平面上の探索を行う
            xOfMax, yOfMax, zOfMax, maxConcentration = \
            self.SearchMaxPollutionOn2dField(pollutions, beginPositions, FunctionToSpecifyRadius, maxRadius, searchAngleRange)

            print("xOfMax = " + str(xOfMax))
            print("yOfMax = " + str(yOfMax))
            print("zOfMax = " + str(zOfMax))
            print("maxConcentration = " + str(maxConcentration))

            #x, y座標は固定しz座標だけを変化させ、最高濃度値を示すz座標を見つける
            zOfFixedXY, maxConcentrationOfFixedXY = common3d.FindMaxConcentrationOnZ(pollutions, fixedX = xOfMax, fixedY = yOfMax)

            #z座標を変えても最高濃度値の更新がなければ探索終了
            if(maxConcentrationOfFixedXY <= maxConcentration):
                return xOfMax, yOfMax, zOfMax, maxConcentration

            #z座標を変化させて最高濃度値の更新があれば探索座標等を更新
            zOfMax = zOfFixedXY
            beginPositions = common.ConvertSingleElementsToList(xOfMax, yOfMax, zOfMax)
            maxConcentration = maxConcentrationOfFixedXY
            print("new z = " + str(zOfMax))
