#!/bin/bash
#PBS -k o
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:20:00
#PBS -M nathan.lima@wsu.edu
#PBS -m abe
#PBS -N CONTAM_input_${year}_${site}
#PBS -j oe
#PBS -e /home/lima/iaq/input/errors/
#PBS -o /home/lima/iaq/input/scripts/

module load python/3.6.1
python /home/lima/iaq/input/contam.py ${year} ${site}
