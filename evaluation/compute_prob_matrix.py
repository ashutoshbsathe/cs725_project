import glob 
import numpy as np 
import matplotlib.pyplot as plt
src_path = '../../results_32/bird_{psi}/DoodlerGAN_all/part_gen/'
partlist = 'generated*.txt'
allparts = 'all_parts.txt'

for psi in [0.5, 0.6, 0.7, 0.8, 0.9]:
    with open(src_path.format(psi=psi) + allparts, 'r') as f:
        curr_parts_list = f.readlines()
    probs = np.zeros((len(curr_parts_list), len(curr_parts_list)))
    num_parts_used = np.zeros(len(curr_parts_list)+1)
    step_part_distribution = np.zeros((10, len(curr_parts_list)))
    for partorder_file in glob.glob(src_path.format(psi=psi) + partlist):
        with open(partorder_file, 'r') as f:
            partorder = f.readlines()
        num_parts_used[len(partorder)] += 1
        if len(partorder) == 0:
            continue
        last_part_idx = curr_parts_list.index(partorder[0])
        last_i = 0
        step_part_distribution[last_i, last_part_idx] += 1
        for part in partorder[1:]:
            curr_part_idx = curr_parts_list.index(part)
            probs[last_part_idx, curr_part_idx] += 1
            step_part_distribution[last_i+1, curr_part_idx] += 1
            last_part_idx = curr_part_idx
            last_i += 1
    step_part_distribution /= np.tile(step_part_distribution.sum(axis=1), (len(curr_parts_list), 1)).T
    probs /= np.tile(probs.sum(axis=1), (len(curr_parts_list), 1)).T
    print(num_parts_used)
    print(probs)
    print(step_part_distribution)
    plt.clf()
    plt.matshow(probs)
    plt.xticks(range(len(curr_parts_list)), labels=curr_parts_list, rotation='vertical')
    plt.yticks(range(len(curr_parts_list)), labels=curr_parts_list)
    plt.savefig(f'probs_{psi}.pdf', bbox_inches='tight', dpi=300)
    plt.clf()
    plt.matshow(step_part_distribution.T)
    plt.xticks(range(10), labels=[f'Step {i+1}' for i in range(10)], rotation='vertical')
    plt.yticks(range(len(curr_parts_list)), labels=curr_parts_list)
    plt.savefig(f'stepwise_part_distribution_{psi}.pdf', bbox_inches='tight', dpi=300)
    print(64*'-')

