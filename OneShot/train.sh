#!/bin/sh 

stylegan2_pytorch --data ./orig_dataset/ --num-train-steps 55000 --image-size 32 --batch-size 16
