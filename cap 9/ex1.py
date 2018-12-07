from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp   = MPI.COMM_WORLD.Get_size()
n = int(sys.argv[1])

if rank == 0:
	a = np.random.rand(n**2).reshape((n,n))
	b = np.random.rand(n**2).reshape((n,n))
	
	print('A =', a)
	print('B =', b)

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
mpirun -n 4 python ex1.py 4

Output:
A = [[ 0.74591729  0.61653374  0.43884297  0.45714971]
 [ 0.56082061  0.69735534  0.31142346  0.717076  ]
 [ 0.21418818  0.01738483  0.89673599  0.15490917]
 [ 0.30107933  0.24827121  0.91797089  0.99449601]]
B = [[ 0.0875909   0.89808533  0.97421103  0.26826853]
 [ 0.82067443  0.78065795  0.5074437   0.69023383]
 [ 0.35081293  0.79891743  0.24435334  0.67594049]
 [ 0.69019274  0.91499478  0.02325737  0.47656687]]
AB = [[ 1.04078224  1.92008824  1.15740186  1.14015272]
 [ 1.2255965   1.95298318  0.99300086  1.18402716]
 [ 0.45453198  1.06408996  0.44020952  0.74942429]
 [ 1.23855162  2.10755143  0.66673708  1.34657284]]
"""




