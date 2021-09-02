

import numpy as np

xLength = 5
yLength = 10
zLength = 15

test_list = [[[0.0 for i in range(zLength)] for j in range(yLength)] for k in range(xLength)]

for x_count in range(xLength):
    for y_count in range(yLength):
        for z_count in range(zLength):
            test_list[x_count][y_count][z_count] = 0.0


print(test_list)
arrayed = np.array(test_list)
print(arrayed.shape)
