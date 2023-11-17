import requests
from requests_html import HTMLSession
import pandas as pd
import csv
import os
from datetime import datetime
from pathlib import Path

notebookpath = Path.cwd()
folderpath = notebookpath.parent
os.chdir(folderpath)

def fetch_data():
    # URL of the website containing weather data
    url = 'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=C0D59'

    # Start an HTML Session
    session = HTMLSession()

    # Fetch the webpage
    r = session.get(url)

    # Render the JavaScript with an appropriate sleep time
    r.html.render(sleep=5)

    # Extract tables into a list of DataFrames
    tables = pd.read_html(r.html.html)

    # Assuming the first table is the required one
    return tables[0]

def append_to_csv(new_data, filename):
    if os.path.isfile(filename):
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(filename, index=False)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_filename = os.path.join(script_dir, 'weather_data.csv')

    new_data = fetch_data()
    append_to_csv(new_data, csv_filename)
    
if __name__ == "__main__":
    main()
