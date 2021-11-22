#!/bin/sh 

python generate_creative_birds.py \
    --models_dir ../../trained_models/models \
    --results_dir ../demo --data_dir ../../data \
    --num_image_tiles 2
