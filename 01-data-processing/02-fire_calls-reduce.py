from pathlib import Path
import pandas as pd

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / '01-fire_service_calls.csv.gz'
csv_out_path = data_dir / '02-fire_service_calls.csv.gz'

df = pd.read_csv(csv_in_path, low_memory=False)

print(f'Original data - number of rows: {len(df)}')

print('Columns with NaN values (will remove rows):\n', df.isna().any(axis='rows'), sep='')

# drop rows with missing values
df = df.dropna()

print(f'NaN dropped data - number of rows: {len(df)}')

# We discard the 'Unit Type' column since rows are duplicated by each unit
# that arrived at the incident. After that, we drop the duplicates.
df = df.drop('Unit Type', axis='columns')
df = df.drop_duplicates()

# save the result
df.to_csv(csv_out_path, index=False)

print(f'Final data - number of rows: {len(df)}')
