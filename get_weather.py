import requests
from requests_html import HTMLSession
import pandas as pd
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo
from io import StringIO
import re

def fetch_data(url):
    session = HTMLSession()
    r = session.get(url)
    
    # Render the JavaScript with an appropriate sleep time
    r.html.render(sleep=5)
    
    # Extract tables into a list of DataFrames
    tables = pd.read_html(StringIO(r.html.html))
    data = tables[0]
    
    # Process the weather column since it's images and we want text
    weather_cells = r.html.find('td[headers="weather"] img') 
    
    # Extract 'alt' text (captions) from images
    weather_captions = [cell.attrs.get('alt', '') for cell in weather_cells]
    data.iloc[:, 2] = data.iloc[:, 2].astype(str)

    # Replace the weather column in the DataFrame
    if len(weather_captions) == len(data):
        data.iloc[:, 2] = weather_captions
    
    # Extract the station name
    station_name_element = r.html.find('li#BarStationName', first=True)
    station_name = station_name_element.text if station_name_element else "Unknown_Station"
    
    return data, station_name

def append_to_csv(new_data, filename):
    # Get the current year
    current_time_gmt8 = datetime.now(ZoneInfo('Asia/Taipei'))
    
    # Format the time column in new_data to include the current year
    new_data['觀測時間'] = new_data['觀測時間'].apply(lambda x: f"{current_time_gmt8.year}/{x}")
    new_data['觀測時間'] = pd.to_datetime(new_data['觀測時間'], format='%Y/%m/%d %H:%M')

    if os.path.isfile(filename):
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([new_data, existing_data], ignore_index=True)
        updated_data = updated_data.astype({'觀測時間': 'str'})
        updated_data = updated_data.drop_duplicates()
    else:
        updated_data = new_data

    updated_data.to_csv(filename, index=False)

def main(urls):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for url in urls:
        new_data, station_name = fetch_data(url)
        csv_filename = os.path.join(script_dir, f'weather_data_{station_name}.csv')
        
        append_to_csv(new_data, csv_filename)
    
if __name__ == "__main__":
    urls = [
        'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=C0D59',
        'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=46757',
        'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=CAD03',
        'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=CAD04',
        'https://www.cwa.gov.tw/V8/C/W/OBS_Station.html?ID=CAD10'
    ]
    main(urls)
