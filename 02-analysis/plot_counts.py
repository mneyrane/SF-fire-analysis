import re
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme(context='paper', style='darkgrid', font='Arimo')


data_dir = Path(__file__).parents[1] / 'data'
fig_dir = Path(__file__).parents[1] / 'figures'

calls_path = data_dir / 'DP-fire_service_calls.csv.gz'
incs_path = data_dir / 'DP-nm_incidents.csv.gz'

df_calls = pd.read_csv(calls_path)
df_incs = pd.read_csv(incs_path)

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

plt.figure()
sns.barplot(x=ct_count_top10.values, y=ct_count_top10.index, palette='flare')
plt.savefig(fig_dir / 'call_type_counts.svg', bbox_inches='tight', pad_inches=.25)

#
# Create and save Situation count as given by the dataset of "Fire Incidents".
#
# "Fire Incidents" are defined by non-medical incidents, as reported in the
# open data portal. The incident numbers in this dataset occur in the Fire
# Service Calls dataset, and is effectively a subset.
print(f"Total number of (non-medical) incidents: {len(df_incs)}")

s_count = df_incs['Situation Summary'].value_counts()
r_count = df_incs['Response Summary'].value_counts()

plt.figure()
sns.barplot(x=s_count.values, y=s_count.index, palette='flare')
plt.savefig(fig_dir / 'nm_situation_counts.svg', bbox_inches='tight', pad_inches=.25)

plt.figure()
sns.barplot(x=r_count.values, y=r_count.index, palette='flare')
plt.savefig(fig_dir / 'nm_response_counts.svg', bbox_inches='tight', pad_inches=.25)
