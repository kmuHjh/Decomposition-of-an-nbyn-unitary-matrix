import graycode as gc
import numpy as np

def decomposition(matrix):
    n = int(np.log2(matrix.shape[0]))
    gc_arr = gc.get_graycode(n)
    del_arr = gc.get_deleteorder(gc_arr)
    type_arr = gc.get_twoleveltype(del_arr, n)
    print(gc_arr)
    print('**')
    print(del_arr)
    print('**')
    print(type_arr)


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



decomposition(matrix_8)