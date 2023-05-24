from pathlib import Path
import gzip
import pandas as pd

L_YEAR = 2020
U_YEAR = 2022
CHUNKSIZE = 2**16

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / 'Fire_Incidents.csv.gz'
csv_out_path = data_dir / '01-nm_incidents.csv.gz'

target_columns = [
    'Incident Number',
    'Exposure Number',
    'Incident Date',
    'Call Number',
    #'Suppression Units',
    #'Suppression Personnel',
    #'EMS Units',
    #'EMS Personnel',
    #'Other Units',
    #'Other Personnel',
    #'Fire Fatalities',
    #'Fire Injuries',
    #'Civilian Fatalities',
    #'Civilian Injuries',
    #'Estimated Property Loss',
    #'Estimated Contents Loss',
    'Primary Situation',
    'Action Taken Primary',
    #'Property Use',
    'neighborhood_district',
    'point',
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
            'neighborhood_district' : 'Neighborhood',
            'point' : 'Location',
            'Primary Situation' : 'Situation',
            'Action Taken Primary' : 'Response',
        }, axis='columns')
        
        # convert incident date to datetime format
        df['Incident Date'] = pd.to_datetime(
            df['Incident Date'],
            format='%Y-%m-%dT%H:%M:%S')
        
        # keep incidents between L_YEAR and U_YEAR
        incident_year = df['Incident Date'].dt.year
        df = df[(incident_year <= U_YEAR) & (incident_year >= L_YEAR)]
        
        # write chunk
        df.to_csv(writer, header=header, index=False)
        header = False # only write header from first chunk
