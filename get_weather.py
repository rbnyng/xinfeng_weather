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

def save_to_csv(data):
    # Define the CSV file name
    filename = "weather_data.csv"

    # Check if file exists
    file_exists = os.path.isfile(filename)

    # Writing to csv file
    with open(filename, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
        # Use DataFrame's to_csv method to handle the writing
        data.to_csv(csvfile, index=False, header=not file_exists)

def main():
    # Fetch data from the website
    data = fetch_data()

    # Save or append the data to a CSV file
    save_to_csv(data)

if __name__ == "__main__":
    main()
