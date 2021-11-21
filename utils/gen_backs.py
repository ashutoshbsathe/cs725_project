from PIL import Image
import numpy as np
import glob 
import os 

input_width = 256
input_height = 256 
input_glob_pattern = './orig_dataset_rgb_hq/*.png'

outdir = './ppt_backs/'
target_width = 1920
target_height = 1080

num = 20

if not os.path.exists(outdir):
    os.makedirs(outdir)

num_width = target_width // input_width + 1 
num_height = target_height // input_height + 1 

img_list = np.array(glob.glob(input_glob_pattern))

for i in range(num):
    imgs = np.random.choice(img_list, num_width * num_height, replace=False)
    final = np.zeros((num_height * input_height, num_width * input_width, 3))
    for x in range(num_width):
        for y in range(num_height):
            idx = x * num_height + y
            img = np.array(Image.open(imgs[idx]))
            final[y*input_height:(y+1)*input_height, x*input_width:(x+1)*input_width, :] = img 
    print('Generated image of size:', final.shape)
    h, w, c = final.shape 
    if h > target_height:
        # random crop
        h_start = np.random.choice(h - target_height)
        final = final[h_start:h_start+target_height, :, :]
    if w > target_width:
        # random crop 
        w_start = np.random.choice(w - target_width)
        final = final[:, w_start:w_start+target_width, :]
    print('Final image of size:', final.shape)
    Image.fromarray(final.astype(np.uint8)).save(f'{outdir}/{i}.png')
