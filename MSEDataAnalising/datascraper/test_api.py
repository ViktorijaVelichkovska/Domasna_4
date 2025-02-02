import requests

url = "http://127.0.0.1:8000/api/get-data/"
params = {"company_code": "ABC", "start_date": "2024-01-01", "end_date": "2024-01-31"}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())
