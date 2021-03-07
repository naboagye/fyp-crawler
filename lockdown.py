import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt, date, timedelta
#import wikipedia

def test(x):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    test_date = dt.strptime(x.strip(), "%Y-%m-%d").date()
    return test_date >= start

# Getting correct table
url = "https://en.wikipedia.org/wiki/COVID-19_lockdowns"
df = pd.read_html(url, match='COVID-19 pandemic lockdowns')
df = df[0]

# Removing unneccesary table headers
df.columns = df.columns.get_level_values(2)    

# Including only national lockdowns in dataframe
df = df.loc[df['Level'] == "National"]

# Removing brackets with hyperlinks from dates
df = df.replace(r"\[.*?\]","",regex=True)
df = df.replace(r"\(.*?\)","",regex=True)

# Replacing empty spaces or NaN with 0
df = df.fillna(0)

# Removing unneccesary columns
df.drop('Place', inplace=True, axis=1)
df.drop('Start date', inplace=True, axis=1)
df.drop('Length (days)', inplace=True, axis=1)
df.drop('Level', inplace=True, axis=1)

# Renaming columns
df.columns = ['Country', 'L1', 'L2', 'L3']

result = []
for index, row in df.iterrows():
    if row['L2'] == 0:
        result.append(row['L1'])
    elif row['L3'] == 0:
        result.append(row['L2'])
    else:
        result.append(row['L3'])
        
df['Lockdown End'] = result
df.drop('L1', inplace=True, axis=1)
df.drop('L2', inplace=True, axis=1)
df.drop('L3', inplace=True, axis=1)
df['Lockdown End'] = df['Lockdown End'].replace(['2020-04-21to 2020-05-04'], "2020-05-04")
df['Lockdown End'] = df['Lockdown End'].replace(['not set'], 0)
df.drop( df[ df['Lockdown End'] == 0 ].index , inplace=True)
df['Current Lockdown?'] = df['Lockdown End'].apply(test)
#df = df.loc[df['Current Lockdown?'] == True]
print(df)
#cv = wikipedia.page('COVID-19 lockdowns')
#refs = cv.references