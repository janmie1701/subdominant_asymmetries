#!/usr/bin/env bash

# subdom_off_data0_10-0_analysis_ET
# PARENTS 
# CHILDREN subdom_off_data0_10-0_analysis_ET_final_result subdom_off_data0_10-0_analysis_ET_plot
if [[ "subdom_off_data0_10-0_analysis_ET" == *"$1"* ]]; then
    echo "Running: /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_pipe_analysis outdir/subdom_off_config_complete.ini --outdir outdir --detectors ET --label subdom_off_data0_10-0_analysis_ET --data-dump-file outdir/data/subdom_off_data0_10-0_generation_data_dump.pickle --sampler dynesty"
    /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_pipe_analysis outdir/subdom_off_config_complete.ini --outdir outdir --detectors ET --label subdom_off_data0_10-0_analysis_ET --data-dump-file outdir/data/subdom_off_data0_10-0_generation_data_dump.pickle --sampler dynesty
fi

# subdom_off_data0_10-0_analysis_ET_final_result
# PARENTS subdom_off_data0_10-0_analysis_ET
# CHILDREN 
if [[ "subdom_off_data0_10-0_analysis_ET_final_result" == *"$1"* ]]; then
    echo "Running: /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_result --result outdir/result/subdom_off_data0_10-0_analysis_ET_result.json --outdir outdir/final_result --extension json --max-samples 20000 --lightweight --save"
    /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_result --result outdir/result/subdom_off_data0_10-0_analysis_ET_result.json --outdir outdir/final_result --extension json --max-samples 20000 --lightweight --save
fi

# subdom_off_data0_10-0_analysis_ET_plot
# PARENTS subdom_off_data0_10-0_analysis_ET
# CHILDREN 
if [[ "subdom_off_data0_10-0_analysis_ET_plot" == *"$1"* ]]; then
    echo "Running: /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_pipe_plot --result outdir/result/subdom_off_data0_10-0_analysis_ET_result.json --outdir outdir/result --waveform --format png"
    /holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_pipe_plot --result outdir/result/subdom_off_data0_10-0_analysis_ET_result.json --outdir outdir/result --waveform --format png
fi

