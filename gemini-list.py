import requests

API_KEY = "AIzaSyAH7aYrAZsTEf-XA9fz3crl0kRDl5hcmCQ"
LIST_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(LIST_ENDPOINT)
print(response.text)
