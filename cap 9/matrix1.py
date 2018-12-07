import numpy as np
import sys

n = int(sys.argv[1])

#a=np.random.rand(n**2).reshape((n,n))
#b=np.random.rand(n**2).reshape((n,n))
a = np.linspace(1,n**2,n**2).reshape((n,n))
b = np.linspace(10,10*n**2,n**2).reshape((n,n))

c=np.zeros([n, n])
for i in range(n):
    for k in range(n):
        for j in range(n):
            c[i][j] += a[i][k]*b[k][j]

print ('a:\n%s' % a)
print ('b:\n%s' % b)
print ('c:\n%s' % c)
