from abc import ABCMeta, abstractmethod

# 抽象クラス
class Pollution_State_Creater(metaclass=ABCMeta):


    @abstractmethod
    def create_local_pollution(self):
        pass

    @abstractmethod
    def create_random_pollution(self):
        pass

    @abstractmethod
    def Auto_Pollutions_Create(self):
        pass

    @abstractmethod
    def Adjust_Pollution(self):
        pass

    @abstractmethod
    def get_all_pollution_states(self):
        pass
