#!/bin/bash
#

cd /disk/users/odahme/farm_output

for i in {0..9..1}
    do
        sbatch -p long --nodes=1-1 --ntasks=1 --cpus-per-task=4 --mem=8000 /home/uzh/odahme/Master_Thesis/selection/submit.slurm $i
    done

cd -
