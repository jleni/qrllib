# -*- coding: utf-8 -*-
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import pandas as pd
import seaborn as sns

sns.set()
sns.set_context("talk", font_scale=1.5)

from matplotlib.ticker import MaxNLocator


data = pd.read_csv('data.csv')
data['timems'] = data['time'] * 1000
data['leaves'] = 2**data['height']

x_axis = 'height'

print(data)

tmp1 = data[(data.source == 'qrllib') & (data.operation=='create')]
tmp2 = data[(data.source == 'legacy') & (data.operation=='create')]
ax1 = tmp1.plot(kind='line', y='time', x=x_axis, style='ro--', label='qrllib', )
ax = tmp2.plot(kind='line', y='time', x=x_axis, style='bo--', label='current code', ax=ax1)
ax.set_title('Key generation')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (s)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_yscale('log')
ax.get_figure().savefig('keygen.png')

tmp1 = data[(data.source == 'qrllib') & (data.operation=='sign')]
tmp2 = data[(data.source == 'legacy') & (data.operation=='sign')]
ax1 = tmp1.plot(kind='line', y='timems', x=x_axis, style='ro--', label='qrllib', )
ax = tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='current code', ax=ax1)
ax.set_title('Sign [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (ms)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_yscale('log')
ax.get_figure().savefig('sign.png')

tmp1 = data[(data.source == 'qrllib') & (data.operation=='verify')]
tmp2 = data[(data.source == 'legacy') & (data.operation=='verify')]
ax1 = tmp1.plot(kind='line', y='timems', x=x_axis, style='ro--', label='qrllib', )
ax = tmp2.plot(kind='line', y='timems', x=x_axis, style='bo--', label='current code', ax=ax1)
ax.set_title('Verify [256 bytes message]')
ax.set_xlabel('Tree height')
ax.set_ylabel('Time (ms)')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.set_yscale('log')
ax.get_figure().savefig('verify.png')
