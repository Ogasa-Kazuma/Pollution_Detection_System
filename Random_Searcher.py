

import random
import common
import numpy as np

class RandomSearcher:

    def __init__(self):
        self.__pathOfSearchedX = list()
        self.__pathOfSearchedY = list()
        self.__pathOfSearchedZ = list()
        self.__searchingDistance = 0

    def CalculateSearchingDistance(self):
        for i in range(len(self.__pathOfSearchedX) - 1):
            x_calc = (self.__pathOfSearchedX[i + 1] - self.__pathOfSearchedX[i]) ** (2)
            y_calc = (self.__pathOfSearchedY[i + 1]- self.__pathOfSearchedY[i]) ** (2)
            z_calc = (self.__pathOfSearchedZ[i + 1] - self.__pathOfSearchedZ[i]) ** (2)
            self.__searchingDistance += np.sqrt(x_calc + y_calc + z_calc)

        return self.__searchingDistance

    def SearchTargetPollution(self, pollutions, targetValue):

        pollutions_ = pollutions.copy()
        xlim, ylim, zlim = pollutions_.shape

        xOfMax, yOfMax, zOfMax, maxConcentration = 0, 0, 0, 0

        while(1):
            #初期座標をランダムに設定

            x = random.randint(0, xlim - 1)
            y = random.randint(0, ylim - 1)
            z = random.randint(0, zlim - 1)

            self.__pathOfSearchedX.append(x)
            self.__pathOfSearchedY.append(y)
            self.__pathOfSearchedZ.append(z)

            while(1):

                #探索距離が上限に達したら探索を終了
                maxDistanceLimit = 100000
                if(self.CalculateSearchingDistance() > maxDistanceLimit):
                    print("探索距離が" + str(maxDistanceLimit) + "を超えたため探索を中止します")
                    return xOfMax, yOfMax, zOfMax, maxConcentration

                #目標濃度値以上の場所を発見したら探索終了
                if(pollutions_[x][y][z] >= targetValue):
                    return x, y, z, pollutions_[x][y][z]

                #周りの濃度値が全て一定（つまりより濃度の高い点が見つからない）ならランダムに移動し探索し直す
                range = [(x - 1 >= 0), (x + 1 < xlim), (y - 1 >= 0), (y + 1 < ylim), (z - 1 >= 0), (z + 1 < zlim)]
                extractedPollutions = common.ExtractList(pollutions_, [x - range[0], x + range[1]], \
                [y - range[2], y + range[3]], [z - range[4], z + range[5]])

                #周りの濃度値に変化があるかどうかを判定
                if(common.IsAllElementsEqual(extractedPollutions)):
                    break

                #ランダムに進行方向を決定
                x_ = random.randint(-1, 1)
                y_ = random.randint(-1, 1)
                z_ = random.randint(-1, 1)

                #濃度リストの範囲外ならもう一度x_とかをランダムに決め直す
                if(0 <= (x + x_) and 0 <= (y + y_) and 0 <= (z + z_) and (x + x_) < xlim and (y + y_) < ylim and (z + z_) < zlim):
                    self.__pathOfSearchedX.append(x + x_)
                    self.__pathOfSearchedY.append(y + y_)
                    self.__pathOfSearchedZ.append(z + z_)

                    #さらに高い濃度の点を見つけたら座標と濃度値を更新
                    if(pollutions_[x + x_][y + y_][z + z_] > pollutions_[x][y][z]):
                        x, y, z = x + x_, y + y_, z + z_

                    #「探索全体での最高濃度値」を超えていれば座標を更新(上記の更新はあくまで現在地とその周辺についてのみの比較のみ)
                    if(pollutions_[x][y][z] > maxConcentration):
                        xOfMax, yOfMax, zOfMax = x, y, z
                        maxConcentration = pollutions_[x][y][z]
