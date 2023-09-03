import os
import sys

# add the parent directory of the flask_app module to the search path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import gspread
from google.oauth2.service_account import Credentials
from flask_app.models.flavor import Flavor

# Define the scope and credentials to use for authentication
scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds = Credentials.from_service_account_file('C:/Users/Francisco/Desktop/NOVEL/novel-379206-032ae9c2200b.json', scopes=scope)

# Authenticate with the Google Sheets API
client = gspread.authorize(creds)

# Open the Google Sheet by URL or name
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1-M6bG--3XKM9k3Q9XX3hSrBT2adEP3FbJ0m9ESb-39I/edit#gid=1710817940')
# or
# sheet = client.open('Your Sheet Name')

# Get the first worksheet in the sheet
worksheet = sheet.get_worksheet(0)

# Get the values in columns A, B, and C
values = worksheet.get('A:C')

# Loop through the rows and create Flavor objects
for row in values[1:]:
    if row and row[0]:
        name = row[0]
        description = row[2] if len(row) > 2 else ''
        flavor_type = row[0].lower() if 'sorbet' in row[0].lower() else 'ice cream'
        is_ice_cream = (flavor_type == 'ice cream')

        data = {
            'name': name,
            'description': description,
            'is_ice_cream': is_ice_cream
        }

        flavor = Flavor(data)
        flavor.save(data)

    else:
        print('Empty row or missing name:', row)