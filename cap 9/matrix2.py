import numpy as np
import sys

n = int(sys.argv[1])
debug = sys.argv[1][0] == '+'

#a=np.random.rand(n**2).reshape((n,n))
#b=np.random.rand(n**2).reshape((n,n))
a = np.linspace(1,n**2,n**2).reshape((n,n))
b = np.linspace(10,10*n**2,n**2).reshape((n,n))

ab=np.matmul(a, b)

print ('a:\n%s' % a)
print ('b:\n%s' % b)
print ('ab:\n%s' % ab)
