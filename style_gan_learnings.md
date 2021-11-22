# Motivation 
1. We want to see if we can generate even higher resolution sketches using ProgressiveGAN like training

# Tricks and Tips on Training

Model was trained in a progressive GAN fashion with size starting from 4 x 4 image, up to 32 x 32 images

- Model learned well enough for 4 x 4 images, with an alpha increment of 1e-3 after every batch.
- However, as a new layer faded in and the generation size increased to 8 x 8, the discriminator got too good too fast causing instability in the generator.

A couple of measures were brought in to tackle this problem - 

[ ] Lower the fade in rate - did not work

[ ] For each training loop of discriminator, train the generator x times, x = 2, 3, 4 - did not work

[ ] Directly train for 8 x 8 - this failed colossally

[ ] Label smoothing - randomly flip the labels of real images (more aptly called One-side label smoothing)

[ ] Noise in real images - introduce Gaussian noise into the real image - make the life of the discriminator tough

The last two had to be tuned over iterations in order to stop the discriminator from collapsing, causing the generator to get noisy feedback. These two eventually led
to better stability in the training procedure when new resolution faded in. However, one aspect of tuning was to decay down the label smoothing and noise introduction.
So they couldn't stabilize the growth of the resolution from 8 x 8 to 16 x 16.

A couple of other things that were tried - 

[ ] Play around with the architecture - no latent space input, and learn only using the conditional input from encoder - couldn't be evaluated 
using a human due to unstable training.

[ ] Play around with the disciminator architecture - to make it less powerful (decreasing conv layers, or number of filters, or number of dense layers at the end).
None worked as good as label smoothing and Gaussian noise injection.

[ ] Losses [D(x) - logit for the real image, x and D(G(z)) - logit for the fake generated image] -

    Wasserstein distance, Critic Loss = - (D(x) - D(G(z))), Generator Loss= - D(g(z))
    Hinge Loss, Critic loss = relu(1 - D(x)) + relu(1 + D(G(z)))
   
   
 # StyleGAN architecture
 
## Overview
 The StyleGAN has been trained in a progressive fashion with the resolution of generated images gradually increasing from 4 x 4 to 16 x 16. New layers are faded in, as can be seen in the origin implementation of Progressive GAN. The Generator is made of successive Synthesis blocks - first block generates 4 x 4 images, the next generates 8 x 8 and so on. Difference from the original StyleGAN - it has been trained in a conditional fashion, with the part sketches providing the conditioning part. Hence the generator attempts to learn the probability distribution <img src="https://render.githubusercontent.com/render/math?math=P(part | partial\_sketch)">
 
## Synthesis block structure

1. Upsampler - `bilinear` upsampling has been used, not a transpose convolution
2. A 3 x 3 convolution network (1 or 2 conv layers within, depending on hyperparam selection)
3. A noise adder - generated noise is constant across batches and channels, a learned per feature map weight vector transforms the noise for each channel/feature map
4. Style modulation - A linear transformation on the latent vector (style) -> amplification of instance normalized feature map values + a bias (computed by the linear transform)
5. A 3 x 3 convolution network (2 conv layers within)
6. A noise adder
7. Style modulation

Corresponding to the growing layers of the generator, there are growing layers of the discriminator - each layer can be called a Discriminator block.

## Discriminator block structure

1. Downsampler - an average pooling layer with kernel_size=2, stride=2
2. A 3 x 3 convolution network (1 or 2 conv layers within, depending on hyperparam selection)

The initial synthesis block contains an additional learned tensor (channel x height x width). And the final discriminator block contains an additional sequential layer consisting of two dense layers for classification.

## Training overview

The model is trained in an incremental fashion - first the weights pertaining to a 4 x 4 image are learnt. Simultaneously the next layer (namely 16 x 16) is faded in with a smoothing factor <img src="https://render.githubusercontent.com/render/math?math=alpha">. The value of  <img src="https://render.githubusercontent.com/render/math?math=alpha"> is gradually incremented (by 1e-3 in the implementation) until the next layer completely dominates. As the training progresses through iterations, layers until the final layer (16 x 16) are faded in.
