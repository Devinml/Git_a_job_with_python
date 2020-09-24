import requests
url = 'https://data.sba.gov/api/3/action/datastore_search?resource_id=ca6534fb-28eb-476d-91d8-f872152689e9&limit=5&q=title:jones'  

text = requests.get(url)
# fileobj = urllib.urlopen(url)
print(text.text)