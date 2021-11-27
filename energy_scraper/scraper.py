#! /usr/bin/env python3
from urllib import request
from bs4 import BeautifulSoup

ENERGY_DASHBOARD_LIVE_URL = 'https://www.energydashboard.co.uk/live'

raw_content = request.urlopen(ENERGY_DASHBOARD_LIVE_URL)
raw_html = raw_content.read()
soup_html = BeautifulSoup(raw_html, 'html.parser')

soup_title = soup_html.find('h3')
_, title_time = soup_title.text.split('-')
title_time = title_time.strip()
print(title_time)

colon_index = title_time.find(':')
if colon_index:
    time, period = title_time[colon_index-2:].split(' ')
    print(time, period, sep='*')

soup_labels = soup_html.find_all(class_=['label'])

values = [''.join(label.text.split()) for label in soup_labels if 'Current' not in label.text and 'Total' not in label.text]
print(values)

energy_supply = {}

for v in values:
    name, percent = v.split('-')
    percent = percent.replace('%', '')
    energy_supply[name] = percent
    print(name, percent)

print(energy_supply)
