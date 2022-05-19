# cypress-google-api
Scrape self storage leads from google search API

## Main.py:
gets addresses linked to raw_traffic.csv longitude/latitudes tied to roads with average daily vehicle traffic of 10k-40k.

## google_places.py:
### get_place_ids:
- take longitude and latitude and return businesses with keyword storage or mini warehouse
- filter out cities that have a life storage (publicly traded)
- return relevant Google My Business info: business name, phone, address, google my business url, website (if applicable)
