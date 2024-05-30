import numpy as np
import decompoisition_nqubit as dn


#twolevel_arr : U1^d,U2^d...Un^d (data type : array [n][n])
#type_arr : 109, 191, 119 (data type : array str)
#tlform : 054, 075, 067 (data type : array int)
#main input function
def decomposition_gate(matrix):
    twolevel_arr, type_arr, tlform_arr = dn.decomposition_matrix(matrix)
    print(twolevel_arr)
    print('d')
    print(type_arr)
    print('d')
    print(tlform_arr)
    return 0