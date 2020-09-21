import numpy as np
from numba import jit
import time

def f1(x):
    y = x*0.0
    for i in range(len(x)):
        y[i] = np.log(x[i])
    return y

@jit(nopython=True)
def f2(x):
    y = np.zeros(len(x))
    for i in range(len(x)):
        y[i] = np.log(x[i])
    return y

x = np.arange(0.1, 100, .0001)

t1 = time.time()
y1 = f1(x)
t2 = time.time()
y2 = f2(x)
t3 = time.time()
y3 = f2(x)
t4 = time.time()

print(t2-t1)
print(t3-t2)
print(t4-t3)

