import glob 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.colors as colors 
src_path = '../../results_32/bird_{psi}/DoodlerGAN_all/part_gen/'
partlist = 'generated*.txt'
allparts = 'all_parts.txt'

max_steps = 8

def truncated_colormap(cmap_name, minval=0.0, maxval=0.0, n=100):
    # https://stackoverflow.com/a/18926541
    cmap = plt.get_cmap(cmap_name)
    return colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n))
    )
    
    

for psi in [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    with open(src_path.format(psi=psi) + allparts, 'r') as f:
        curr_parts_list = [line.strip() for line in f.readlines()]
    curr_parts_list.remove('none')
    probs = np.zeros((len(curr_parts_list), len(curr_parts_list)))
    num_parts_used = np.zeros(len(curr_parts_list)+1)
    step_part_distribution = np.zeros((max_steps, len(curr_parts_list)))
    for partorder_file in glob.glob(src_path.format(psi=psi) + partlist):
        with open(partorder_file, 'r') as f:
            partorder = [line.strip() for line in f.readlines()]
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
    plt.clf()
    plt.matshow(probs, cmap=truncated_colormap('GnBu', 0.0, 0.5))
    for i in range(len(probs)):
        for j in range(len(probs[0])):
            plt.text(j, i, f'{probs[i, j]:.2f}', ha='center', va='center')
    plt.xticks(range(len(curr_parts_list)), labels=curr_parts_list, rotation=45)
    plt.yticks(range(len(curr_parts_list)), labels=curr_parts_list)
    plt.xlabel('Next part')
    plt.ylabel('Current part')
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.title(r'$\Pr(Next\;part|Current\;part)$')
    plt.savefig(f'probs_{psi}.pdf', bbox_inches='tight', dpi=300)
    plt.clf()
    plt.matshow(step_part_distribution.T, cmap='Wistia')
    for i in range(len(step_part_distribution.T)):
        for j in range(len(step_part_distribution.T[0])):
            plt.text(j, i, f'{step_part_distribution.T[i, j]:.2f}', ha='center', va='center')
    plt.xticks(range(max_steps), labels=[f'Step {i+1}' for i in range(max_steps)], rotation=45)
    plt.yticks(range(len(curr_parts_list)), labels=curr_parts_list)
    plt.title('\n'.join([f'{int(x)} sketches use {i} parts' for (i, x) in filter(lambda x: x[1] > 0, list(enumerate(num_parts_used)))]))
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.savefig(f'stepwise_part_distribution_{psi}.pdf', bbox_inches='tight', dpi=300)
    print(num_parts_used)
    print(64*'-')

