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

nmi_path = data_dir / 'DP-nm_incidents.csv.gz'

# load fire incidents
df_nmi = pd.read_csv(
    nmi_path, 
    usecols=['Incident Date', 'Incident Number', 'Situation Summary'],
    parse_dates=['Incident Date'])

df_fire = df_nmi[df_nmi['Situation Summary'] == 'Fire']
df_fire = df_fire.drop('Situation Summary', axis='columns')
df_fire = df_fire.reset_index(drop=True)

SAMPLE_SIZE = 2000

df_fire_sample = df_fire.sample(n=SAMPLE_SIZE, axis='index')

week_groupby = df_fire_sample.groupby(pd.Grouper(key='Incident Date', freq='D'))
week_count = week_groupby.count()
week_count = week_count.reset_index()
week_count = week_count.rename({'Incident Number' : 'Incident Count'}, axis='columns')

def month_to_season(x):
    if x.month in (12,1,2):
        return 'winter'
    elif x.month in (3,4,5):
        return 'spring'
    elif x.month in (6,7,8):
        return 'summer'
    else:
        return 'autumn'
    
week_count['Season'] = week_count['Incident Date'].apply(month_to_season)

sns.histplot(week_count, x='Incident Count', hue='Season', multiple='dodge', binwidth=1, shrink=.9)
plt.savefig('test.png')

season_counts = [
    week_count.loc[week_count['Season'] == 'winter', 'Incident Count'],
    week_count.loc[week_count['Season'] == 'spring', 'Incident Count'],
    week_count.loc[week_count['Season'] == 'summer', 'Incident Count'],
    week_count.loc[week_count['Season'] == 'autumn', 'Incident Count'],
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

print(posthoc)
