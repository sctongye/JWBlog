import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from datetime import datetime
from django.conf import settings


def update_ref_info():
    try:
        # Define paths
        static_dir = os.path.join(
            settings.BASE_DIR, 'static', 'referee_records')
        output_file_path = os.path.join(static_dir, 'refinfo.js')
        backups_dir = os.path.join(static_dir, 'backups')

        # Ensure backup directory exists
        os.makedirs(backups_dir, exist_ok=True)

        # Create backup of current file with error handling
        if os.path.exists(output_file_path):
            try:
                backup_filename = f'refinfo_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.js'
                backup_path = os.path.join(backups_dir, backup_filename)
                with open(output_file_path, 'r', encoding='utf-8') as src, \
                        open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            except PermissionError as e:
                print(f"Warning: Could not create backup file: {str(e)}")

        # Set up Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds",
                 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]

        credentials_path = os.path.join(settings.BASE_DIR, 'static', 'referee_records',
                                        'api-project-814768689976-28b4d8043bd4.json')

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, scope)
        client = gspread.authorize(creds)

        # Open the spreadsheet
        sheet = client.open_by_url(
            "https://docs.google.com/spreadsheets/d/1fsq-WJBGfIBjla8U0E5y5cjNocH9M-0Ts5ujXYIgw5E/edit?gid=0#gid=0").sheet1

        # Get and process data
        data = sheet.get_all_values()
        column_names = data[0]
        data = data[1:]
        df = pd.DataFrame(data, columns=column_names)

        # Process data
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%I:%M %p')
        df = df.fillna('')
        df['id'] = df['id'].astype(int)
        df_sorted = df.sort_values(by='id', ascending=False)

        # Create features
        features = []
        for _, row in df_sorted.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['Long'], row['Lat']]
                },
                "properties": {
                    "Date": row['Date'],
                    "Time": row['Time'],
                    "Year": row['Year'],
                    "Season": row['Season'],
                    "League": row['League'],
                    "Level": row['Level'],
                    "Type": row['Type'],
                    "Half_Length": row['Half_Length'],
                    "Home": row['Home'],
                    "Away": row['Away'],
                    "Location": row['Location'],
                    "City": row['City'],
                    "Assignor": row['Assignor'],
                    "Role": row['Role'],
                    "Coworker1": row['Coworker1'],
                    "Coworker2": row['Coworker2'],
                    "Score": row['Score'],
                    "Yellow": row['Yellow'],
                    "Penalty": row['Penalty'],
                    "Note": row['Note'],
                    "Fee": row['Fee'],
                    "Long": row['Long'],
                    "Lat": row['Lat'],
                    "Pay4WebDisplay": row['Pay4WebDisplay']
                }
            }
            features.append(feature)

        # Save to file
        output_content = "const refInfo = " + \
            json.dumps(features, indent=2, ensure_ascii=False)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

        return True

    except Exception as e:
        print(f"Error in update_ref_info: {str(e)}")
        raise
