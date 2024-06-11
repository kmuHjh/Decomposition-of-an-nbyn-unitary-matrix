import circuit as cc
from qiskit import *
import numpy as np

matrix = np.array([
[0,0,0,0,-1,0,0,0],
[0,0,0,0,0,-1,0,0],
[0,0,0,0,0,0,0,-1],
[0,0,0,0,0,0,-1,0],
[1,0,0,0,0,0,0,0],
[0,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0]])

n = int(np.log2(matrix.shape[0]))

qc = QuantumCircuit(n,n)
cc.decomposition_list(qc, matrix)
qc.draw('mpl')