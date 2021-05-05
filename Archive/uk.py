import requests
from json import dumps


ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
AREA_TYPE = "overview"
AREA_NAME = "england"

filters = [
    f"areaType={ AREA_TYPE }"
]

structure = {
    "date": "date",
    "dailyCases": "newCasesByPublishDate",
    "percentage": "newCasesByPublishDateChangePercentage",
    "rate": "newCasesBySpecimenDateRollingRate"
}

rate = {
    "rate": "newCasesBySpecimenDateRollingRate"
}

api_params = {
    "filters": str.join(";", filters),
    "structure": dumps(structure, separators=(",", ":")),
    "latestBy": "newCasesByPublishDate"
}

api_params2 = {
    "filters": str.join(";", filters),
    "structure": dumps(rate, separators=(",", ":")),
    "latestBy": "newCasesBySpecimenDateRollingRate"
}

formats = [
    "json"
]


for fmt in formats:
        api_params["format"] = fmt
        response = requests.get(ENDPOINT, params=api_params, timeout=10)
        assert response.status_code == 200, f"Failed request for {fmt}: {response.text}"
        res = response.json()
        
        response2 = requests.get(ENDPOINT, params=api_params2, timeout=10)
        assert response2.status_code == 200, f"Failed request for {fmt}: {response.text}"
        res2 = response2.json()
        
        date = res["data"][0]["date"]
        dailyCases = res["data"][0]["dailyCases"]
        percentage = res["data"][0]["percentage"]
        rate = res2["data"][0]["rate"]

#for fmt in formats:
#    api_params["format"] = fmt
#    response = get(ENDPOINT, params=api_params, timeout=10)
#    assert response.status_code == 200, f"Failed request for {fmt}: {response.text}"
#    print(f"{fmt} data:")
#    print(response.content.decode())

print(date, dailyCases, percentage, rate)