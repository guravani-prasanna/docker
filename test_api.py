import requests

url = "http://127.0.0.1:8000/decrypt-seed"
payload = {"encrypted_seed": "PASTE_YOUR_BASE64_STRING_HERE"}
response = requests.post(url, json=payload)
print(response.json())