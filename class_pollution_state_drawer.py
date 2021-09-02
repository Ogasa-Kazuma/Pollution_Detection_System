from abc import ABCMeta, abstractmethod

# 抽象クラス
class Pollution_State_Drawer(metaclass=ABCMeta):

  @abstractmethod
  def draw_pollution_map(self):
      pass
