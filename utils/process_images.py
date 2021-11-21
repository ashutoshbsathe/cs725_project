from data_process import vector_to_raster
import pickle 
import os 
from tqdm import tqdm 
import cv2 

with open('./good_creative_birds.pkl', 'rb') as f:
    data = pickle.load(f)

size=32
output = '../oneshot/orig_dataset/'
output_rgb = '../oneshot/orig_dataset_rgb/'
output_hq = '../oneshot/orig_dataset_hq/'
output_rgb_hq = '../oneshot/orig_dataset_rgb_hq/'

if not os.path.exists(output):
    os.makedirs(output)

if not os.path.exists(output_rgb):
    os.makedirs(output_rgb)

if not os.path.exists(output_hq):
    os.makedirs(output_hq)

if not os.path.exists(output_rgb_hq):
    os.makedirs(output_rgb_hq)

raster_images = vector_to_raster(data, part_label=False, nodetail=True, side=size, line_diameter=3, padding=16, bg_color=(1, 1, 1), fg_color=(0, 0, 0))
raster_images_rgb = vector_to_raster(data, part_label=True, nodetail=True, side=size, line_diameter=3, padding=16, bg_color=(1, 1, 1), fg_color=(0, 0, 0))
raster_images_hq = vector_to_raster(data, part_label=False, nodetail=True, side=size*8, line_diameter=3, padding=16, bg_color=(1, 1, 1), fg_color=(0, 0, 0))
raster_images_rgb_hq = vector_to_raster(data, part_label=True, nodetail=True, side=size*8, line_diameter=6, padding=16, bg_color=(1, 1, 1), fg_color=(0, 0, 0))

for i, (img, img_rgb, img_hq, img_rgb_hq) in enumerate(tqdm(zip(raster_images, raster_images_rgb, raster_images_hq, raster_images_rgb_hq))):
    #cv2.imwrite(os.path.join(output, f'doodle_{i:04d}.png'), img)
    #cv2.imwrite(os.path.join(output_rgb, f'doodle_{i:04d}.png'), img_rgb)
    cv2.imwrite(os.path.join(output_hq, f'doodle_{i:04d}.png'), img_hq)
    cv2.imwrite(os.path.join(output_rgb_hq, f'doodle_{i:04d}.png'), img_rgb_hq)
