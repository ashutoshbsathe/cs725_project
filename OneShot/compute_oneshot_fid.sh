#!/bin/sh 
set -e 
set -x
# https://askubuntu.com/a/420983
# Run as `./compute_fid.sh >&1 | tee oneshot_fids.log`
for PSI in 0.5 0.6 0.7 0.8 0.9 1.0
do
    ./fid_score.py --gpu 0 ../../raw_data/oneshot/orig_dataset_bw/ ../../raw_data/oneshot/results_$PSI/ungrid/ --dims 192
done
