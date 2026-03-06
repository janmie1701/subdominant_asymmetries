#!/bin/bash
/holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/bilby_pipe_analysis outdir/NRSur_config_complete.ini --outdir outdir --detectors ET1 ET2 ET3 --label NRSur_data0_10-0_analysis_ET --data-dump-file outdir/data/NRSur_data0_10-0_generation_data_dump.pickle --sampler dynesty

