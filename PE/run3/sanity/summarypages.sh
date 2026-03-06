#!/bin/bash -l

/holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/summarypages \
--samples /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/outdir/final_result/sanity_data0_10-0_analysis_ET_result.json \
--webdir /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/webdir \
--gw \
--no_ligo_skymap \
--disable_interactive \
--multi_process 6 \
--config /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/outdir/sanity_config_complete.ini \
--psd ET1:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/ET_D_psd.txt ET2:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/ET_D_psd.txt ET3:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run3/sanity/ET_D_psd.txt \
--labels sanity \
--f_low 20 \
--redshift_method exact \
--evolve_spins_forwards

