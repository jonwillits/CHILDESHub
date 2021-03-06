import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from childeshub.hub import Hub

# CORPUS_NAMES = ['childes-20180315', 'childes-20180319']
P_NOISES = ['no_o', 'all_1', 'all_2', 'all_3', 'all_4']
WINDOW_SIZE = 2


def calc_num_shared_io_mappings(p):  # TODO speedup usign just probe windows
    windows_mat = hub.make_windows_mat(p, hub.num_windows_in_part)[:, -WINDOW_SIZE:]

    u = np.unique(windows_mat, axis=0)
    result = len(windows_mat) - len(u)

    print(len(windows_mat), len(u), result)

    return result


# make data
ys_list = []
for p_noise in P_NOISES:
    hub = Hub(mode='sem',
              num_parts=2,
              part_order='inc_age',
              corpus_name='childes-20180315',
              p_noise=p_noise)
    y1 = calc_num_shared_io_mappings(hub.reordered_partitions[0])
    y2 = calc_num_shared_io_mappings(hub.reordered_partitions[1])
    ys_list.append((y1, y2))

# fig
bar_width0 = 0.0
bar_width1 = 0.25
_, ax = plt.subplots(dpi=192)
plt.title('window_size={}'.format(WINDOW_SIZE))
ax.set_ylabel('Number of Re-occurring IO Mappings')
ax.set_xlabel('punctuation')
ax.set_xlabel('p_noise')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='both', top='off', right='off')
num_conditions = len(P_NOISES)
xs = np.arange(1, num_conditions + 1)
ax.set_xticks(xs)
ax.set_xticklabels(P_NOISES)
# plot
colors = sns.color_palette("hls", 2)[::-1]
labels = ['partition 1', 'partition 2']
for n, (x, ys) in enumerate(zip(xs, ys_list)):
    ax.bar(x + bar_width0, ys[0], bar_width1, color=colors[0], label=labels[0] if n == 0 else '_nolegend_')
    ax.bar(x + bar_width1, ys[1], bar_width1, color=colors[1], label=labels[1] if n == 0 else '_nolegend_')
plt.legend(frameon=False)
plt.tight_layout()
plt.show()
