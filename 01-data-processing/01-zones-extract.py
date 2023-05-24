from pathlib import Path
import pandas as pd

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / 'Zoning_Map_-_Zoning_Districts.csv.gz'
csv_out_path = data_dir / 'DP-zones.csv.gz'

# columns to extract
target_columns = [ 
    'gen', 
    'the_geom',
]

df = pd.read_csv(csv_in_path, usecols=target_columns, low_memory=False)

df = df.rename({
    'gen' : 'Zone Type',
    'the_geom' : 'Geometry'
    }, axis='columns')

# correct an entry typo
df.loc[df['Zone Type'] == 'Mixed', 'Zone Type'] = 'Mixed Use'

print(df['Zone Type'].value_counts())

df.to_csv(csv_out_path, index=False)
