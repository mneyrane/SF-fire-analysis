from pathlib import Path
import pandas as pd

L_YEAR = 2020
U_YEAR = 2022

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / 'Fire_Safety_Complaints.csv.gz'
csv_out_path = data_dir / '01-fire_safety_complaints.csv.gz'

# columns to extract
complaints_columns = [
    'Received Date',
    'Location',
    'Neighborhood  District',
    'Disposition',
    'Disposition Date',
    'Complaint Item Type Description',
]

df = pd.read_csv(csv_in_path, usecols=complaints_columns, low_memory=False)

df = df.rename({
        'Neighborhood  District' : 'Neighborhood',
        'Complaint Item Type Description' : 'Complaint Type',
    }, axis='columns')

print(f'Original data - number of rows: {len(df)}')

# convert date columns to datetime
df['Received Date'] = pd.to_datetime(
    df['Received Date'], errors='coerce', format='%m/%d/%Y')

df['Disposition Date'] = pd.to_datetime(
    df['Disposition Date'], errors='coerce', format='%m/%d/%Y')

# extract complaints between L_YEAR AND U_YEAR
received_year = df['Received Date'].dt.year
disposition_year = df['Disposition Date'].dt.year

datecmp = lambda x : (x >= L_YEAR) & (x <= U_YEAR)

df = df[datecmp(received_year) & (datecmp(disposition_year) | disposition_year.isna())]

print(f'Data in {L_YEAR}-{U_YEAR} (or NaT) - number of rows: {len(df)}')

# drop rows with empty values
df = df.dropna()

print(f'Data in {L_YEAR}-{U_YEAR} (NaT dropped) - number of rows: {len(df)}')

# select only fire-related complaints
fire_related_complaints = [
    'alarm systems',
    'multiple fire code violations',
    'blocked exits',
    'extinguishers',
    'sprinkler/standpipe systems',
    'combustible materials',
    'exit maintenance',
]

df = df[df['Complaint Type'].isin(fire_related_complaints)]

print(f'Fire-related data in {L_YEAR}-{U_YEAR} - number of rows: {len(df)}')

# save extracted data
df.to_csv(csv_out_path, index=False)

print(f'Final extracted data - number of rows: {len(df)}')
