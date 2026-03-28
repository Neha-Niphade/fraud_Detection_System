import requests
print("Test script started...")
url = "http://127.0.0.1:5000/predict"

data = {
    "features": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,100]
}

response = requests.post(url, json=data, timeout=5)

print("Status Code:", response.status_code)
print("Raw Response:", response.text)

try:
    print("JSON:", response.json())
except:
    print("No JSON response")