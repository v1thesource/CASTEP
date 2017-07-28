# Turn lattice vectors (3x3 matrices) into lattice parameters! By Alexandros Kenich
# Version 0.1. For usage with CASTEP .cell files
# Example usage:
# python vector2abc.py filename.cell

import csv
import sys
import math

#print sys.argv[0] # prints name of script
#print sys.argv[1] # prints argument1
#print sys.argv[2] # prints argument2 (uncomment if needed)

# Assign the filename (argument1) to a global variable
cellfile = sys.argv[1]

# Extract vectors in a matrix of string values
def matrix_as_string(filename):
	"""
	Cell file looks like this:

	%BLOCK lattice_cart
 	10.3706750000000003  0.0205487000000000 -0.1007824000000000
 	-0.0212244000000000 10.4725819999999992 -0.0265279000000000
 	-1.7037192999999999  0.0229314000000000 10.6187673000000000
	%ENDBLOCK lattice_cart
	
	"""
	matrix = [] # Initialise matrix as list
	indexnum = -1 # Index number, we count from 0
	listoflines = list(filename) # Turn file into list of lines
	for line in map(str.upper, listoflines):
		indexnum += 1
		if "%BLOCK LATTICE_CART" in line:
			matrix.append(str.split(listoflines[indexnum+1]))
			matrix.append(str.split(listoflines[indexnum+2]))
			matrix.append(str.split(listoflines[indexnum+3]))
	return matrix

# Turn string matrix into float matrix
def floatify(matrix_as_string):
	for x in range(3):
		for y in range(3):
			matrix_as_string[x][y] = float(matrix_as_string[x][y])
	return matrix_as_string

# Helper function for vector magnitudes
def __pythagoras(a,b,c):
	magnitude = (a**2 + b**2 + c**2)**0.5
	return magnitude

# Get lattice parameters from matrix
def lattice_params(matrix_as_float):
	a_param = __pythagoras((matrix_as_float[0][0]),(matrix_as_float[0][1]),(matrix_as_float[0][2]))
	b_param = __pythagoras((matrix_as_float[1][0]),(matrix_as_float[1][1]),(matrix_as_float[1][2]))
	c_param = __pythagoras((matrix_as_float[2][0]),(matrix_as_float[2][1]),(matrix_as_float[2][2]))
	return a_param, b_param, c_param

# Get angles alpha/beta/gamma. These come from the dot product of vectors:
# a.b = |a||b|cos(theta). Yes numpy has np.dot, but I assume you don't have numpy.
def angles(matrix_as_float):
	a,b,c = lattice_params(matrix_as_float)
	dot_bc = sum(matrix_flt[1][i]*matrix_flt[2][i] for i in range(3))
	dot_ac = sum(matrix_flt[0][i]*matrix_flt[2][i] for i in range(3))
	dot_ab = sum(matrix_flt[0][i]*matrix_flt[1][i] for i in range(3))
	alpha_rad = math.acos(dot_bc/(b*c))
	beta_rad  = math.acos(dot_ac/(a*c))
	gamma_rad = math.acos(dot_ab/(a*b))
	alpha = alpha_rad*180/math.pi
	beta  = beta_rad *180/math.pi
	gamma = gamma_rad*180/math.pi
	return alpha, beta, gamma

# Start the program
with open(cellfile) as filename:
    matrix_str = matrix_as_string(filename)
    #print matrix_str[0][0] + matrix_str[0][2] # Check if it concatenates 
    matrix_flt = floatify(matrix_str)
    #print matrix_flt[0][0] + matrix_flt[0][2] # Check if it sums
    a,b,c = lattice_params(matrix_flt)
    alpha,beta,gamma = angles(matrix_flt)
    print a,b,c,alpha,beta,gamma
    
