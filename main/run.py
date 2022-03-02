import requests
req = requests.get('http://adminApp:8000/api/user')     # TODO: update this link
print(req.text)
