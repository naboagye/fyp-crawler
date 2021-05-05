import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt, date, timedelta

''' function to determine if a country has a lockdown end date beyond the date of the 
start of the current week'''
def testDate(x):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    start = dt.combine(start, dt.min.time())
    return x >= start

# function to replace any date values that are ranges with just the end date 
def format(x):
    if len(x) > 10:
        return(x[-10:])
    else:
        return(x)

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
print(df)
# Removing unneccesary columns
df.drop('Place', inplace=True, axis=1)
df.drop('Start date', inplace=True, axis=1)
df.drop('Length (days)', inplace=True, axis=1)
df.drop('Level', inplace=True, axis=1)
df.drop('Total length (days)', inplace=True, axis=1)
# Renaming columns
df.columns = ['Country', 'L1', 'L2', 'L3']

# Determining the column with the end date of the latest lockdown
result = []
for index, row in df.iterrows():
    if row['L2'] == 0:
        result.append(row['L1'])
    elif row['L3'] == 0:
        result.append(row['L2'])
    else:
        result.append(row['L3'])
        
df['Lockdown End'] = result

# Dropping byproduct attributes in determining end date of lockdowns
df.drop('L1', inplace=True, axis=1)
df.drop('L2', inplace=True, axis=1)
df.drop('L3', inplace=True, axis=1)

# Removing dates that are ranges and replacing not "set dates" with zero values
df['Lockdown End'] = df['Lockdown End'].apply(format)

# Dropping any rows that don't have an end date in the format YYYY-MM-DD
df['Lockdown End'] = pd.to_datetime(df['Lockdown End'], format='%Y-%m-%d', errors='coerce')
df.dropna()

# Applying function to determine countries with a current lockdown
df['Current Lockdown?'] = df['Lockdown End'].apply(testDate)
df = df.loc[df['Current Lockdown?'] == True]
print(df)
