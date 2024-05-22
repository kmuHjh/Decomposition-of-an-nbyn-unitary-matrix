import numpy as np

def recursive(arr):
    new_arr = []
    size = np.size(arr)
    for i in range(size):
        temp = str(arr[i])
        temp = '0' + temp
        new_arr.append(temp)
    for i in range(size-1,-1,-1):
        temp = str(arr[i])
        temp = '1' + temp
        new_arr.append(temp)

    return new_arr        

#return gray code decimal array
def get_graycode(n):
    arr = [0, 1]
    if n >= 2:
        for i in range(n-1):
            arr = recursive(arr)
    for i in range(np.size(arr)):
        temp = int(arr[i],2)
        arr[i] = temp

    return arr

#return delete order using by two level unitary matrix
#(i,j,k) i = column , (j,k) = two level unitary matrix form
#use (j,k) form and delete (k,i) position of input matrix 
def get_deleteorder(graycode):
    gc_arr = graycode
    del_arr = []
    while len(gc_arr) > 1:
        for i in range(len(gc_arr) - 1, 0, -1):  
            del_arr.append([gc_arr[0],gc_arr[i-1], gc_arr[i]])
        gc_arr = np.delete(gc_arr, 0)
    return del_arr

#test set
'''
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

print(np.matmul(matrix_4,matrix_4.conjugate().transpose()))

gc_arr = get_graycode(2)
del_arr = get_deleteorder(gc_arr)

for i in range(len(del_arr)):
    print(del_arr[i])
'''