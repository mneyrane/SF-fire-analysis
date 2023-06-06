import re
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme(context='paper', style='whitegrid', font='Arimo')
facecolor = '#f8f5f0'

data_dir = Path(__file__).parents[1] / 'data'
fig_dir = Path(__file__).parents[1] / 'figures'

fig_dir.mkdir(exist_ok=True)

calls_path = data_dir / 'DP-fire_service_calls.csv.gz'
inc_path = data_dir / 'DP-nm_incidents.csv.gz'
com_path = data_dir / 'DP-fire_safety_complaints.csv.gz'

df_calls = pd.read_csv(calls_path)
df_inc = pd.read_csv(inc_path)
df_com = pd.read_csv(com_path)

#
# create and save Call Type Count figure
ct_count = df_calls['Call Type'].value_counts()

ct_count_nm = ct_count.drop('Medical Incident')
other_count = ct_count_nm.tail(-10).sum()
ct_count_top10 = ct_count_nm.head(10)
ct_count_top10.at['Other'] = ct_count_top10.at['Other'] + other_count
ct_count_top10 = ct_count_top10.sort_values(ascending=False)

print(f"Total number of calls: {ct_count.sum()}")
print(f"Number of medical incidents: {ct_count['Medical Incident']}")
print(f"Number of top 10 call types (no medical incidents): {ct_count_top10.sum()}")

#print(ct_count_top10)

plt.figure(facecolor=facecolor)
sns.barplot(x=ct_count_top10.values, y=ct_count_top10.index, palette='flare')
plt.savefig(fig_dir / 'call_type_counts.svg', bbox_inches='tight')

#
# Create and save Situation and Response count as given by the dataset of 
# "Fire Incidents".
#
# "Fire Incidents" are defined by non-medical incidents (but still includes
# emergency incidents), as reported in the open data portal. The incident 
# numbers in this dataset occur in the Fire Service Calls dataset, and is 
# effectively a subset.
print(f"Total number of (non-medical) incidents: {len(df_inc)}")

s_count = df_inc['Situation Summary'].value_counts()
r_count = df_inc['Response Summary'].value_counts()

#print(s_count)
#print(r_count)

plt.figure(facecolor=facecolor)
sns.barplot(x=s_count.values, y=s_count.index, palette='flare')
plt.savefig(fig_dir / 'nm_situation_counts.svg', bbox_inches='tight')

plt.figure(facecolor=facecolor)
sns.barplot(x=r_count.values, y=r_count.index, palette='flare')
plt.savefig(fig_dir / 'nm_response_counts.svg', bbox_inches='tight')

#
# create and save Complaint Type Count figure
print(f"Total number of fire safety complaints: {len(df_com)}")

c_count = df_com['Complaint Type'].value_counts()

#print(c_count)

plt.figure(facecolor=facecolor)
ax = sns.barplot(x=c_count.values, y=c_count.index, palette='flare')
plt.savefig(fig_dir / 'complaint_type_counts.svg', bbox_inches='tight')
