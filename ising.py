from random import getrandbits, randint
import math
import numpy
import pprint

K = 1
J = 1

def totalSpin(l):
    t = 0
    for i in range(len(l)):
        for j in range(len(l)):
            t += sum(l[i][j])
    return t/((len(l)**2)*2)

def totalEnergy(l):
    E = 0
    n = len(l)
    for i in range(n):
        for j in range(n):
            E += -J * l[i][j][1] * (l[i][j][0] + l[i-1][j][0] if i>0 else l[n-1][j][0] + l[i][j+1][0] if j+1<n else l[i][0][0])
            E += -J * l[i][j][0] * (l[i][j][1] + l[i][j-1][1] if j>0 else l[i][n-1][1] + l[i+1][j][1] if i+1<n else l[0][j][1])
    return E

def lattice(n,T=0.01):
    #config = [[[1 if getrandbits(1) else -1,1 if getrandbits(1) else -1] for j in range(n)] for i in range(n)]
    config = [[[1,1] for j in range(n)] for i in range(n)]
    eprev = totalEnergy(config)
    for ite in range(1000000):
        #row col - unit cell - 2 points in each unit cell
        i,j,k = randint(0,n-1),randint(0,n-1),getrandbits(1)
        if k == 1: #chose top site
            Hold = -J * config[i][j][1] * (config[i][j][0] + config[i-1][j][0] if i>0 else config[n-1][j][0] + config[i][j+1][0] if j+1<n else config[i][0][0])
        elif k == 0: #chose bottom site
            Hold = -J * config[i][j][0] * (config[i][j][1] + config[i][j-1][1] if j>0 else config[i][n-1][1] + config[i+1][j][1] if i+1<n else config[0][j][1])
        # p proportional to exp(-bH)
        Hnew = -1 * Hold
        if Hnew < Hold:
            config[i][j][k] *= -1
        else:
            beta = 1 /(K*T)
            prob = math.e**(beta*(Hold-Hnew))
            config[i][j][k] = numpy.random.choice([-1*config[i][j][k],config[i][j][k]], p=[prob,1-prob])
            
        if ite > (n**2)*2 and ite % (n**2)*2 == 0:
            e = totalEnergy(config)
            if abs(e-eprev)<0.00000001:
                return totalSpin(config),e
            else:
                eprev = e
                
    return totalSpin(config),totalEnergy(config)

el = []
sl = []

for i in range(1,200):
    temp = i/100
    s,e = 0,0
    for j in range(20):
        res = lattice(18,temp)
        s += res[0]
        e += res[1]
    s /= 20
    e /= 20
    el.append(e)
    sl.append(s)
    print(temp,s,e,sep=',')

"""
with open("data4.csv") as f:
    l = f.readline()
    while l:
        t,s,e = l.split(',')
        el.append(float(e))
        sl.append(float(s))
        l = f.readline()

vr = numpy.var(el)
for i in range(1,200):
    temp = i/100
    c = (1/(K*temp*temp*2*18*18))*vr
    print(temp,sl[i],el[i],c,sep=',')
"""
"""
heat capacity c = (1/(k*T*T*N))*(variance of E) , where E is the sum of all the site hamiltonians, variance = mean of E**2 - * (mean of E)**2
"""
