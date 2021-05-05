import requests

url = "https://api.covid19api.com/premium/travel/country/united-kingdom"

payload = {}
headers = {
  'X-Access-Token': '5cf9dfd5-3449-485e-b5ae-70a60e997864'
}

response = requests.get(url, headers=headers, data = payload)

#print(response.text.encode('utf8'))
print(response.json()['Notes'][0]['Note'])