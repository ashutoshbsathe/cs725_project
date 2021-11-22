This repository contains the code dumps used for our CS725 project titled "*Exploring Generative Adversarial Networks for Doodling*". We mainly explore the following methodologies - 

1. DoodlerGAN - from Facebook Research, can be found under the folder named DoodlerGAN
2. One Step unconditional StyleGAN2 - Code credits - https://github.com/lucidrains/stylegan2-pytorch/tree/master/stylegan2_pytorch, can be found under the folder named OneShot
3. StyleGAN trained in a progressive approach - Swaroop's repo - https://github.com/swaroop-nath/style-gan-doodling, Code inspired by - <a href="https://github.com/aladdinpersson/Machine-Learning-Collection/tree/master/ML/Pytorch/GANs/ProGAN">aladdinperson</a>, <a href="https://github.com/huangzh13/StyleGAN.pytorch/tree/155a923947b873832689b75e47346ea23e0cbb22">Zhonghao</a>, can be found under the folder name StyleGAN

The evaluation results (on metrics like FID, GD) can be found in evaluation/*_fids.log and StyleGAN/gd_scores.log

The demo video can be found under the demo folder. It is a 1 minute video which shows the quality of the generated images and the generation of a doodle using the DoodlerGAN models step by step.

The details of the implementation of StyleGAN that we followed can be found under style_gan_learning.md, along with a brief discussion of what happened in training.
