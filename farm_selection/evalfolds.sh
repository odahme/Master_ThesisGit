#!/bin/bash
#
source activate Py3Root6
echo "start classifying fold $1"
python /afs/cern.ch/work/o/odahme/private/Master_thesis/selection/clas_fold.py $1
