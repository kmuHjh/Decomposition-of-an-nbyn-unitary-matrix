import graycode as gc
import numpy as np
from scipy.linalg import eig
import math
import cmath

def make_twolevel(matrix, del_arr): 
    x = matrix[del_arr[1]][del_arr[0]]
    y = matrix[del_arr[2]][del_arr[0]]
    r = np.sqrt(np.abs(x)**2 + np.abs(y)**2)
    A = np.array([
        [np.real(x), -np.imag(x), np.real(y), -np.imag(y)],
        [np.imag(x), np.real(x), np.imag(y), np.real(y)],
        [np.real(y), np.imag(y), -np.real(x), -np.imag(x)],
        [np.imag(y), -np.real(y), -np.imag(x), np.real(x)]
        ], dtype=float)
    B = np.array([r, 0, 0, 0], dtype=float)
    a1, a2, b1, b2 = np.linalg.lstsq(A, B, rcond=None)[0]
    twolevel = np.identity((np.size(matrix[0])), dtype = complex)
    a = a1 + 1j*a2
    b = b1 + 1j*b2
    twolevel[del_arr[1]][del_arr[1]] = a
    twolevel[del_arr[1]][del_arr[2]] = b
    twolevel[del_arr[2]][del_arr[1]] = -np.conjugate(b)
    twolevel[del_arr[2]][del_arr[2]] = np.conjugate(a)
    return twolevel

def decomposition_matrix(matrix):
    n = int((matrix.shape[0]))
    final = ((n*(n-1))/2)-1
    det = (np.linalg.det(matrix)).conjugate()
    cnt = 0
    twolevel_arr = []
    return_type_arr = []
    return_tlform = []
    n = int(np.log2(matrix.shape[0]))
    gc_arr = gc.get_graycode(n)
    del_arr = gc.get_deleteorder(gc_arr)
    type_arr = gc.get_twoleveltype(del_arr, n)
    for i in range(len(del_arr)):
        if (np.abs(matrix[del_arr[i][2]][del_arr[i][0]]) == 0):
            cnt += 1
            continue
        temp = make_twolevel(matrix, del_arr[i])
        if cnt == final:
            x = del_arr[i][2]
            y = del_arr[i][1]
            temp[x][x] = det * temp[x][x]
            temp[x][y] = det * temp[x][y]
        twolevel_arr.append(temp.conjugate().transpose())
        return_type_arr.append(type_arr[i])
        return_tlform.append(del_arr[i])
        matrix = np.matmul(temp, matrix)
        cnt += 1
    return twolevel_arr, return_type_arr, return_tlform

def get_Ugate(matrix, tlform):
    ugate = np.identity(2, dtype = complex)
    x = tlform[1]
    y = tlform[2]
    if x>y:
        temp = x
        x = y
        y = temp
    ugate[0][0] = matrix[x][x]
    ugate[0][1] = matrix[x][y]
    ugate[1][0] = matrix[y][x]
    ugate[1][1] = matrix[y][y]
    return ugate

#U to sqrt.(U) using by eigvalue decomposition
def get_sqrtU(matrix):
    eigvals, eigvecs = eig(matrix)
    sqrt_eigvals = np.sqrt(eigvals)
    sqrt_Lambda = np.diag(sqrt_eigvals)
    sqrtU = eigvecs @ sqrt_Lambda @ np.linalg.inv(eigvecs)

    return sqrtU

def solve_unitary(matrix):
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