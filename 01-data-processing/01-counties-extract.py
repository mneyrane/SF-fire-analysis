from pathlib import Path
import pandas as pd
import shapely as shp

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / 'bayarea_county.csv.gz'
csv_out_path = data_dir / 'DP-SF_boundary.csv.gz'

df = pd.read_csv(csv_in_path)

res = df.loc[df['COUNTY'] == 'San Francisco', 'the_geom']

# extract relevant polygons for San Francisco county
bdry = shp.from_wkt(res.iat[0])
polys = list(bdry.geoms)
bdry_new = shp.geometry.MultiPolygon(polys[:2])

df_new = pd.DataFrame({'Geometry' : [bdry_new]})

df_new.to_csv(csv_out_path, index=False)
