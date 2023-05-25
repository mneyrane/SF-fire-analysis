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
zone_path = data_dir / 'DP-zones.csv.gz'

# load fire incidents
df_nmi = pd.read_csv(
    nmi_path, 
    usecols=['Incident Date', 'Location', 'Situation Summary'],
    parse_dates=['Incident Date'])

# these are the top 4 situation summaries in count
situations = [
    'False Alarm and False Call', 
    'Service Call', 
    'Fire', 
    'Rescue and Emergency Medical Service Incidents',
]

df_nmi.loc[~df_nmi['Situation Summary'].isin(situations), 'Situation Summary'] = 'Other'

SAMPLE_SIZE = 10000

df_sample = df_nmi.sample(n=SAMPLE_SIZE, axis='index')
df_sample = df_sample.reset_index(drop=True)
df_sample['Location'] = df_sample['Location'].apply(from_wkt)
gdf_sample = gpd.GeoDataFrame(df_sample, geometry='Location', crs='EPSG:2227')

# load zones
df_zones = pd.read_csv(zone_path)
df_zones['Geometry'] = df_zones['Geometry'].apply(from_wkt)
gdf_zones = gpd.GeoDataFrame(df_zones, geometry='Geometry', crs='EPSG:4326')
gdf_zones = gdf_zones.to_crs('EPSG:2227')

# quickly save zone plot
gdf_zones.plot(column='Zone Type', categorical=True, linewidth=.25, edgecolor='black', legend=True, legend_kwds={'loc' : 'upper left'}, cmap='Paired')
plt.savefig(fig_dir / 'zones.png', dpi=300, bbox_inches='tight')

# perform join and run chi-squared independence test

join = gdf_sample.sjoin_nearest(gdf_zones, how='inner')
join = join.drop('index_right', axis='columns')

zone_count = join[['Zone Type', 'Situation Summary']].value_counts()
zone_count = zone_count.unstack()
zone_count = zone_count.rename({
    'False Alarm and False Call' : 'False Alarm',
    'Service Call' : 'Service Call',
    'Fire' : 'Fire',
    'Rescue and Emergency Medical Service Incidents' : 'Rescue/EMS',
    }, axis='columns')

print(zone_count)

chi = stats.chi2_contingency(zone_count)

print('Chi-square (independence) test statistic:', chi.statistic)
print('Chi-square (independence) p-value:', chi.pvalue)
print('Chi-square (independence) degrees of freedom:', chi.dof)
print('Chi-square (independence) expected frequencies:\n', chi.expected_freq)
