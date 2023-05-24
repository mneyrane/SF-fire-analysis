import re
from pathlib import Path
import pandas as pd

data_dir = Path(__file__).parents[1] / 'data'

csv_in_path = data_dir / '01-nm_incidents.csv.gz'
csv_out_path = data_dir / '02-nm_incidents.csv.gz'

df = pd.read_csv(csv_in_path, low_memory=False)

# keep only the initial exposure (e.g. spreading fire) of each incident
df = df[df['Exposure Number'] == 0]
df = df.drop('Exposure Number', axis='columns')

print(f'Original data - number of rows: {len(df)}')

print('Columns with NaN values (will remove rows):\n', df.isna().any(axis='rows'), sep='')

# drop rows with missing values
df = df.dropna()

# create situation and response summary columns
code_regex = re.compile(r'\d')

def code_to_situation(code_str):
    # Convert incident codes (three-digit numbers) to their first-digit 
    # category, as specified by the National Fire Incident Reporting System.
    res = code_regex.match(code_str)
    assert(res is not None)
    digit = res.group(0)
    
    if digit == '1':
        return 'Fire'
    elif digit == '2':
        return 'Overpressure Rupture, Explosion, Overheat (No Fire)'
    elif digit == '3':
        return 'Rescue and Emergency Medical Service Incidents'
    elif digit == '4':
        return 'Hazardous Condition (No Fire)'
    elif digit == '5':
        return 'Service Call'
    elif digit == '6':
        return 'Good Intent Call'
    elif digit == '7':
        return 'False Alarm and False Call'
    elif digit == '8':
        return 'Severe Weather and Natural Disaster'
    elif digit == '9':
        return 'Special Incident Type'
    else:
        raise ValueError(f"Invalid digit: {digit}")
        
def code_to_response(code_str):
    # Convert response codes (two-digit numbers) to their first-digit
    # category as specified by the National Fire Incident Reporting System.
    res = code_regex.match(code_str)
    assert(res is not None)
    digit = res.group(0)
    
    if digit == '1':
        return 'Fire Control or Extinguishment'
    elif digit == '2':
        return 'Search and Rescue Activity'
    elif digit == '3':
        return 'Administer Emergency Medical Services'
    elif digit == '4':
        return 'Mitigate Hazardous Conditions'
    elif digit == '5':
        return 'Fire Control, Rescue, and Hazardous Condition Migitation Support'
    elif digit == '6':
        return 'Restore System or Provide Services'
    elif digit == '7':
        return 'Provide Assistance'
    elif digit == '8':
        return 'Provide Information, Investigate, or Enforce Codes or Regulations'
    elif digit == '9':
        return 'Fill In, Standby'
    elif digit == '0':
        return 'Other Actions Taken'
    else:
        raise ValueError(f"Invalid digit: {digit}")


df['Situation Summary'] = df['Situation'].apply(code_to_situation)
df['Response Summary'] = df['Response'].apply(code_to_response)

df = df.drop(['Situation', 'Response'], axis='columns')

# save the result
df.to_csv(csv_out_path, index=False)

print(f'Final data - number of rows: {len(df)}')
