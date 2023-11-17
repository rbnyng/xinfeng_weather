import requests
from requests_html import HTMLSession
import pandas as pd
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo


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
    data = tables[0]

    # Extracting the HTML content of the third column
    html_content = r.html.find('table', first=True).html
    column_session = HTMLSession()
    r_column = column_session.get(html=html_content)
    third_column_cells = r_column.html.find('table tr td:nth-of-type(3)')

    # Extract 'alt' text from images in each cell
    captions = []
    for cell in third_column_cells:
        img = cell.find('img', first=True)
        caption = img.attrs['alt'] if img and 'alt' in img.attrs else ''
        captions.append(caption)

    data.iloc[:, 2] = captions

    return data

def append_to_csv(new_data, filename):
    # Get the current year
    current_time_gmt8 = datetime.now(ZoneInfo('Asia/Taipei'))
    
    # Format the time column in new_data to include the current year
    new_data['觀測時間'] = new_data['觀測時間'].apply(lambda x: f"{current_time_gmt8.year}/{x}")
    new_data['觀測時間'] = pd.to_datetime(new_data['觀測時間'], format='%Y/%m/%d %H:%M')

    if os.path.isfile(filename):
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data = updated_data.astype({'觀測時間': 'str'})
        updated_data = updated_data.drop_duplicates()
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
