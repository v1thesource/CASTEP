# Band gap calculator from dos.pl output! By Alexandros Kenich
# Example usage:
# python bandgap_calculator.py dos_output_file

import csv
import sys

#print sys.argv[0] # prints name of script
#print sys.argv[1] # prints var1
#print sys.argv[2] # prints var2 (uncomment if needed)

# Assign the filename to a global variable
dosfile = sys.argv[1]

# Print the list
def printdos(doslist):
        for row in doslist:
                print(row)

# Extract the data from the dos file into a list
def extract_dos(filename):
	readCSV = csv.reader(filename, delimiter=' ', skipinitialspace = True, quoting=csv.QUOTE_NONNUMERIC)
	return list(readCSV)


# Search through the first column of the dos-list 
# for zero (the origin) and then look for the first
# band gap. Return its size in eV

def findzeroenergy(doslist):
	indexnum = 0
	while doslist[indexnum][0] < 0:
		indexnum += 1
	return indexnum


def find_VBM_index(zeroindex, doslist):
	iterator = zeroindex
	while (doslist[iterator][1] != 0) or (doslist[iterator][1] >= doslist[iterator - 1][1]):
		iterator += 1
	if doslist[iterator][1] == doslist[iterator + 5][1]: # So you don't get a minimum with only 4 zeroes
		return iterator
	else:
		iterator += 5
	while (doslist[iterator][1] != 0) or (doslist[iterator][1] >= doslist[iterator - 1][1]):
                iterator += 1
	return iterator


def find_CBM_index(VBMindex, doslist):
	iterator = VBMindex
	while doslist[iterator][1] == 0:
		iterator += 1
	return iterator


def calculate_band_gap(VBMindex, CBMindex, doslist):
	band_gap_value = doslist[CBMindex][0] - doslist[VBMindex][0]
	return band_gap_value


# Start the program
with open(dosfile) as filename:
        doslist = extract_dos(filename)
        #printdos(doslist)
	indexofzero = findzeroenergy(doslist)
	VBMindex = find_VBM_index(indexofzero, doslist)
	CBMindex = find_CBM_index(VBMindex, doslist)
	band_gap = calculate_band_gap(VBMindex, CBMindex, doslist)
	#print '%s is the element number closest to zero' %(indexofzero)
	#print '%s is the actual energy value at that index' %(doslist[indexofzero][0])
	#print '%s is the DOS at that index' %(doslist[indexofzero][1])
	#print '%s is the VBM index, energy at VBM is %s, DOS is %s' %(VBMindex, doslist[VBMindex][0], doslist[VBMindex][1])
	#print '%s is the CBM index, energy at CBM is %s, DOS is %s' %(CBMindex, doslist[CBMindex][0], doslist[CBMindex][1])
	#print 'Band gap is %s eV' %(band_gap)
	print '%s %s' %(dosfile, band_gap)
