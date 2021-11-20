from PIL import Image
import numpy as np 
import glob 
import os 
src_paths = [
    './results_0.5/default/',
    './results_0.6/default/',
    './results_0.7/default/',
    './results_0.8/default/',
    './results_0.9/default/',
    './results_1.0/default/',
]
dest_paths = [
    './results_0.5/ungrid/',
    './results_0.6/ungrid/',
    './results_0.7/ungrid/',
    './results_0.8/ungrid/',
    './results_0.9/ungrid/',
    './results_1.0/ungrid/',
]
max_i = 100
for i in range(max_i):
    for j in range(6):
        assert len(glob.glob(src_paths[j] + f'*-{i}.jpg')) == 1, f'{src_paths[j]}, {i}'

print('Verification done')

for k, src in enumerate(src_paths):
    results = []
    for idx in range(max_i):
        path = glob.glob(src + f'*-{idx}.jpg')[0]
        img = np.array(Image.open(path))[2:-2, 2:-2]

        for i in range(0, 270, 34):
            for j in range(0, 270, 34):
                results.append(img[i:i+32, j:j+32])

    results = np.stack(results, 0)
    if not os.path.exists(dest_paths[k]):
        os.makedirs(dest_paths[k])
    for idx, img in enumerate(results):
        Image.fromarray(img).save(dest_paths[k] + f'/{idx:04d}.png')

    print(src, ' done')

