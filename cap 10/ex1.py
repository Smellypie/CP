from mpi4py import MPI
import numpy as np
import sys
from math import sqrt

def E(n, i, j, a):
	E = np.zeros(n**2).reshape((n, n))
	
	for k in range(n):
		E[k][k] = 1;
	
	E[j][i] = a
	
	return E

def P(n, i, j):
	P = np.zeros(n**2).reshape((n, n))
	
	for k in range(n):
		P[k][k] = 1;
	
	P[i][i] = 0
	P[j][j] = 0
	P[i][j] = 1
	P[j][i] = 1
	
	return P

def D(n, i, a):
	D = np.zeros(n**2).reshape((n, n))
	
	for k in range(n):
		D[k][k] = 1;
	
	D[i][i] = a
	
	return D

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp   = MPI.COMM_WORLD.Get_size()
n = int(sys.argv[1])

a = np.empty(n**2, dtype='d').reshape((n,n))

if rank == 0:
	a = np.random.rand(n**2).reshape((n,n))
	
	print('A =', a)

	recvbuf = np.empty(n**2, dtype='d').reshape((n,n))

comm.Bcast(a, root=0)
if rank == 2:
	for i in range(n):
		for j in range(i+1, n):
			if (rank*(int(n/mp)) <= j < (rank+1)*(int(n/mp))):
				if a[i][i] != 0:
					k = -(a[j][i]/a[i][i])
					e = E(n, i, j, k)
					a = np.matmul(e, a)
					print(a)

if rank == 2:
	print(a)


################################################################
"""
if rank == 0:
	a = np.random.rand(n**2).reshape((n,n))
	
	print('A =', a)

	recvbuf = np.empty(n**2, dtype='d').reshape((n,n))
	
	for i in range(1, mp):
		comm.send(a[i], dest=i)

	a = a[0]
else:
	a = comm.recv(source=0)
	b = np.empty(n**2, dtype='d').reshape((n,n))  # allocate space to receive the array
	recvbuf = None

comm.Bcast(b, root=0)

sendbuf = np.matmul(a, b)

comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
	print('AB =', recvbuf)
"""

