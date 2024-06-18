import circuit as cc
from qiskit import *
import numpy as np
from qiskit.quantum_info import Statevector
import unitary as u

bit_num = 32
target_det = 1j
matrix = u.generate_unitary_matrix_with_det(bit_num, target_det)

n = int(np.log2(matrix.shape[0]))
qc = QuantumCircuit(n,n)

#qc.x(0)
#qc.x(1)


qc.barrier()
cc.decomposition_list(qc, matrix)
ket = Statevector(qc)
ket.draw('latex')

qc.draw('mpl')