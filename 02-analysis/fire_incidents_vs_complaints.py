from pathlib import Path
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from shapely import from_wkt
from scipy import stats

sns.set_theme(context='paper', style='darkgrid', font='Arimo')


data_dir = Path(__file__).parents[1] / 'data'
fig_dir = Path(__file__).parents[1] / 'figures'

fig_dir.mkdir(exist_ok=True)

nmi_path = data_dir / 'DP-nm_incidents.csv.gz'
com_path = data_dir / 'DP-fire_safety_complaints.csv.gz'

# load fire incidents
df_nmi = pd.read_csv(
    nmi_path, 
    usecols=['Incident Date', 'Location', 'Situation Summary'],
    parse_dates=['Incident Date'])

df_nmi_fire = df_nmi[df_nmi['Situation Summary'] == 'Fire']
df_nmi_fire = df_nmi_fire.drop('Situation Summary', axis='columns')
df_nmi_fire['Location'] = df_nmi_fire['Location'].apply(from_wkt)
df_nmi_fire = df_nmi_fire.reset_index(drop=True)
gdf_nmi_fire = gpd.GeoDataFrame(df_nmi_fire, geometry='Location', crs='EPSG:2227')

# load complaints
df_com = pd.read_csv(
    com_path, 
    usecols=['Received Date', 'Location'],
    parse_dates=['Received Date'])
    
df_com['Location'] = df_com['Location'].apply(from_wkt)
gdf_com = gpd.GeoDataFrame(df_com, geometry='Location', crs='EPSG:2227')

# compute BEFORE and AFTER data points for complaints

FT_TO_KM = 3.048e-4
RADIUS_KM = 0.5
SAMPLE_SIZE = 2000

t_offset = pd.Timedelta('30 days')
t_start = pd.Timestamp('2020-01-01') + t_offset
t_end = pd.Timestamp('2022-12-31') - t_offset

date_mask = (gdf_com['Received Date'] >= t_start) & (gdf_com['Received Date'] <= t_end)
gdf_com_sample = gdf_com[date_mask]
gdf_com_sample = gdf_com_sample.sample(n=SAMPLE_SIZE, axis='index')

def f(x, gdf):
    date = x['Received Date']
    date_start = date - t_offset
    date_end = date + t_offset
    
    before_mask = (gdf['Incident Date'] >= date_start) & (gdf['Incident Date'] <= date)
    after_mask = (gdf['Incident Date'] >= date) & (gdf['Incident Date'] <= date_end)
    
    gdf_before = gdf[before_mask].copy()
    gdf_after = gdf[after_mask].copy()
    
    dist_before = FT_TO_KM * gdf_before.distance(x['Location'])
    dist_after = FT_TO_KM * gdf_after.distance(x['Location'])
    
    count_before = (dist_before <= RADIUS_KM).sum()
    count_after = (dist_after <= RADIUS_KM).sum()
    
    return {'before' : count_before, 'after' : count_after}
    
    

counts = gdf_com_sample.apply(
    f, 
    axis='columns', 
    result_type='expand', 
    args=(gdf_nmi_fire,))


ax = sns.histplot(data=counts, multiple='dodge', binwidth=3, shrink=.9)
ax.set_xlabel('Fire-related incidents near complaint (30 days, 500 m)')
plt.savefig(fig_dir / 'fire_incidents_vs_complaints_analysis.svg', bbox_inches='tight')

# run Mann-Whitney U-test on BEFORE and AFTER complaint counts
res = stats.mannwhitneyu(x=counts['before'], y=counts['after'])
print('Mann-Whitney U-test statistic:', res.statistic)
print('Mann-Whitney U-test p-value:', res.pvalue)
