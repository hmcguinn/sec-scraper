#! /bin/bash

#SBATCH -p general
#SBATCH -N 1
#SBATCH --mem=8g
#SBATCH -n 1
#SBATCH -c 12
#SBATCH -t 5-
#SBATCH --mail-type=begin,requeue,end
#SBATCH --mail-user=houlton@unc.edu

module add python3
python3 multi.py
