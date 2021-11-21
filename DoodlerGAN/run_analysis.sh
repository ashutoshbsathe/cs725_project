#!/bin/sh
set -e 
set -x 
for PSI in 0.5 0.6 0.7 0.8 0.9 1.0
do
    python generate_creative_birds.py --models_dir ../../models --results_dir ../../results_32/bird_$PSI/ --data ../../data/ --num_image_tiles 8 --trunc_psi $PSI --generate_all --image_size 32
done
