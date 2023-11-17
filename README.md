# Weather Data Scraper and Updater

This repository contains a Python script for scraping weather data from the CWA website and a GitHub Actions workflow to run this script daily at 12 PM GMT+8. The script fetches the latest weather data, appends it to a CSV file, and commits this updated file back to the repository.

## How It Works

- The `get_weather.py` fetches weather data from a public weather data website.
- The data is extracted from an HTML table that is dynamically loaded using JavaScript.
- This data is then appended to a CSV file (`weather_data.csv`) if it exists, and created if it does not.
- The GitHub Actions workflow (`daily-script-run.yml`) is scheduled to run this script daily.
- The updated CSV file is then committed and pushed back to the repository.

## Setup

### Requirements

- Python 3.11
- Libraries: `pandas`, `requests_html`
