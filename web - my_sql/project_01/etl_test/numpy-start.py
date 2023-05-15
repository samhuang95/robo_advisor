import numpy as np

# data = np.empty([3,3,3])
# print(data)





arr1 = np.array([
    [1,2,3],
    [4,5,6]
])

arr2 = np.array([
    [1,2,3],
    [4,5,6]
])

arr3 = np.array([
    [1,2]
    [2,3]
])

re = np.hstack((arr1, arr2, arr3))
print(re)