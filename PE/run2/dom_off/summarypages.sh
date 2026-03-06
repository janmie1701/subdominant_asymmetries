#!/bin/bash -l

/holohome/jannik.mielke/anaconda3/envs/bilby_asym/bin/summarypages \
--samples /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/outdir/final_result/dom_off_data0_10-0_analysis_ET_result.json \
--webdir /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/webdir \
--gw \
--no_ligo_skymap \
--disable_interactive \
--multi_process 6 \
--config /holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/outdir/dom_off_config_complete.ini \
--psd ET1:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/ET_D_psd.txt ET2:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/ET_D_psd.txt ET3:/holohome/jannik.mielke/subdom_asym/PE/bilby_asym/run2/dom_off/ET_D_psd.txt \
--labels dom_off \
--f_low 20 \
--redshift_method exact \
--evolve_spins_forwards

