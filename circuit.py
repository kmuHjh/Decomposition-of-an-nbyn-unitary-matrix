import numpy as np
import decomposition_matrix as dm
from qiskit import *
import cmath

#twolevel_arr : U1^d,U2^d...Un^d (data type : array [n][n])
#type_arr : 109, 191, 119 (data type : array str)
#tlform : 054, 075, 067 (data type : array int) / for U
#main input function
def decomposition_list(qc, matrix):
    twolevel_arr, type_arr, tlform_arr = dm.decomposition_matrix(matrix)
    for i in range(len(twolevel_arr)):
        matrix_U = dm.get_Ugate(twolevel_arr[i], tlform_arr[i])
        decomposition_nqubit(qc, type_arr[i], matrix_U)
    
def decomposition_nqubit(qc, type_arr, U):
    n_circuit = count_circuit(type_arr)
    X = np.array([[0, 1],[1, 0]])
    V = dm.get_sqrtU(U)
    if n_circuit < 2:
        return
    if n_circuit == 2:
        decomposition_2qubit(qc, type_arr, U)
    decomposition_2qubit(qc, circuit_1(type_arr), V)
    print(circuit_1(type_arr))
    decomposition_nqubit(qc, circuit_2(type_arr), X)
    print(circuit_2(type_arr))
    decomposition_2qubit(qc, circuit_1(type_arr), V.conjugate().transpose())
    print(circuit_1(type_arr))
    decomposition_nqubit(qc, circuit_2(type_arr), X)
    print(circuit_2(type_arr))
    decomposition_nqubit(qc, circuit_3(type_arr), V)
    print(circuit_3(type_arr))


def decomposition_2qubit(qc, type_arr, U):
    

    return 0

#count using qubit
def count_circuit(type_arr):
    total = len(type_arr)
    n_5 = 0
    for i in range(total):
        if type_arr[i] == '5':
            n_5 = n_5 + 1
    
    return total - n_5   

# 91111 -> 91555 , 55911 -> 55915
#find first 1's position, and right side value change
def circuit_1(type_arr):
    return_arr = type_arr.copy()
    position_1 = 9999
    position_9 = 9999
    for i in range(len(type_arr)):
        if type_arr[i] == '9':
            position_9 = i
            break
    cnt_5 = 0
    if type_arr[position_9+1] == '5':
        for i in range(position_9+1, len(type_arr)):
            if type_arr[i] == '5':
                cnt_5 = cnt_5 + 1
            else:
                break
    if cnt_5 != 0:
        temp_arr = np.concatenate((type_arr[:position_9+1], type_arr[position_9+1+cnt_5:]))
        return_arr = circuit_1(temp_arr)
        if return_arr is None:
            return
        return_arr = np.concatenate((return_arr[:position_9+1], ['5']*cnt_5, return_arr[position_9+1:]))
    else:
        for i in range(len(type_arr)):
            if type_arr[i] == '1':
                position = i
                break
        for i in range(position+1, len(type_arr)):
            return_arr[i] = '5'
    return return_arr

# 91111 -> 59111, 55911 -> 55591
# find 9's position and there is '5' after shift one step to right side 
def circuit_2(type_arr):
    return_arr = type_arr.copy()
    position_9 = 9999
    for i in range(len(type_arr)):
        if type_arr[i] == '9':
            position_9 = i
            break
    cnt_5 = 0
    if position_9 < len(type_arr)-1 and type_arr[position_9+1] == '5':
        for i in range(position_9+1, len(type_arr)):
            if type_arr[i] == '5':
                cnt_5 += 1
            else:
                break
    if cnt_5 != 0:
        temp_arr = np.concatenate((type_arr[:position_9 + 1], type_arr[position_9 + 1 + cnt_5:]))
        return_arr = circuit_2(temp_arr)
        if return_arr is None:
            return
            return_arr = np.concatenate((return_arr[:position_9 + 1], ['5'] * cnt_5, return_arr[position_9 + 1:]))
    else:
        return_arr[position_9] = '5'
        for i in range(position_9 + 1, len(type_arr)):
            return_arr[i] = type_arr[i-1]
    return return_arr

# 91111 -> 95111 , 55911 -> 55951
# find 9's position and (9's position + 1) is '5'
def circuit_3(type_arr):
    return_arr = type_arr.copy()
    position_9 = 9999
    for i in range(len(type_arr)):
        if type_arr[i] == '9':
            position_9 = i
            break
    
    cnt_5 = 0
    if type_arr[position_9+1] == '5':
        for i in range(position_9+1, len(type_arr)):
            if type_arr[i] == '5':
                cnt_5 += 1
            else:
                break
    
    if cnt_5 != 0:
        temp_arr = np.concatenate((type_arr[:position_9 + 1], type_arr[position_9 + 1 + cnt_5:]))
        return_arr = circuit_3(temp_arr)
        if return_arr is None:
            return
        return_arr = np.concatenate((return_arr[:position_9 + 1], ['5'] * cnt_5, return_arr[position_9 + 1:]))
    else:
        return_arr[position_9 + 1] = '5'
    return return_arr

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
decomposition_list(qc, matrix_4)