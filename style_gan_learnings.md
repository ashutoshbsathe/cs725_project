Model was trained in a progressive GAN fashion with size starting from 4 x 4 image, up to 32 x 32 images

Initial iteration - 
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
   
