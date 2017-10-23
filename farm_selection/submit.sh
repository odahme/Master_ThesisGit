#!/bin/bash
#

cd /disk/users/odahme/farm_output

for i in {0..9..1}
    do
        sbatch -p standard --nodes=1-1 --ntasks=1 --cpus-per-task=24 --mem=60000 /home/uzh/odahme/Master_Thesis/farm_selection/submit.slurm $i 24
    done

cd -
