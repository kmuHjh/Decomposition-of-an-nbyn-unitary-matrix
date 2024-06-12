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
    for i in reversed(range(len(twolevel_arr))):
        new_arr = swap(qc, type_arr[i])
        matrix_U = dm.get_Ugate(twolevel_arr[i], tlform_arr[i])
        decomposition_nqubit(qc, new_arr, matrix_U)
        new_arr = swap(qc, type_arr[i])
        
def decomposition_nqubit(qc, type_arr, U):
    n_circuit = count_circuit(type_arr)
    X = np.array([[0, 1],[1, 0]])
    V = dm.get_sqrtU(U)
    if n_circuit < 2:
        return
    elif n_circuit == 2:
        decomposition_2qubit(qc, type_arr, U)
    elif n_circuit >= 3:
        decomposition_2qubit(qc, circuit_1(type_arr), V)
        decomposition_nqubit(qc, circuit_2(type_arr), X)
        decomposition_2qubit(qc, circuit_1(type_arr), V.conjugate().transpose())
        decomposition_nqubit(qc, circuit_2(type_arr), X)
        decomposition_nqubit(qc, circuit_3(type_arr), V)


def decomposition_2qubit(qc, type_arr, U):
    alpha, beta, gamma, pi_v = dm.solve_unitary(U)
    p_control = -1
    p_target = -1
    control_type = -1
    for i in range(len(type_arr)):
        if type_arr[i] == '9':
            p_target = i
            break
    for i in range(len(type_arr)):
        if type_arr[i] == '0' or type_arr[i] == '1':
            p_control = i
            if type_arr[i] == '0':
                control_type = 0
            else:
                control_type = 1
            break
    
    qc.rz((alpha-gamma)/2, p_target)
    xgate(qc, control_type, p_control)
    qc.cx(p_control, p_target)
    xgate(qc, control_type, p_control)
    qc.rz((alpha+gamma)/2, p_target)
    qc.ry(beta/2, p_target)
    xgate(qc, control_type, p_control)
    qc.cx(p_control, p_target)
    xgate(qc, control_type, p_control)
    qc.ry(-beta/2, p_target)
    qc.rz(-alpha, p_target)
    qc.p(pi_v, p_control)
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
    if position_9 < len(type_arr) - 1 and type_arr[position_9 + 1] == '5':
        for i in range(position_9 + 1, len(type_arr)):
            if type_arr[i] == '5':
                cnt_5 += 1
            else:
                break
    
    if cnt_5 != 0:
        for i in range(position_9 + cnt_5 + 1, len(type_arr)):
            if type_arr[i] == '1' or type_arr[i] == '0':
                position_1 = i
                break
        for i in range(position_1 + 1, len(type_arr)):
            return_arr[i] = '5'
    else:
        for i in range(len(type_arr)):
            if type_arr[i] == '1' or type_arr[i] == '0':
                position_1 = i
                break
        for i in range(position_1 + 1, len(type_arr)):
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
        position_5 = 9999
        for i in range(len(type_arr)):
            if type_arr[i] == '5':
                if i > position_9:
                    position_5 = i
                    break
        temp_arr = np.concatenate((type_arr[:position_9 + 1], type_arr[position_9 + 1 + cnt_5:]))
        new_return_arr = temp_arr.copy()
        position_99 = 9999
        for i in range(len(temp_arr)):
            if temp_arr[i] == '9':
                position_99 = i
                break
        new_return_arr[position_9] = '5'
        new_return_arr[position_9+1] = '9'
        final_arr =  np.concatenate((new_return_arr[:position_5 ], ['5'] * cnt_5, new_return_arr[position_5 :]))
        return final_arr
    else:
        return_arr[position_9] = '5'
        return_arr[position_9+1] = '9'
    
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
    if position_9 < len(type_arr) - 1:
        for i in range(position_9 + 1, len(type_arr)):
            if type_arr[i] == '5':
                cnt_5 += 1
            else:
                break

    if cnt_5 != 0:
        temp_arr = np.concatenate((type_arr[:position_9 + 1], type_arr[position_9 + 1 + cnt_5:]))
        for i in range(len(temp_arr)):
            if temp_arr[i] == '9':
                position_99 = i
                break
        temp_arr[position_99 + 1] = '5'
        return_arr = np.concatenate((temp_arr[:position_99 + 1], ['5'] * cnt_5, temp_arr[position_99 + 1:]))
    else:
        if position_9 + 1 < len(return_arr):
            return_arr[position_9 + 1] = '5'
    
    return return_arr

def count_circuit(type_arr):
    total = len(type_arr)
    n_5 = 0
    for i in range(total):
        if type_arr[i] == '5':
            n_5 = n_5 + 1
    
    return total - n_5 

def swap(qc, type_arr):
    return_arr = type_arr.copy()
    if type_arr[0] == '9':
        return return_arr
    target_position = 9999
    for i in range(len(type_arr)):
        if type_arr[i] == '9':
            target_position = i
            break
    if type_arr[0] != '9':
        origin_0 = type_arr[0]
        return_arr[target_position] = origin_0
        return_arr[0] = '9'
        qc.cx(target_position, 0)
        qc.cx(0, target_position)
        qc.cx(target_position, 0)
    return return_arr
    
#This x gate is for anti control bit.
def xgate(qc, control_type, p_control):
    if control_type == 0:
        qc.x(p_control)