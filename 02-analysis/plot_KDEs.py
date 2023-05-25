from pathlib import Path
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from shapely import from_wkt

sns.set_theme(context='paper', style='darkgrid', font='Arimo')


data_dir = Path(__file__).parents[1] / 'data'
fig_dir = Path(__file__).parents[1] / 'figures'

fig_dir.mkdir(exist_ok=True)

nmi_path = data_dir / 'DP-nm_incidents.csv.gz'
com_path = data_dir / 'DP-fire_safety_complaints.csv.gz'
bdry_path = data_dir / 'DP-SF_boundary.csv.gz'

# load San Francisco boundary
df_bdry = pd.read_csv(bdry_path)
s_bdry = df_bdry['Geometry'].apply(from_wkt)
gs_bdry = gpd.GeoSeries(s_bdry, crs='EPSG:4326')
gs_bdry = gs_bdry.to_crs('EPSG:2227')

# load fire incidents
df_nmi = pd.read_csv(nmi_path)
s_nmi_fire = df_nmi.loc[df_nmi['Situation Summary'] == 'Fire', 'Location']
s_nmi_fire = s_nmi_fire.apply(from_wkt)
s_nmi_fire = s_nmi_fire.reset_index(drop=True)

gs_nmi_fire = gpd.GeoSeries(s_nmi_fire, crs='EPSG:2227')

# load complaints
df_com = pd.read_csv(com_path)
s_com = df_com['Location']
s_com = s_com.apply(from_wkt)

gs_com = gpd.GeoSeries(s_com, crs='EPSG:2227')

# generate KDE plots
fig, axs = plt.subplots(1, 2)

gs_bdry.boundary.plot(edgecolor='black', linewidth=.5, ax=axs[0])
xlim, ylim = axs[0].get_xlim(), axs[0].get_ylim()
sns.kdeplot(x=gs_nmi_fire.x, y=gs_nmi_fire.y, color='red', fill=True, ax=axs[0])
axs[0].set_xlim(*xlim)
axs[0].set_ylim(*ylim)
axs[0].set_title('Fire-related incidents')

gs_bdry.boundary.plot(edgecolor='black', linewidth=.5, ax=axs[1])
xlim, ylim = axs[1].get_xlim(), axs[1].get_ylim()
sns.kdeplot(x=gs_com.x, y=gs_com.y, color='blue', fill=True, ax=axs[1])
axs[1].set_xlim(*xlim)
axs[1].set_ylim(*ylim)
axs[1].set_title('Fire safety complaints')

fig.savefig(fig_dir / 'fire_inc_and_complaints_KDE.svg', bbox_inches='tight')
