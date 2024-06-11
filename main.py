import circuit as cc
from qiskit import *
import numpy as np
from qiskit.quantum_info import Statevector

matrix_7 = np.array([
[0,0,0,0,-1,0,0,0],
[0,0,0,0,0,-1,0,0],
[0,0,0,0,0,0,0,-1],
[0,0,0,0,0,0,-1,0],
[1,0,0,0,0,0,0,0],
[0,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0]])

matrix_5 = (1/2)*np.array([
[1,1,1,1],
[1,1j,-1,-1j],
[1,-1,1,-1],
[1,-1j,-1,1j]])

matrix_t = np.array([
[1,0,0,0],
[0,1,0,0],
[0,0,0,1],
[0,0,1,0]])


matrix = matrix_7
n = int(np.log2(matrix.shape[0]))
qc = QuantumCircuit(n,n)

#qc.x(0)
#qc.x(1)


qc.barrier()
cc.decomposition_list(qc, matrix)
ket = Statevector(qc)
ket.draw('latex')

qc.draw('mpl')