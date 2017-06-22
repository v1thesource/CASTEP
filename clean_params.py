# Remove those pesky duplicates from .param files! By Alexandros Kenich
# Version 0.1. For usage with CASTEP .param files
# Example usage:
# python clean_params.py filename.param

import csv
import sys
import math

#print sys.argv[0] # prints name of script
#print sys.argv[1] # prints argument1
#print sys.argv[2] # prints argument2 (uncomment if needed)

# Assign the filename (argument1) to a global variable
paramfile = sys.argv[1]

# Generate a cleaned up linelist without duplicates if necessary
def cleanup_duplicate_lines(filename):
	seen = list() # A set where we append seen lines
	for line in filename:
		line_lower = line.lower() # Ignore case, make everything lower
		line_lower = line_lower.rstrip('\n') # \n is automatically appended to each line, remove it
		if line_lower == '': # Special case for empty lines, you want to keep duplicates
			seen.append(line_lower)
		elif line_lower in seen:
			continue
		else:
			seen.append(line_lower)
	if seen == set():
		return "No duplicates"
	else:
		return seen

# Replace all lines in a file
def replace_lines(original,replacement):
    original.seek(0)
    original.truncate()
    for line in replacement:
    	print>>original, line
    	

# Start the program
with open(paramfile, "r+") as filename:
    cleanup = cleanup_duplicate_lines(filename)
    if cleanup == "No duplicates":
    	sys.exit()
    else:
    	replace_lines(filename, cleanup)

