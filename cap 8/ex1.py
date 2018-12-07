from mpi4py import MPI
import numpy as np
from sys import argv

def asDouble(r, i, n):
	for j in range(n):
		if r[i] == r[j] and i != j:
			return (1)
	return (0)

def fix(r, n):
	moved = 0
	for i in range(n):
		if asDouble(r, i, n):
			moved = 1
			r[i] += 1
	if moved == 1:
		fix(r, n)

def rankSort(a, n1, n2):
	r = np.empty(n2 - n1, dtype='d')
	for i in range(n1, n2):
		x = 0
		for j in range(n):
			if a[i] > a[j]:
				x += 1
		r[i%(n2-n1)] = x

	return r

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp   = MPI.COMM_WORLD.Get_size()
n = int(argv[1])

if rank == 0:
	data = np.random.rand(n)
	recvbuf = np.empty(n, dtype='d')
else:
	data = np.empty(n, dtype='d')  # allocate space to receive the array
	recvbuf = None

comm.Bcast(data, root=0)
print(rank, 'data received: ', data)

sendbuf = rankSort(data, rank*(n//mp), (rank+1)*(n//mp))

comm.Gather(sendbuf, recvbuf, root=0)
print(rank,'recvbuf',recvbuf)

if rank == 0:
	fix(recvbuf, n)
	b = np.empty(n, dtype=float)
	for i in range(n):
		b[int(recvbuf[i])] = data[i]

	print(b)


"""
mpirun -n 4 python ex1.py 12

Output:
1 data received:  [ 0.96856241  0.09449252  0.6165444   0.07271075  0.8942985   0.93241756
  0.13921901  0.57749488  0.48653928  0.54097358  0.14829868  0.03983311]
1 recvbuf None
2 data received:  [ 0.96856241  0.09449252  0.6165444   0.07271075  0.8942985   0.93241756
  0.13921901  0.57749488  0.48653928  0.54097358  0.14829868  0.03983311]
2 recvbuf None
3 data received:  [ 0.96856241  0.09449252  0.6165444   0.07271075  0.8942985   0.93241756
  0.13921901  0.57749488  0.48653928  0.54097358  0.14829868  0.03983311]
3 recvbuf None
0 data received:  [ 0.96856241  0.09449252  0.6165444   0.07271075  0.8942985   0.93241756
  0.13921901  0.57749488  0.48653928  0.54097358  0.14829868  0.03983311]
0 recvbuf [ 11.   2.   8.   1.   9.  10.   3.   7.   5.   6.   4.   0.]
[ 0.03983311  0.07271075  0.09449252  0.13921901  0.14829868  0.48653928
  0.54097358  0.57749488  0.6165444   0.8942985   0.93241756  0.96856241]

"""

