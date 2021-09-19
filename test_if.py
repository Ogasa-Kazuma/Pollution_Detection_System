

import test_random_speed
import importlib
import numpy as np
import copy
import Pollution_Creater3D
import Test
importlib.reload(Test)
importlib.reload(test_random_speed)
importlib.reload(np)
importlib.reload(copy)
importlib.reload(Pollution_Creater3D)

import Data_Recorder
import inspect
importlib.reload(inspect)





test = Test.Test_()
test2 = Test.Test_()

test.setTestValue(50)
test2.setTestValue(30)

test.ConfuseObj(test2)
print(test.getTestValue())
print(test2.getTestValue())



# #インスタンスが違えば、メンバ関数のIDは違うものになる！！！！！！
# print(test.getTestValue is test2.getTestValue)
# print(id(test.getTestValue))
# print(id(test2.getTestValue))
#
# #aにtestのメンバ関数のidを格納
# a = test.setTestValue
# a(50) #インスタンスのメンバメソッド単体も格納できる！
#
# #aにはメンバ関数のidが入っているのでaとメンバ関数のidは等しい
# print(a)
# print(id(test.setTestValue))
