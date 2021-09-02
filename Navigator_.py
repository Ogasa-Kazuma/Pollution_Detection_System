




class Navigator:

    def __init__(self, minTerminalConcentration):
        self.__minTerminalConcentration = minTerminalConcentration

    def setMinTerminalConcentration(self, minTerminalConcentration):
        self.__minTerminalConcentration = minTerminalConcentration

    def InstructNextDirection(self, lastPositionsOfMax, latestPositionsOfMax):
        #オイラー角を計算
        roll, pitch, yaw = common.CalculateEulerAngles(lastPositionsOfMax, latestPositionsOfMax)
        return roll, pitch, yaw
