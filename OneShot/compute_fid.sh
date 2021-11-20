#!/bin/sh 
set -e 
set -x
# https://askubuntu.com/a/420983
# Run as `./compute_fid.sh >&1 | tee oneshot_fids.log`
for PSI in 0.5 0.6 0.7 0.8 0.9 1.0
do
    ./fid_score.py --gpu 0 orig_dataset/ results_$PSI/ungrid/
done
