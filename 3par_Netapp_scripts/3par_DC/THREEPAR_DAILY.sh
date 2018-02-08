#!/bin/bash

##############################################################################
# Set up the list of scripts to process
##############################################################################
FILE_LOC="/data01/home/svmso/vdi/bin"
FILE_LST=(
           load_THREEPAR_DEVICE.pl
           load_THREEPAR_LUNS.pl
           load_THREEPAR_ACTIVITY.pl
          )

##############################################################################
#  Iterate through our file list and execute each of the scripts in order
##############################################################################
for file in "${FILE_LST[@]}"
do
    $FILE_LOC/$file
done
