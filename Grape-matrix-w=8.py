 #! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import random
from itertools import combinations
from itertools import product
import csv
import os
import galois


# Define the values of x^8 to x^16
#x^8= X^5+X^4+X^3+1 
x8 = 2**5 + 2**4 + 2**3 + 1
x9 = 2**6 + 2**5 + 2**4 + 2
x10 = 2**7 + 2**6 + 2**5 + 2**2
x11 = 2**7 + 2**6 + 2**5 + 2**4 + 1
x12 = 2**7 + 2**6 + 2**4 + 2**3 + 2 + 1
x13 = 2**7 + 2**3 + 2**2 + 2 + 1
x14 = 2**5 + 2**2 + 2 + 1
x15 = 2**6 + 2**3 + 2**2 + 2
x16 = 2**7 + 2**4 + 2**3 + 2**2


list_x=[x8,x9,x10,x11,x12,x13,x14,x15,x16]
list_x_bin=[]
for j in range(len(list_x)):
    print('galois.Poly.Int(list_x[j])','{:08b}'.format((list_x[j])))
    list_x_bin.append('{:08b}'.format((list_x[j])))
print('list_x_bin:',list_x_bin)
all_combinations = list(product([0, 1], repeat=len(list_x)))

def count_ones(binary_number):
    count = 0
    for bit in binary_number:
        if bit == '1':
            count += 1
    return count


def find_one(i, list_x, all_combinations):
    l_ones_count = []  # Number of ones in the 17x1 binary vector after 256 combinations
    l_result_count = []  # 17x1 binary vector result after combining 256 polynomial combinations
    l_high_bin_count = []  # Statistics of the selected high 9 bits binary
    for j in range(len(all_combinations)):  # Iterate through the 256 combinations of 8 polynomials
        result = galois.Poly.Int(i)  # Initialize the result polynomial
        l_list_x_bin = []  # Binary representation of polynomials: ['00111001', '01110010', '11100100', '11110001', '11011011', '10001111', '00100111', '01001110', '10011100']
        l_all_combinations = []
        result_l_list_x_bin = 0  # Polynomial result after combining selected polynomials in all_combinations[j], number of ones in the first eight bits
        for jj in range(len(all_combinations[j])):  # 8 polynomial combinations
            if all_combinations[j][jj] == 1:  # Polynomial is selected
                result += (galois.Poly.Int(list_x[jj] * all_combinations[j][jj]))  # Add the selected polynomial in all_combinations[j]
                if len(l_list_x_bin) == 0:
                    result_l_list_x_bin = int(list_x_bin[jj], 2)
                if len(l_list_x_bin) > 0:
                    num = int(list_x_bin[jj], 2)
                    result_l_list_x_bin ^= num
                l_list_x_bin.append(list_x_bin[jj])
        ones_count = count_ones(('{:08b}'.format(int(result))))  # Number of ones in the 8x8 sum
        l_all_combinations.append(all_combinations[j])
        ones_count_1 = len(l_list_x_bin)  # Number of 1s added in the last 9 rows = number of selected polynomials in all_combinations[j]
        ones_count_2 = ones_count + ones_count_1  # Number of ones in the 17x1 vector
        l_ones_count.append(ones_count_2)  # Number of ones in the 17x1 binary vector after 256 combinations
        reversed_tuple = all_combinations[j][::-1]
        high_result_binary = ''.join(str(bit) for bit in reversed_tuple)
        result_binary = high_result_binary + ('{:08b}'.format(int(result)))  # high_result_binary: last 9 bits binary, ('{:08b}'.format(int(result))): first 8 bits binary
        l_result_count.append(result_binary)  # 17x1 binary vector result after combining 256 polynomial combinations
        l_high_bin_count.append(high_result_binary)  # Statistics of the selected high 9 bits binary
    min_value = min(l_ones_count)
    min_index = l_ones_count.index(min_value)
    return min_value, min_index, l_result_count[min_index], l_high_bin_count[min_index]



def big_matrix(k, r, w, l_result_binary):
    transposed_matrix = []
    original_column = '00000000000000001'
    matrix = []
    
    for i in range(8):
        if i > 0:
            original_column = original_column[1:] + original_column[0]  # Shift left by 1 bit
        matrix.append(list(original_column[::-1]))
    transposed = np.transpose(matrix)
    transposed_1 = transposed
    
    for i in range(k - 1):
        transposed_1 = np.hstack((transposed_1, transposed))
    
    l_original_column_2 = l_result_binary[1]
    
    for i in range(len(l_original_column_2)):
        matrix = []
        original_column = l_original_column_2[i]
        
        for j in range(8):
            if j > 0:
                original_column = original_column[1:] + original_column[0]  # Shift left by 1 bit
            matrix.append(list(original_column[::-1]))
        transposed = np.transpose(matrix)
        
        if i == 0:
            transposed_2 = transposed
        if i > 0:
            transposed_2 = np.hstack((transposed_2, transposed))
    
    if len(l_result_binary) == 1:
        transposed_matrix = np.vstack((transposed_1, transposed_2))
    
    if len(l_result_binary) == 2:
        l_original_column_3 = l_result_binary[2]       
        for i in range(len(l_original_column_3)):
            matrix = []
            original_column = l_original_column_3[i]            
            for j in range(8):
                if j > 0:
                    original_column = original_column[1:] + original_column[0]  # Shift left by 1 bit
                matrix.append(list(original_column[::-1]))
            transposed = np.transpose(matrix)           
            if i == 0:
                transposed_3 = transposed
            if i > 0:
                transposed_3 = np.hstack((transposed_3, transposed))        
        transposed_4 = np.vstack((transposed_1, transposed_2, transposed_3))
        transposed_matrix = transposed_4
    
    if len(l_result_binary) == 3:
        l_original_column_3 = l_result_binary[2]        
        for i in range(len(l_original_column_3)):
            matrix = []
            original_column = l_original_column_3[i]           
            for j in range(8):
                if j > 0:
                    original_column = original_column[1:] + original_column[0]  # Shift left by 1 bit
                matrix.append(list(original_column[::-1]))
            transposed = np.transpose(matrix)            
            if i == 0:
                transposed_3 = transposed
            if i > 0:
                transposed_3 = np.hstack((transposed_3, transposed))       
        l_original_column_4 = l_result_binary[3]       
        for i in range(len(l_original_column_4)):
            matrix = []
            original_column = l_original_column_4[i]           
            for j in range(8):
                if j > 0:
                    original_column = original_column[1:] + original_column[0]  # Shift left by 1 bit
                matrix.append(list(original_column[::-1]))
            transposed = np.transpose(matrix)           
            if i == 0:
                transposed_4 = transposed
            if i > 0:
                transposed_4 = np.hstack((transposed_4, transposed))       
        transposed_5 = np.vstack((transposed_1, transposed_2, transposed_3, transposed_4))
        print('transposed_4', transposed_5)
        transposed_matrix = transposed_5
    
    csv_file = str(k) + '-' + str(r) + '-' + str(w) + "ring_matrix.csv"    
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(transposed_matrix)    
    print(f"The transformed large matrix has been written to {csv_file}")
    print('transposed_1', transposed_matrix)   
    count_ones_transposed_matrix = np.sum(np.array(transposed_1) == '1')
    print(f"Number of ones in count_ones_transposed_matrix: {count_ones_transposed_matrix}")

def generate_vandermonde_matrix(rows, cols):
    GF256 = galois.GF(256, irreducible_poly=[1, 0, 0, 1, 1, 1, 0, 0, 1]) 
    primitive_element = GF256.primitive_element
    print('primitive element:', primitive_element)
    vander_matrix = GF256.Vandermonde(primitive_element, cols, rows).T
    return vander_matrix

def main():
    w = 8
    r = 3
    k= 10
    vander_matrix = generate_vandermonde_matrix(r, k)
    print('Vandermonde matrix:', vander_matrix)
    l_dict = {}
    l_result_binary = {}
    idx = 0
    for row in vander_matrix:
        print('row:', row)
        l_result_binary_value = []
        if idx > 0:
            for elem in row:
                print('element:', elem)
                elem = int(elem)
                binary_elem = '{:08b}'.format(elem)
                high_binary_string = '000000000'  # Initialize the last 9 bits of the binary string
                original_bin = high_binary_string + binary_elem
                l_key_value = []
                min_value, min_index, result_binary, high_bin = find_one(elem, list_x, all_combinations)
                l_key_value.append(result_binary)  # 17x1 vector result
                l_dict[elem] = l_key_value
                l_result_binary_value.append(result_binary)

        if idx > 0:
            print('l_result_binary_value:', l_result_binary_value)
            l_result_binary[idx] = l_result_binary_value
        idx += 1

    big_matrix(k, r, w, l_result_binary)

if __name__ == "__main__":
    main()
