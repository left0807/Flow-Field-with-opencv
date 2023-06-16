import numpy as np

v1 = np.array([1, 2, 3, 4])
v2 = v1.copy()
v1 += 10
print(v1, v2)