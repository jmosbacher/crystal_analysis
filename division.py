#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:05:35 2017

@author: joe
"""

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import os
import matplotlib.pyplot as plt

gamma_file = '/home/joe/PycharmProjects/CrystalManager3.0/CalciumFluoride_BACK_IRR_CAF5_1_110816_VIS'
irr_file = '/home/joe/PycharmProjects/CrystalManager3.0/CalciumFluoride_IRR_CAF5_1_110816_VIS'
#dir_path = os.path.dirname(os.path.realpath(__file__))
#gamma_path = os.path.join(dir_path,gamma_file)

gamma_df = pd.read_csv(gamma_file)
irr_df = pd.read_csv(irr_file)
irr_df['em_wl'] = irr_df['em_wl'].apply(int)
gamma_df['em_wl'] = gamma_df['em_wl'].apply(int)

#g = gamma_df.sort_values('em_wl').reset_index()
#irr = irr_df.sort_values('em_wl').reset_index()
#merged = pd.merge_asof(g,irr,by='ex_wl', on='em_wl', suffixes=('g', 'irr'))
g_grouped = gamma_df.groupby(['ex_wl','em_wl'])
irr_grouped = irr_df.groupby(['ex_wl','em_wl'])
gmean = g_grouped.mean()
irrmean = irr_grouped.mean()
gmean['bg_corrected'] = gmean['signal']-gmean['bg']
irrmean['bg_corrected'] = irrmean['signal']-irrmean['bg']
merged = gmean.reset_index().merge(irrmean.reset_index(),on=['ex_wl','em_wl'],suffixes=['_G','_N+G'])
div = irrmean/gmean
div.reset_index(inplace=True)
merged['N+G/G'] = div['bg_corrected']
merged['N+G/G(BG)'] = div['bg']
fig = plt.figure()
grouped = merged.groupby('ex_wl')
#for ex_wl, df in grouped:
 #   df.plot(x='em_wl',y=['N+G/G','bg_corrected_N+G',
  #            'bg_corrected_G','bg_G','bg_N+G','N+G/G(BG)'],
   # title=str(ex_wl)+'nm',subplots=True,logy=True,)
    
grouped['N+G/G'].hist(bins=400,alpha=0.5)
plt.figure()    
merged['N+G/G'].hist(bins=400,alpha=0.5)    
plt.show()