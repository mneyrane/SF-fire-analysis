from pathlib import Path
import gzip
import pandas as pd

L_YEAR = 2020
U_YEAR = 2022
CHUNKSIZE = 2**16

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / 'Fire_Department_Calls_for_Service.csv.gz'
csv_out_path = data_dir / '01-fire_service_calls.csv.gz'

# columns to extract
target_columns = [
    'Call Number',
    'Incident Number',
    'Call Type',
    'Received DtTm',
    'Call Type Group',
    'Call Final Disposition',
    'case_location',
    'Unit Type',
    'Neighborhooods - Analysis Boundaries',
]

reader = pd.read_csv(
    csv_in_path, 
    usecols=target_columns, 
    chunksize=CHUNKSIZE, 
    low_memory=False)

header = True

with gzip.open(csv_out_path, mode='wt', newline='') as writer:
    for df in reader:
        df = df.rename({
            'Call Final Disposition' : 'Disposition',
            'case_location' : 'Location',
            'Neighborhooods - Analysis Boundaries' : 'Neighborhood',
        }, axis='columns')
        
        # convert call received column to datetime format
        df['Received DtTm'] = pd.to_datetime(
            df['Received DtTm'], 
            format='%m/%d/%Y %I:%M:%S %p')
        
        # extract calls between L_YEAR and U_YEAR
        call_year = df['Received DtTm'].dt.year
        df = df[(call_year <= U_YEAR) & (call_year >= L_YEAR)]
        
        # write chunk
        df.to_csv(writer, header=header, index=False)
        header = False # only write header for first chunk
