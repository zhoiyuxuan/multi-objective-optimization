import numpy as np
a = np.array([1,1,0,1]).reshape((2,2))
print(a)
for k in range(100):
    b = np.array([k,0,0,k]).reshape((2,2))
    print(a.dot(b)==b.dot(a))
c = np.array([0,1,0,1,0,0,0,0,1]).reshape((3,3))
print(c)

print(a.dot(b))
print(b.dot(a))
