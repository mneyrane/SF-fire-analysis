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

nmi_path = data_dir / 'DP-nm_incidents.csv.gz'
zone_path = data_dir / 'DP-zones.csv.gz'

# load fire incidents
df_nmi = pd.read_csv(
    nmi_path, 
    usecols=['Incident Date', 'Location', 'Situation Summary'],
    parse_dates=['Incident Date'])

situations = ['False Alarm and False Call', 'Service Call', 'Fire']

df_nmi_fire = df_nmi[df_nmi['Situation Summary'].isin(situations)]
df_nmi_fire = df_nmi_fire.copy()
#df_nmi_fire = df_nmi_fire.drop('Situation Summary', axis='columns')
df_nmi_fire['Location'] = df_nmi_fire['Location'].apply(from_wkt)
df_nmi_fire = df_nmi_fire.reset_index(drop=True)
gdf_nmi_fire = gpd.GeoDataFrame(df_nmi_fire, geometry='Location', crs='EPSG:2227')

SAMPLE_SIZE = 5000

gdf_sample = gdf_nmi_fire.sample(n=SAMPLE_SIZE, axis='index')

# load zones
df_zones = pd.read_csv(zone_path)
df_zones['Geometry'] = df_zones['Geometry'].apply(from_wkt)
gdf_zones = gpd.GeoDataFrame(df_zones, geometry='Geometry', crs='EPSG:4326')
gdf_zones = gdf_zones.to_crs('EPSG:2227')

join = gdf_sample.sjoin_nearest(gdf_zones, how='inner')
join = join.drop('index_right', axis='columns')

gdf_zones['Area'] = gdf_zones.area

FT_TO_KM = 3.048e-4

groupby = gdf_zones[['Area', 'Zone Type']].groupby('Zone Type')
total_area_km = (FT_TO_KM)**2 * groupby.sum()
total_area_km = total_area_km['Area']

zone_count = join[['Zone Type', 'Situation Summary']].value_counts()

zone_count = zone_count.unstack()

zone_count_weighted = zone_count / total_area_km

print(zone_count)
print(zone_count_weighted)
#chi = stats.chisquare(zone_count)

#print('Chi-square (frequency) test statistic:', chi.statistic)
#print('Chi-square (frequency) p-value:', chi.pvalue)

