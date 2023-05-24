from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely import from_wkt

data_dir = Path(__file__).parents[1] / 'data'

csv_nmi_inpath = data_dir / '02-nm_incidents.csv.gz'
csv_fsc_inpath = data_dir / '02-fire_service_calls.csv.gz'
csv_com_inpath = data_dir / '01-fire_safety_complaints.csv.gz'

csv_nmi_outpath = data_dir / 'DP-nm_incidents.csv.gz'
csv_fsc_outpath = data_dir / 'DP-fire_service_calls.csv.gz'
csv_com_outpath = data_dir / 'DP-fire_safety_complaints.csv.gz'

sf_bdry_path = data_dir / 'DP-SF_boundary.csv.gz'

df_bdry = pd.read_csv(sf_bdry_path)
df_bdry['Geometry'] = df_bdry['Geometry'].apply(from_wkt)

gdf_bdry = gpd.GeoDataFrame(geometry=df_bdry['Geometry'], crs='EPSG:4326')
gdf_bdry = gdf_bdry.to_crs('EPSG:2227')

# spatial join with non-medical incident data
df_nmi = pd.read_csv(csv_nmi_inpath)
df_nmi['Location'] = df_nmi['Location'].apply(from_wkt)
gdf_nmi = gpd.GeoDataFrame(df_nmi, geometry='Location', crs='EPSG:4326')
gdf_nmi = gdf_nmi.to_crs('EPSG:2227')

nmi_join = gdf_nmi.sjoin(gdf_bdry, how='inner', predicate='intersects')
nmi_join = nmi_join.drop('index_right', axis='columns')

print('Non-medical incidents BEFORE spatial join:', len(df_nmi))
print('Non-medical incidents AFTER spatial join:', len(nmi_join))

df_nmi_new = pd.DataFrame(nmi_join)
df_nmi_new.to_csv(csv_nmi_outpath, index=False)

# spatial join with fire service call data
df_fsc = pd.read_csv(csv_fsc_inpath)
df_fsc['Location'] = df_fsc['Location'].apply(from_wkt)
gdf_fsc = gpd.GeoDataFrame(df_fsc, geometry='Location', crs='EPSG:4326')
gdf_fsc = gdf_fsc.to_crs('EPSG:2227')

fsc_join = gdf_fsc.sjoin(gdf_bdry, how='inner', predicate='intersects')
fsc_join = fsc_join.drop('index_right', axis='columns')

print('Fire service calls BEFORE spatial join:', len(df_fsc))
print('Fire service calls AFTER spatial join:', len(fsc_join))

df_fsc_new = pd.DataFrame(fsc_join)
df_fsc_new.to_csv(csv_fsc_outpath, index=False)

# spatial join with fire safety complaint data
df_com = pd.read_csv(csv_com_inpath)
df_com['Location'] = df_com['Location'].apply(from_wkt)
gdf_com = gpd.GeoDataFrame(df_com, geometry='Location', crs='EPSG:4326')
gdf_com = gdf_com.to_crs('EPSG:2227')

com_join = gdf_com.sjoin(gdf_bdry, how='inner', predicate='intersects')
com_join = com_join.drop('index_right', axis='columns')

print('Fire safety complaints BEFORE spatial join:', len(df_com))
print('Fire safety complaints AFTER spatial join:', len(com_join))

df_com_new = pd.DataFrame(com_join)
df_com_new.to_csv(csv_com_outpath, index=False)
