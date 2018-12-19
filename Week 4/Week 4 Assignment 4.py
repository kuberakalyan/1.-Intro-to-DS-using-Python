# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 18:28:53 2017

@author: KUBERA KALYAN
"""
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import ttest_ind
# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
homes = (pd.read_csv('City_Zhvi_AllHomes.csv')
           .set_index('State'))
homes['State1'] = pd.Series(states)
homes = (homes.reset_index()
              .drop(['State'], axis = 1)
              .rename(columns = {'State1':'State'})
              .set_index(['State','RegionName']))
homes = homes[homes.columns[-200:]]
for col in range(0, 67):
    homes[str(2000+int(col/4)) + 'q' + str(1+col%4)] = (homes[homes.columns[3*col:3*(col+1)]]).mean(axis = 1)
homes = homes[homes.columns[-67:]]
file = open('university_towns.txt')
university = file.read().split('\n')
Data = pd.DataFrame(columns=['State', 'RegionName'])
i = 0
t = 0
while (t<len(university)):
    if(university[t].split('[edit]')[0] != university[t]):
        state = university[t].split('[')[0]
    else:
        region = university[t].split(' (')[0]
        Data.loc[i] = (state,region)
        i+=1
    t+=1
University = Data.drop(517)
University = University.set_index(['State','RegionName'])
uni_towns = pd.merge(University, homes, how='inner', left_index= True,right_index = True)
uni_towns = uni_towns[['2008q2','2009q2']]
uni_towns['Ratio'] = uni_towns['2008q2']/uni_towns['2009q2']
uni_towns = uni_towns.dropna()
non_uni_towns = homes[~homes.index.isin(uni_towns.index)]
non_uni_towns = non_uni_towns[['2008q2','2009q2']]
non_uni_towns['Ratio'] = non_uni_towns['2008q2']/non_uni_towns['2009q2']
non_uni_towns = non_uni_towns.dropna()
print(stats.ttest_ind(uni_towns['Ratio'], non_uni_towns['Ratio']))
print(np.mean(uni_towns['Ratio']))
print(np.mean(non_uni_towns['Ratio']))
