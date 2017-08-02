#!/bin/bash

# This script runs the Brouwer diagram script at temperature $temp and the smallest possible $Convergence.
# It will append the Brouwer diagram data to datadump.txt, and then increment $temp by $temp_increment

temp="300"
temp_maximum="2500"
Convergence=1e-40
temp_increment="5"

while [ "$(bc <<< "$temp < $temp_maximum") == "1" ]
do
  perl defect_analysis3.pl intrinsic > failure.test
  echo Temperature = $temp
  echo Convergence = $Convergence
  if grep -Fxq "Could not deteremine the Fermi level that gives charge neutrality, recommned you examine your DFT energies" ./failure.test
  then
  sed -i -e "s/Convergence : $Convergence/Convergence : $(python<<<"print($Convergence*10)")/g" intrinsic.input
  Convergence=$(python<<<"print($Convergence*10)")
  else
  cat intrinsic.res >> datadump.txt
  sed -i -e "s/Temperature : $temp/Temperature : $( bc <<< "$temp + $temp_increment" )/g" intrinsic.input
  temp=$( bc <<< "$temp + $temp_increment" )
  fi
done
