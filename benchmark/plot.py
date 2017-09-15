# -*- coding: utf-8 -*-
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import pandas as pd
import seaborn as sns

sns.set()
sns.set_context("talk", font_scale=1.5)

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
tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]


ax = tmp1.plot(kind='line', y='time', x=x_axis, style='ro--', label='python', )
tmp2.plot(kind='line', y='time', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='time', x=x_axis, style='go--', label='qrllib fast', ax=ax)
ax.set_title('Key generation')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('keygen.png')

op = 'sign'
tmp1 = data[(data.source == 'old') & (data.operation==op)]
tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]

ax = tmp1.plot(kind='line', y='timems', x=x_axis, style='ro--', label='python', )
#tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='timems', x=x_axis, style='go--', label='qrllib fast', ax=ax)
ax.set_title('Sign [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (ms)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('sign.png')

op = 'verify'
tmp1 = data[(data.source == 'old') & (data.operation==op)]
tmp2 = data[(data.source == 'new') & (data.operation==op)]
tmp3 = data[(data.source == 'new2') & (data.operation==op)]

ax = tmp1.plot(kind='line', y='timems', x=x_axis, style='ro--', label='python', )
tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='qrllib', ax=ax)
tmp3.plot(kind='line', y='timems', x=x_axis, style='go--', label='qrllib fast', ax=ax)
ax.set_title('Verify [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (ms)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('verify.png')

############# SPEED UP #################

speed_up = data1.merge(data3, on=['operation', 'height'])
speed_up['ops_old'] = 1./speed_up['time_x']
speed_up['ops_new'] = 1./speed_up['time_y']
speed_up['speedup'] = speed_up['ops_new'] / speed_up['ops_old']
print(speed_up)

ax = speed_up[speed_up.operation=='create'].plot(kind='line', y='speedup', x=x_axis, style='bo--', label='qrllib')
ax.set_title('Key generation [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('speed up factor')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('speedup_create.png')

ax = speed_up[speed_up.operation=='sign'].plot(kind='line', y='speedup', x=x_axis, style='bo--', label='qrllib')
ax.set_title('Sign [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('speed up factor')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('speedup_sign.png')

ax = speed_up[speed_up.operation=='verify'].plot(kind='line', y='speedup', x=x_axis, style='bo--', label='qrllib')
ax.set_title('Verify [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('speed up factor')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
#ax.set_yscale('log')
ax.get_figure().savefig('speedup_verify.png')
