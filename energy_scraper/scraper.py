#! /usr/bin/env python3
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup


ENERGY_DASHBOARD_LIVE_URL = 'https://www.energydashboard.co.uk/live'


def populate_object(input_data, output_object):
    for v in input_data:
        name, percent = v.split('-')
        name = name.lower()
        raw_percent = percent.replace('%', '') if '%' in percent else percent
        raw_percent = float(raw_percent)
        output_object[name] = raw_percent


# Step 1 - Get webpage data
datestamp = datetime.now().strftime('%Y%m%d')
raw_content = request.urlopen(ENERGY_DASHBOARD_LIVE_URL)
raw_html = raw_content.read()
soup_html = BeautifulSoup(raw_html, 'html.parser')

# Step 2 - Extract time
soup_title = soup_html.find('h3')
_, title_time = soup_title.text.split('-')
title_time = title_time.strip()
print(title_time)

colon_index = title_time.find(':')
if colon_index:
    display_time = title_time[colon_index-2:].strip()
    time_12hr = datetime.strptime(display_time, "%I:%M %p")
    time_24hr = datetime.strftime(time_12hr, "%H:%M")
    timestamp = datestamp + ''.join(time_24hr.split(':'))

# Step 3 - Extract energy supply mix
soup_labels = soup_html.find_all(class_=['label'])

values = [''.join(label.text.split()) for label in soup_labels if 'Current' not in label.text and 'Total' not in label.text]
print(values)

# Step 4 - Format data for transmission
current_supply = {}
cumulative = {}

populate_object(values[:3], current_supply)
populate_object(values[3:], cumulative)

energy_supply = {
    'timestamp': timestamp,
    'current': current_supply, 
    'cumulative': cumulative
}

print(energy_supply)
