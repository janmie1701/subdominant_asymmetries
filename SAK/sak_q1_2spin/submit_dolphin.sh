#!/bin/bash 
#SBATCH --job-name=sak_q1_2spin
#SBATCH --nodes=1                
#SBATCH --ntasks=1             
#SBATCH --cpus-per-task=80 
#SBATCH --output=dolphin_NRSur.out
#SBATCH --error=dolphin_NRSur.err
#SBATCH --time=100:00:00
#SBATCH --mail-user=jannik.mielke@aei.mpg.de
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=REQUEUE
#SBATCH --mail-type=ALL

echo $(date) $1
python3 -u dolphin_generator_NRSur.py > dolphin_NRSur.out
echo $(date) $1
