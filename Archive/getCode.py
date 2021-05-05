import requests

def getCode(country):
    country_url = f"https://restcountries.eu/rest/v2/name/{country}"
    response = requests.get(country_url).json()
    iso2 = response[0]['alpha2Code']
    flag = response[0]['flag']
    print(iso2)

getCode("France")