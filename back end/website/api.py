import requests
import json

url = "https://api.apilayer.com/fixer/latest?symbols=IRR&base=USD"

payload = {}
headers= {
  "apikey": "FlrvKqJtAc3XmMouYkcrN8IhZPVJR765"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
data = json.loads(result)
dollar = data['rates']['IRR']

