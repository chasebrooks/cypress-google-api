import requests
import os


url = 'https://maps.googleapis.com/maps/api/place/details/json'

params = dict(
    key=os.environ['GOOGLE_API_KEY'],
    place_id='ChIJW__jdUPV-YgRKwsCsHCO4ME'
)

resp = requests.get(url=url, params=params)
data = resp.json()

address = data['result']['formatted_address']
phone = data['result']['formatted_phone_number']
name = data['result']['name']
maps_url = data['result']['url']
try:
    website = data['result']['website']
except Exception:
    website = ''
print(name, phone, address, url, website)
