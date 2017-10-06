#!/bin/bash
#
#SBATCH -J classifying
#SBATCH --mail-type=end
#SBATCH --mail-user=oliver.dahme@uzh.ch
# Make sure we are in the right directory in case writing files
  mkdir -p /scratch/$USER/$SLURM_JOB_ID
  cd /scratch/$USER/$SLURM_JOB_ID
  source activate Py3Root6

  # Run actual commands here
  echo "my username is " $USER
  echo "start classifying fold $1"
  python /home/uzh/odahme/Master_Thesis/farm_selection/clas_fold.py $1 $2
  # Remove scratch directory at the end of your job
  # Do not forget to copy any output first to a safe place
  cd
  rm -rf /scratch/$USER/$SLURM_JOB_ID

