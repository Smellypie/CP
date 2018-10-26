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

if(rank == 0):
	p = MPI.COMM_WORLD.Get_size()
	n = int(sys.argv[1])//p
	sigma = 1

	print ('Number of processes:', p)
	
	while sigma > 0.001:
		for i in range(1, p):
			comm.send(1, i)
		
		E = expectedFreq(n*p)
		O = rollDices(n)
		
		for i in range(1, p):
			comm.send(n, i)
			Op = comm.recv(source=i)
			
			for j in range(2, 13):
				O[j] += Op[j]
		
		sigma = meanDev(O, E)
		
		print(O, sum(O[i] for i in range(2, 13)))
		print('sigma =', sigma)
		n *= 2

	for i in range(1, p):
		comm.send(0, i)
		
	print('Done')

else:
	while (comm.recv(source=0)) != 0:
		n = comm.recv(source=0)
		O = rollDices(n)
		comm.send(O, dest=0)

"""
mpirun -n 4 python ex1.py 1024

Output:
Number of processes: 4
{2: 23, 3: 57, 4: 64, 5: 105, 6: 132, 7: 179, 8: 152, 9: 119, 10: 98, 11: 66, 12: 29} 1024
sigma = 0.03721066503487429
{2: 53, 3: 110, 4: 158, 5: 274, 6: 263, 7: 320, 8: 280, 9: 230, 10: 164, 11: 135, 12: 61} 2048
sigma = 0.029377852747926758
{2: 123, 3: 236, 4: 357, 5: 468, 6: 576, 7: 677, 8: 575, 9: 438, 10: 333, 11: 219, 12: 94} 4096
sigma = 0.01924948283196108
{2: 199, 3: 478, 4: 678, 5: 976, 6: 1115, 7: 1388, 8: 1142, 9: 868, 10: 655, 11: 477, 12: 216} 8192
sigma = 0.016494935831776428
{2: 455, 3: 932, 4: 1371, 5: 1809, 6: 2278, 7: 2690, 8: 2271, 9: 1884, 10: 1342, 11: 879, 12: 473} 16384
sigma = 0.006485037662960884
{2: 952, 3: 1809, 4: 2594, 5: 3700, 6: 4515, 7: 5562, 8: 4482, 9: 3615, 10: 2731, 11: 1809, 12: 999} 32768
sigma = 0.011189942690561347
{2: 1858, 3: 3602, 4: 5494, 5: 7322, 6: 9108, 7: 10928, 8: 9110, 9: 7294, 10: 5436, 11: 3565, 12: 1819} 65536
sigma = 0.0029692016459613555
{2: 3580, 3: 7283, 4: 10923, 5: 14645, 6: 18296, 7: 21751, 8: 18216, 9: 14548, 10: 10969, 11: 7186, 12: 3675} 131072
sigma = 0.002291273148947473
{2: 7354, 3: 14479, 4: 21691, 5: 29329, 6: 36708, 7: 43356, 8: 36152, 9: 29162, 10: 22059, 11: 14617, 12: 7237} 262144
sigma = 0.0021404495516942467
{2: 14440, 3: 29123, 4: 43481, 5: 58619, 6: 72710, 7: 87532, 8: 72877, 9: 58184, 10: 43551, 11: 29182, 12: 14589} 524288
sigma = 0.001143927432826927
{2: 29418, 3: 58234, 4: 87200, 5: 116346, 6: 145278, 7: 174624, 8: 145763, 9: 116784, 10: 87255, 11: 58385, 12: 29289} 1048576
sigma = 0.001139620955915055
{2: 58332, 3: 116424, 4: 174602, 5: 233036, 6: 291243, 7: 350411, 8: 291393, 9: 232791, 10: 174352, 11: 116353, 12: 58215} 2097152
sigma = 0.00039059134172583814
Done
"""


