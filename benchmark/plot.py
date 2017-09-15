# -*- coding: utf-8 -*-
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="darkgrid")
flatui = ["#2c6fbb", "#fd3c06", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
sns.set_palette(sns.color_palette(flatui))

sns.set_context("talk", font_scale=1.4)

from matplotlib.ticker import MaxNLocator


data1 = pd.read_csv('data_old.csv')
data2 = pd.read_csv('data_new.csv')
data3 = pd.read_csv('data_new2.csv')
data = pd.concat([data1, data2, data3 ])


data['timems'] = data['time'] * 1000
data['leaves'] = 2**data['height']

x_axis = 'height'

#print(data)

op = 'create'
tmp1 = data[(data.source == 'old') & (data.operation==op)]
#tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]


fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=False, figsize=(16, 5))
#fig.suptitle("Performance comparison")
#fig.subplots_adjust(top=0.7)

ax1 = tmp1.plot(kind='line', y='time', x=x_axis, style='o:', label='python', ax=ax1)
#tmp2.plot(kind='line', y='time', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='time', x=x_axis, style='o:', label='qrllib', ax=ax1)
ax1.set_title('CreateKeys')
ax1.set_xlabel('Tree height')
ax1.set_ylabel('Time (s)')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
#ax1.get_figure().savefig('keygen.png')

op = 'sign'
tmp1 = data[(data.source == 'old') & (data.operation==op)]
#tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]

ax2 = tmp1.plot(kind='line', y='timems', x=x_axis, style='o:', label='python', ax=ax2)
#tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='timems', x=x_axis, style='o:', label='qrllib', ax=ax2)
ax2.set_title('Sign [256 bytes message]')
ax2.set_xlabel('Tree height')
ax2.set_ylabel('Time (ms)')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
#ax2.get_figure().savefig('sign.png')

op = 'verify'
tmp1 = data[(data.source == 'old') & (data.operation==op)]
#tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]

ax3 = tmp1.plot(kind='line', y='timems', x=x_axis, style='o:', label='python', ax=ax3 )
#tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='timems', x=x_axis, style='o:', label='qrllib', ax=ax3)
ax3.set_title('Verify [256 bytes message]')
ax3.set_xlabel('Tree height')
ax3.set_ylabel('Time (ms)')
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
#ax3.get_figure().savefig('verify.png')

plt.tight_layout()
fig.savefig('performance.png', dpi=300)
fig.show()

############# SPEED UP #################

speed_up = data1.merge(data3, on=['operation', 'height'])
speed_up['ops_old'] = 1./speed_up['time_x']
speed_up['ops_new'] = 1./speed_up['time_y']
speed_up['speedup'] = speed_up['ops_new'] / speed_up['ops_old']

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=False, figsize=(16, 5))
#fig.suptitle("Speed up")
#fig.subplots_adjust(top=0.85)

ax1 = speed_up[speed_up.operation=='create'].plot(kind='line', y='speedup', x=x_axis, style='o:', label='qrllib', ax=ax1)
ax1.set_title('CreateKeys')
ax1.set_xlabel('Tree height')
ax1.set_ylabel('speed up factor')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax1.set_yscale('log')

ax2 = speed_up[speed_up.operation=='sign'].plot(kind='line', y='speedup', x=x_axis, style='o:', label='qrllib', ax=ax2)
ax2.set_title('Sign [256 bytes message]')
ax2.set_xlabel('Tree height')
ax2.set_ylabel('speed up factor')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax2.set_yscale('log')

ax3 = speed_up[speed_up.operation=='verify'].plot(kind='line', y='speedup', x=x_axis, style='o:', label='qrllib', ax=ax3)
ax3.set_title('Verify [256 bytes message]')
ax3.set_xlabel('Tree height')
ax3.set_ylabel('speed up factor')
ax3.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax3.set_yscale('log')

plt.tight_layout()
fig.savefig('speedup.png', dpi=300)
fig.show()

############# SPEED UP #################

print(data3)

data3['ops'] = 1. / data3['time']

fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=False, figsize=(16, 5))
#fig.suptitle("Speed up")
#fig.subplots_adjust(top=0.85)

ax1 = data3[data3.operation=='sign'].plot(kind='line', y='ops', x=x_axis, style='o:', label='qrllib', ax=ax1)
ax1.set_title('Sign [256 bytes message]')
ax1.set_xlabel('Tree height')
ax1.set_ylabel('ops')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.set_ylim(50, 300)
#ax2.set_yscale('log')

ax2 = data3[data3.operation=='verify'].plot(kind='line', y='ops', x=x_axis, style='o:', label='qrllib', ax=ax2)
ax2.set_title('Verify [256 bytes message]')
ax2.set_xlabel('Tree height')
ax2.set_ylabel('ops')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.set_ylim(700, 1100)
#ax2.set_yscale('log')

plt.tight_layout()
fig.savefig('ops.png', dpi=300)
fig.show()
