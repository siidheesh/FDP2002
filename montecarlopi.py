from random import random
import math

def monte():
    N = 100000
    count = 0
    for i in range(N):
        if (random()**2)+(random()**2) <= 1:
            count += 1

    return (4*count)/N
"""
l = ()
n = 10000
for i in range(n):
    l += (monte(),)

mean = sum(l)/n
variance = (sum([x**2 for x in l])/n) - mean**2

print(mean,variance)
"""

def needle(): #needle length = 1, line spacing = 1
    N = 100000
    count = 0
    for i in range(N):
        x = abs(math.cos(2 * math.pi * random())) + random()
        if x >= 1.0:
            count += 1
    return (2*(N/count))

def needle2():
    N = 100000
    count = 0
    for i in range(N):
        a = (2*random(),random())
        b = (2*random(),random())
        length = (((a[0]-b[0])**2)+((a[1]-b[1])**2))**0.5
        x = min(a[0],b[0]) + abs((a[0]-b[0])/length)
        if x > 1.0:
            count += 1
    return (2*(N/count))

def monte1():
    N = 10000
    count = 0
    for i in range(N):
        x,y = random(),random()
        if (x**2)+(y**2) <= 1 and (((x-1)**2)+((y-0.5)**2)) <= 0.5**2:
            count += 1

    return count/N

l = ()
n = 1000
for i in range(n):
    l += (monte1(),)

mean = sum(l)/n
variance = (sum([x**2 for x in l])/n) - mean**2

print(mean,variance)
