#!/bin/bash 
#SBATCH --job-name=rnd_interpolate
#SBATCH --nodes=1                
#SBATCH --ntasks=1             
#SBATCH --cpus-per-task=80 
#SBATCH --output=magic_factors.out
#SBATCH --error=magic_factors.err
#SBATCH --time=240:00:00
#SBATCH --mail-user=jannik.mielke@aei.mpg.de
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL

echo $(date) $1
python3 -u mf_generator.py > magic_factors.out
echo $(date) $1
