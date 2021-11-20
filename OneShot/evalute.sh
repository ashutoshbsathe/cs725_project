#!/bin/sh 
set -e 
set -x
for PSI in 0.5 0.6 0.7 0.8 0.9 1.0
do
    stylegan2_pytorch --generate --trunc-psi $PSI --results-dir results_$PSI --num-generate 1000
done
