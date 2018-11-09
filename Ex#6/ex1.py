from mpi4py import MPI
from random import randint
from math import sqrt
import sys

def rollDices(n):
	O = {}
	for i in range(2, 13):
		O[i] = 0
	    
	for i in range(n):
		v1 = randint(1, 6)
		v2 = randint(1, 6)
		v = v1 + v2
		O[v] += 1
	
	return O

def expectedFreq(n):
	E = {}
	for i in range(2, 13):
		if i <= 7:
			E[i] = n*((i-1)/36)
		else:
			E[i] = n*((13-i)/36)
	return E

def meanDev(O, E):
	sum = 0
	for i in range(2, 13):
		sum += ((O[i] - E[i])/E[i])**2
	
	return (1/11)*sqrt(sum)	


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
go = 1

p = MPI.COMM_WORLD.Get_size()
n = int(sys.argv[1])//p
sigma = 1

if rank == 0:
	print ('Number of processes:', p)

while sigma > 0.001:
	
	E = expectedFreq(n*p)
	O = rollDices(n)

	Op = comm.gather(O, root = 0)
	
	if rank == 0:
		for i in range(1, 4):
			for j in range(2, 13):
				Op[0][j] += Op[i][j]
		Op = Op[0]
				
		
		sigma = meanDev(Op, E)	

		print(Op, sum(Op[i] for i in range(2, 13)))
		print('sigma =', sigma)
		n *= 2

	sigma = comm.bcast(sigma, root = 0)
	n = comm.bcast(n, root = 0)
	


"""
mpirun -n 4 python ex1.py 1024

Output:
Number of processes: 4
{2: 26, 3: 71, 4: 89, 5: 115, 6: 147, 7: 153, 8: 133, 9: 129, 10: 82, 11: 51, 12: 28} 1024
sigma = 0.031136591656716294
{2: 61, 3: 118, 4: 170, 5: 218, 6: 290, 7: 324, 8: 299, 9: 225, 10: 160, 11: 129, 12: 54} 2048
sigma = 0.017830101941209733
{2: 123, 3: 248, 4: 350, 5: 440, 6: 533, 7: 695, 8: 549, 9: 453, 10: 339, 11: 237, 12: 129} 4096
sigma = 0.018543610786304954
{2: 193, 3: 424, 4: 715, 5: 917, 6: 1136, 7: 1335, 8: 1185, 9: 963, 10: 692, 11: 428, 12: 204} 8192
sigma = 0.02034079853413354
{2: 431, 3: 935, 4: 1317, 5: 1846, 6: 2232, 7: 2723, 8: 2308, 9: 1830, 10: 1389, 11: 894, 12: 479} 16384
sigma = 0.008613082040732209
{2: 984, 3: 1838, 4: 2739, 5: 3632, 6: 4573, 7: 5482, 8: 4431, 9: 3649, 10: 2721, 11: 1826, 12: 893} 32768
sigma = 0.008027283710731487
{2: 1773, 3: 3695, 4: 5398, 5: 7316, 6: 9133, 7: 10896, 8: 9041, 9: 7269, 10: 5561, 11: 3621, 12: 1833} 65536
sigma = 0.0035592344995959836
{2: 3681, 3: 7396, 4: 11069, 5: 14442, 6: 18204, 7: 21801, 8: 18249, 9: 14574, 10: 10812, 11: 7244, 12: 3600} 131072
sigma = 0.0027012233907138697
{2: 7214, 3: 14595, 4: 21816, 5: 29006, 6: 36195, 7: 43795, 8: 36425, 9: 29181, 10: 22072, 11: 14667, 12: 7178} 262144
sigma = 0.002063950975509691
{2: 14607, 3: 29149, 4: 43745, 5: 58418, 6: 72852, 7: 87278, 8: 72643, 9: 58342, 10: 43567, 11: 29089, 12: 14598} 524288
sigma = 0.0006022174221024911
"""


