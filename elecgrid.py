import math

def elecgrid(n,vin=100,vout=0,dump=False):
    
    if n == 1: #if n = 1, then it is 1 solitary unit resistor
        gr = 1
        current = (vin-vout)/gr
        print("n =",n,":")
        print("Total current = ",current,"A")
        print("Grid resistance = ",gr,"Ohms\n")
        return
    
    N = n**2

    #solve ax = b
    def solve(a,b):
        def lud(a):
            u = [[0 if j > 0 else a[0][i] for i in range(N)] for j in range(N)]
            for i in range(1,N):
                u.append([0 for j in range(N)])
            l = [[0 for i in range(N)] for j in range(N)]
            for i in range(N):
                l[i][i] = 1
            for row in range(1,N):
                l[row][0] = a[row][0] / u[0][0]
                for col in range(1,N):
                    s = a[row][col] - sum([l[row][i]*u[i][col] for i in range(0, row+1)])
                    if row > col:
                        l[row][col] = s / u[col][col]
                    else:
                        u[row][col] = s
            return (l,u)
        # lu = a
        (l,u) = lud(a)
        # ly = b, ux = y
        y = [0 for i in range(N)]
        x = [0 for i in range(N)]
        for row in range(N):
            y[row] = (b[row] - sum([l[row][i]*y[i] for i in range(0, row+1)])) / l[row][row]
        for row in reversed(range(N)):
            x[row] = (y[row] - sum([u[row][i]*x[i] for i in range(row, N)])) / u[row][row]
        return tuple(x)
    
    coeff = [[0 for i in range(n**2)] for j in range(n**2)]
    tr = 1e-100 # "ohmic contact" btw corners of grid and vin/vout
    r = 1/math.sqrt(n)
    
    for i in range(n):
        for j in range(n):
            p = n*i+j
            if i > 0:
                coeff[p][p-n] = 1
                coeff[p][p] -= 1
            if i < n-1:
                coeff[p][p+n] = 1
                coeff[p][p] -= 1
            if j > 0:
                coeff[p][p-1] = 1
                coeff[p][p] -= 1
            if j < n-1:
                coeff[p][p+1] = 1
                coeff[p][p] -= 1
            if (i == 0 and j == n-1) or (i == n-1 and j == 0):
                coeff[p][p] += r/tr
                
    b = [0 for i in range(N)]
    b[n-1] = (r*vin)/tr #top right corner - vin
    b[n*(n-1)] = (r*vout)/tr #bottom left corner - vout
    
    v = solve(coeff,b)
    
    #Grid display
    print("n =",n,":")
    if dump:
        print("\nGrid diagram :")
        for i in range(n):
            for j in range(n-1):
                print(round(v[(n*i)+j],2),"V",sep='',end='\t')
                print(round((v[(n*i)+j+1]-v[(n*i)+j])/r,2),"A",sep='',end='\t')
            print(round(v[(n*i)+(n-1)],2),"V\n",sep='')
            if i < n - 1:
                for j in range(n):
                    print(round((v[(n*i)+j]-v[(n*(i+1))+j])/r,2),"A\t",sep='',end='\t')
                print("\n")

    current = 2 * ((v[n-1] - v[n-2])/r)
    gr = (vin-vout)/current
    print("Total current = ",current,"A")
    print("Grid resistance = ",gr,"Ohms\n")

for i in range(8):
    elecgrid(2**i,vin=1,vout=0,dump=True)

def h(cl):
    for f in dir(cl):
        if "_" not in f:
            print(f,end=": ")
            help(getattr(cl,f))

