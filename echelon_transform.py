import numpy as np
import sympy as sp


#equations in the form (ax,by,cz,d) --> [1,2,3,4]
#where ax+by+cz=d is the standard equation of a plane
def two_plane_intersection(arr1, arr2):

    matrix = np.array([arr1[0:3], arr2[0:3]])
    #...

def three_plane_intersection(arr1, arr2, arr3):
    
    matrix = np.array([arr1[0:3], arr2[0:3], arr3[0:3]])
    aug_const  = np.array([[arr1[3]], [arr2[3]],[arr3[3]]])

    #convert to agumented arr
    aug_m = np.concatenate((matrix, aug_const), axis = 1)
    #row reduced echelon form
    ref = np.array(sp.Matrix(aug_m).echelon_form())

    z1 = ref[2,3]/ref[2,2]
    #print(ref[2,2], ref[2,3])
   # print(z1)
    y1 = ((ref[1,3]-(ref[1,2]*z1))/(ref[1,1]))
    #print(ref[1,3],(ref[1,2],(ref[1,1])))
    #print(y1)
    x1 = ((ref[0,3]-z1*ref[0,2]-y1*ref[0,1])/(ref[0,0]))
    #print(x1)
    
    '''aug_m_symp = sp.Matrix(aug_m)
    ref = aug_m_symp.echelon_form()
    rref = aug_m_symp.rref()[0]
    print(np.array(ref))
    print(np.array(rref))'''

    print(ref)
    print(aug_m)
    #solution set
    print((x1, y1, z1))
    return(x1, y1, z1)
    #print(matrix)
    #print(aug_const)


if __name__ == "__main__":
    a1 = [1,-1,2,1]
    a2 = [2,1,-1,8]
    a3 = [5,-2,5,11]
    three_plane_intersection(a1, a2, a3)
                    

