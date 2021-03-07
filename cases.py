import requests
import pandas as pd

url = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'

df = pd.read_csv(url)

df = df.filter(['Name', 'Cases - newly reported in last 7 days per 100000 population', 'Cases - newly reported in last 24 hours'])

cases_100000 = df.loc[df['Name']==f'{country}', 'Cases - newly reported in last 7 days per 100000 population'].values[0]
cases_24 = df.loc[df['Name']==f'{country}', 'Cases - newly reported in last 24 hours'].values[0]