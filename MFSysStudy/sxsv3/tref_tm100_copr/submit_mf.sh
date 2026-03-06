#!/bin/bash 
#SBATCH --job-name=tref_tm100_copr
#SBATCH --nodes=1                
#SBATCH --ntasks=1             
#SBATCH --cpus-per-task=80 
#SBATCH --output=out.out
#SBATCH --error=err.err
#SBATCH --time=100:00:00
#SBATCH --mail-user=jannik.mielke@aei.mpg.de
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL

echo $(date) $1
python3 -u mf_generator.py > out.out
echo $(date) $1
