from mpi4py import MPI
from math import sqrt
import time
import sys

def doStuff(inf, sup, n):
	hits = 0
	for i in range(int(n*inf), int(n*sup)):
		for j in range(0, n):
			if sqrt(i**2 + j**2) < n:
				hits += 1
			else:
				break
	return hits

def errRel(T):
	if max(T) != 0:
		return (max(T)-min(T))/max(T)
	else:
		return 0

def adjust(I, T): #TODO funcao para ajustar os intervalos
	pass

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
I = [0, 1/4, 1/2, 3/4, 1]

if(rank == 0):
	p = MPI.COMM_WORLD.Get_size()
	n = int(sqrt(int(sys.argv[1])))
	T = [1, 0, 0, 0]

	print('Number of processes:', p)
	
	while errRel(T) > 0.001:
		for i in range(1, p):
			comm.send(1, i)
		
		init = time.time()
		Hits = doStuff(I[rank], I[rank + 1], n)
		T[rank] = time.time() - init
		
		for i in range(1, p):
			comm.send(n, i)
			T[i] = comm.recv(source=i)
			Op = comm.recv(source=i)
			Hits += Op
		
		print('pi =', 4*(Hits/n**2))
		print(T, errRel(T))
		
		adjust(I, T)

	for i in range(1, p):
		comm.send(0, i)
		
	print('Done')

else:
	while comm.recv(source=0) != 0:
		n = comm.recv(source=0)
		init = time.time()
		Hits = doStuff(I[rank], I[rank + 1], n)
		comm.send(time.time() - init, 0)
		comm.send(Hits, 0)




