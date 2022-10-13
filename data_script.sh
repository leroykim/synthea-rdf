#!/bin/bash
CURRENT_DIR=`pwd`
CSV_DIR="${CURRENT_DIR}/csv"
cd ~/synthea
for (( i=1 ; i<=$1 ; i++ ));
do
    ~/synthea/run_synthea -p $2;
    cp -a ~/synthea/output/csv/. ~/synthea_rdf/csv/patient_$2_bin_$i
done
cd $CURRENT_DIR
