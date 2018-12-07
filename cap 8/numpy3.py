from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
mp   = MPI.COMM_WORLD.Get_size()

if rank == 0:
    numData = 10
else:
    numData = None
    
numData = comm.bcast(numData, root=0)
print(rank, 'Number of data to receive: ',numData)

if rank == 0:
    data = np.linspace(0.0,3.14,numData)
    recvbuf = np.empty(mp*10, dtype='d')
else:
    data = np.empty(numData, dtype='d')  # allocate space to receive the array
    recvbuf = None

comm.Bcast(data, root=0)
print(rank, 'data received: ',data)
sendbuf = np.linspace(rank*100,rank*100+10,numData,endpoint=False)
print (rank, 'Local data to send to master:', sendbuf)
comm.Gather(sendbuf, recvbuf, root=0)
print (rank,'recvbuf',recvbuf)
