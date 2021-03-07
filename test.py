import requests

url = "https://api.covid19api.com/countries"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.json())
