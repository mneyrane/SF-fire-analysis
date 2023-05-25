from pathlib import Path
import numpy as np
import pandas as pd
#import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
#from shapely import from_wkt
from scipy import stats


sns.set_theme(context='paper', style='darkgrid', font='Arimo')


data_dir = Path(__file__).parents[1] / 'data'
fig_dir = Path(__file__).parents[1] / 'figures'

fig_dir.mkdir(exist_ok=True)

nmi_path = data_dir / 'DP-nm_incidents.csv.gz'

# load fire incidents
df_nmi = pd.read_csv(
    nmi_path,
    usecols=['Incident Date', 'Incident Number', 'Situation Summary'],
    parse_dates=['Incident Date'])

df_fire = df_nmi[df_nmi['Situation Summary'] == 'Fire']
df_fire = df_fire.drop('Situation Summary', axis='columns')
df_fire = df_fire.reset_index(drop=True)

SAMPLE_SIZE = 2500

df_fire_sample = df_fire.sample(n=SAMPLE_SIZE, axis='index')

period_groupby = df_fire_sample.groupby(pd.Grouper(key='Incident Date', freq='3D'))
period_count = period_groupby.count()
period_count = period_count.reset_index()
period_count = period_count.rename({'Incident Number' : 'Incident Count'}, axis='columns')

def month_to_season(x):
    if x.month in (12,1,2):
        return 'winter'
    elif x.month in (3,4,5):
        return 'spring'
    elif x.month in (6,7,8):
        return 'summer'
    else:
        return 'autumn'
    
period_count['Season'] = period_count['Incident Date'].apply(month_to_season)

fig, axs = plt.subplots(1, 2, figsize=(9,3))

sns.histplot(period_count, x='Incident Count', hue='Season', multiple='dodge', binwidth=2, shrink=.9, ax=axs[0])
sns.boxplot(period_count, x='Incident Count', y='Season', ax=axs[1])

axs[0].set_xlabel('Fire-related incidents (3 day interval)')
axs[1].set_xlabel('Fire-related incidents (3 day interval)')

fig.tight_layout()
fig.savefig(fig_dir / 'fire_incidents_vs_seasons_analysis.svg', bbox_inches='tight')

season_counts = [
    period_count.loc[period_count['Season'] == 'winter', 'Incident Count'],
    period_count.loc[period_count['Season'] == 'spring', 'Incident Count'],
    period_count.loc[period_count['Season'] == 'summer', 'Incident Count'],
    period_count.loc[period_count['Season'] == 'autumn', 'Incident Count'],
]

var_res = stats.levene(*season_counts)
print('Levene test (median) statistic:', var_res.statistic)
print('Levene test (median) p-value:', var_res.pvalue)

for i, sc in enumerate(season_counts):
    norm_res = stats.normaltest(sc)
    print(f'Normality test ({i}) statistic:', norm_res.statistic)
    print(f'Normality test ({i}) p-value:', norm_res.pvalue)

anova = stats.f_oneway(*season_counts)
print('ANOVA statistic:', anova.statistic)
print('ANOVA p-value:', anova.pvalue)

posthoc = stats.tukey_hsd(*season_counts)
posthoc.confidence_interval(0.99)

print(posthoc)
