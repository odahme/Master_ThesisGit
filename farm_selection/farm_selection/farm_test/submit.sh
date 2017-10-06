#!/bin/bash
#

cd /disk/users/odahme/farm_output
i
for i in {0..9..1}
    do
        sbatch -p long --nodes=1-1 --ntasks=1 --cpus-per-task=24 --mem=60000 /home/uzh/odahme/Master_Thesis/selection/farm_test/submit.slurm $i 24
    done

cd -
