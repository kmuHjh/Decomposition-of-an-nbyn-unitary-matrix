import graycode as gc
import numpy as np
def make_twolevel(matrix, del_arr): 
    print(del_arr)
    x = matrix[del_arr[1]][del_arr[0]]
    y = matrix[del_arr[2]][del_arr[0]]
    r = np.sqrt(np.abs(x)**2 + np.abs(y)**2)
    print(x,y)
    x1 = np.real(x)
    x2 = np.imag(x)
    y1 = np.real(y)
    y2 = np.imag(y)

    A = np.array([
        [x1, -x2, y1, -y2],
        [x2, x1, y2, y1],
        [y1, y2, -x1, -x2],
        [y2, -y1, -x2, x1]
        ], dtype=float)
    
    B = np.array([r, 0, 0, 0], dtype=float)
    
    solution = np.linalg.lstsq(A, B, rcond=None)[0]
    a1, a2, b1, b2 = solution

    twolevel = np.identity((np.size(matrix[0])), dtype = complex)
    a = a1 + 1j*a2
    b = b1 + 1j*b2

    twolevel[del_arr[1]][del_arr[1]] = a
    twolevel[del_arr[1]][del_arr[2]] = b
    twolevel[del_arr[2]][del_arr[1]] = -np.conjugate(b)
    twolevel[del_arr[2]][del_arr[2]] = np.conjugate(a)

    return twolevel

def decomposition(matrix):
    n = int(np.log2(matrix.shape[0]))
    gc_arr = gc.get_graycode(n)
    del_arr = gc.get_deleteorder(gc_arr)
    type_arr = gc.get_twoleveltype(del_arr, n)
    temp = make_twolevel(matrix, del_arr[0])
    print(temp)
    print(np.matmul(temp, matrix))
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



decomposition(matrix_4)