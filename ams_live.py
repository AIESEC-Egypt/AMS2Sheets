from pypodio2 import api
import json
import gspread
from google.oauth2.service_account import Credentials


podio_client_id = ''
podio_client_secret = ''
podio_login_id = ''
podio_login_pw = ''
podio = api.OAuthClient(podio_client_id, podio_client_secret, podio_login_id, podio_login_pw)

# Assuming 25879453 is the app ID
app_id = 25879453

# Initialize pagination parameters
limit = 250  # Adjust the limit based on your needs
offset = 0
all_items = []

while offset < 250:
    filter_params = {'limit': limit, 'offset': offset}
    items = podio.Item.filter(app_id,  attributes=filter_params)

    if not items['items']:
        break  # No more items to retrieve

    all_items.extend(items['items'])
    print(f"Retrieved {len(items['items'])} items. Total items: {len(all_items)}")
    offset += limit


print(f"Total number of items: {len(all_items)}")

fields = ['Created By', 'Created On', 'Deal ID', 'Company reference', 'Local Committee', 'Shared Account with MC', 'Deal owner', 'Interested in:', 'Deal stage', 'Product', 'Sub-Product (IGT)', 'Sub-projects (iGV)', 'Stakeholder Type (iGV)', 'Stakeholders type (iGT)', 'Account Status by MCVP']
all_rows = []
for item in all_items:
    row = []
    for field in fields:
        flag = False
        if field == 'Created By':
            row.append(item['created_by']['name'])
            continue
        if field == 'Created On':
            row.append(item['created_on'])
            continue
        if field == 'Deal ID':
            row.append(item['app_item_id'])
            continue
        for j in range(0, len(item['fields'])):
            x = item['fields'][j]['label'] if item['fields'][j] else "-"
            if x == "-":
                continue
            if x == field:
                flag = 1
                if field == 'Company reference':
                    row.append(item['fields'][j]['values'][0]['value']['title'])
                elif field == 'Local Committee':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Shared Account with MC':
                    row.append(item['fields'][j]['values'][0]['value'])
                elif field == 'Deal owner':
                    row.append(item['fields'][j]['values'][0]['value']['name'])
                elif field == 'Interested in:':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Deal stage':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Product':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Sub-Product (IGT)':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Sub-projects (iGV)':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Stakeholder Type (iGV)':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
                elif field == 'Stakeholders type (iGT)':
                    row.append(item['fields'][j]['values'][0]['value'])
                elif field == 'Account Status by MCVP':
                    row.append(item['fields'][j]['values'][0]['value']['text'])
        if flag == 0:
                row.append("-")
    all_rows.append(row)    
            

print(all_rows)


# Load credentials from the JSON file you downloaded
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'client_secret_809161608184-4eg7pkc4k59v210neei2iqnb4d0hhsi6.apps.googleusercontent.com.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
# Open the Google Sheet using its title
spreadsheet = gc.open("AMS Live")

# Select a worksheet by title
worksheet = spreadsheet.AMS_LIVE
# Read data from the sheet
data = worksheet.get_all_records()
print("Data from the sheet:", data)

