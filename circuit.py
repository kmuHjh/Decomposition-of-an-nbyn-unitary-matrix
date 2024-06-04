import numpy as np
import decomposition_matrix as dm
from qiskit import *
import cmath

#twolevel_arr : U1^d,U2^d...Un^d (data type : array [n][n])
#type_arr : 109, 191, 119 (data type : array str)
#tlform : 054, 075, 067 (data type : array int)
#main input function
def decomposition_nqubit(qc, matrix):
    twolevel_arr, type_arr, tlform_arr = dm.decomposition_matrix(matrix)
    for i in range(len(twolevel_arr)):
        swapgate(qc, type_arr[i])
    


        swapgate(qc, type_arr[i])
    

def swapgate(qc, type_arr):
    target_position = type_arr.index('9')
        if type_arr[0] != '9':
            origin_0 = type_arr[0]
            type_arr[target_position] = origin_0
            type_arr[0] = '9'
            qc.cx(target_position, 0)
            qc.cx(0, target_position)
            qc.cx(target_position, 0)


#This x gate is for anti control bit.
def xgate(qc, flag, position):
    if flag:
        qc.x(position)


def UtoSingle(matrix):
    det = np.linalg.det(matrix)
    det_re = np.real(det)
    det_im = np.imag(det)
    pi_v = (1/2) * math.atan2(det_im,det_re)

    matrix = matrix/np.exp(1j*pi_v)
    
    complex_1 = matrix[0][0]
    complex_2 = matrix[0][1]

    r_1 = np.abs(complex_1)
    r_2 = np.abs(complex_2)

    theta_val = math.atan2(r_2, r_1)
    lambda_val = cmath.phase(complex_1)  
    mu_val = cmath.phase(complex_2)  
    
    alpha = (lambda_val + mu_val)
    beta = 2*theta_val
    gamma = lambda_val - mu_val
    
    
    return (alpha), (beta), (gamma), (pi_v)
    

def decomposition_2qubit(qc, control_type, control_p, target_p, U):
    xgate(qc, not control_type, control_p)
    alpha, beta, gamma, pi_v = UtoSingle(U)
    xgate(qc, not control_type, control_p)
    return 0


#test set

matrix_8 = np.array([
[0,0,0,0,-1,0,0,0],
[0,0,0,0,0,-1,0,0],
[0,0,0,0,0,0,0,-1],
[0,0,0,0,0,0,-1,0],
[1,0,0,0,0,0,0,0],
[0,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0],
[0,0,1,0,0,0,0,0]])

matrix_4 = (1/2)*np.array([
[1,1,1,1],
[1,1j,-1,-1j],
[1,-1,1,-1],
[1,-1j,-1,1j]])

qc = QuantumCircuit(2,2)
decomposition_nqubit(qc, matrix_4)