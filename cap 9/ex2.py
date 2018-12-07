from mpi4py import MPI
import numpy as np
import sys
from math import sqrt

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp   = MPI.COMM_WORLD.Get_size()
n = int(sys.argv[1])
rt = int(sqrt(mp))

if rank == 0:
	a = np.random.rand(n**2).reshape((n,n))
	b = np.random.rand(n**2).reshape((n,n))
	
	print('A =', a)
	print('B =', b)
	result = np.matmul(a, b)
	#print('AB =', np.matmul(a, b))
	recvbuf = np.empty(n**2, dtype='d').reshape((n,n))
	
	bt = np.transpose(b)
	k = 0
	for i in range(rt):
		for j in range(rt):
			if k == 0:
				k += 1
			else:
				data = np.block([[a[i*(n//rt):(i+1)*(n//rt)]],
						[bt[j*(n//rt):(j+1)*(n//rt)]]])
				comm.send(data, dest=k)
				k += 1

	data = np.block([[a[0*(n//rt):(0+1)*(n//rt)]], [bt[0*(n//rt):(0+1)*(n//rt)]]])
else:
	data = comm.recv(source=0)
	recvbuf = None

a = data[:n//rt]
b = np.transpose(data[n//rt:])
sendbuf = np.matmul(a, b)

comm.Gather(sendbuf, recvbuf, root=0)

if rank == 0:
	k = 0;
	D = np.empty(n**2, dtype='d').reshape((n,n))
	for i in range(rt):
		for j in range(rt):
			D[i*(n//rt):(i+1)*(n//rt), j*(n//rt):(j+1)*(n//rt)] = recvbuf[k*(n//mp):(k+1)*(n//mp)].reshape((n//rt, n//rt))
			k += 1

	print('AB =', D)






