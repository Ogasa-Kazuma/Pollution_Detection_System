


class Test_:

  def __init__(self):
    self.__testValue = 100
    myID = self

  def setTestValue(self, value):

    print(id(self))
    self.__testValue = value

  def getTestValue(self):
    return self.__testValue

  def ConfuseObj(self, self2):

      print(self)
      print(self2)

      self = self2


  def getFuncID(self):
      print(id(self.setTestValue))
      return id(self.getTestValue)
