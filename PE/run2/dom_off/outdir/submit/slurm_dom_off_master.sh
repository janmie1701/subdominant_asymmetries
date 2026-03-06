#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00
#SBATCH --output=outdir/submit/dom_off_master_slurm.out
#SBATCH --error=outdir/submit/dom_off_master_slurm.err
#SBATCH --job-name=dom_off_master

jid0=($(sbatch --nodes=1 --ntasks-per-node=80 --time=10-00:00:00 --output=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET.out --error=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET.err --job-name=dom_off_data0_10-0_analysis_ET outdir/submit/dom_off_data0_10-0_analysis_ET.sh))

echo "jid0 ${jid0[-1]}" >> outdir/submit/slurm_ids

jid1=($(sbatch --nodes=1 --ntasks-per-node=1 --time=1:00:00 --output=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET_final_result.out --error=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET_final_result.err --job-name=dom_off_data0_10-0_analysis_ET_final_result --dependency=afterok:${jid0[-1]} outdir/submit/dom_off_data0_10-0_analysis_ET_final_result.sh))

echo "jid1 ${jid1[-1]}" >> outdir/submit/slurm_ids

jid2=($(sbatch --nodes=1 --ntasks-per-node=1 --time=1:00:00 --output=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET_plot.out --error=outdir/log_data_analysis/dom_off_data0_10-0_analysis_ET_plot.err --job-name=dom_off_data0_10-0_analysis_ET_plot --dependency=afterok:${jid0[-1]} outdir/submit/dom_off_data0_10-0_analysis_ET_plot.sh))

echo "jid2 ${jid2[-1]}" >> outdir/submit/slurm_ids
