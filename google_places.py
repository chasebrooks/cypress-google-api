import csv
import os
import requests
import time

def get_place_ids():
    """
    To get final formatting:
    1. remove duplicates in excel
    2. Filter for name contains "storage" or "mini warehouse"
    """

    # given list of target road longitude/latitudes, get list of all surrounding storage facilities
    georgia_publicly_traded_companies_cities = ['Atlanta','Austell','Cumming','Chamblee','College Park','Decatur',
                                    'Doraville','Dunwoody','Fayetteville','Hapeville','Jonesboro',
                                    'Kennesaw','Lawrenceville','Lithonia','Mableton','Marietta','Norcross',
                                    'Peachtree City','Peachtree Corners','Riverdale','Smyrna','Stone Mountain',
                                    'Woodstock','Fort Oglethorpe','Columbus','Savannah','Warner Robbins','East Point']
    tennessee_publicly_traded_companies_cities = ['Chattanooga', 'Nashville', 'Hixson', 'Hendersonville', 'Memphis', 
                                                'Madison', 'Hermitage', 'Antioch']

    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    params = dict(
        keyword='storage OR mini warehouse -public -life -cube',
        radius='2500',
        key=os.environ['GOOGLE_API_KEY']
    )

    with open('data/TN_raw_traffic.csv', 'r') as f, open('outputs/TN/places_output.csv', 'w', newline='') as w:
        reader = csv.reader(f)
        writer = csv.writer(w)
        count = 0
        for row in reader:
            count += 1
            if count % 20 == 0:
                time.sleep(2)
                print('added {} records'.format(count))
            # exclude publicly traded company cities
            try:
                if row[1] not in tennessee_publicly_traded_companies_cities:
                    params['location'] = row[0].replace(' ', '')
                    resp = requests.get(url=url, params=params)
                    data = resp.json() 
                    for business in data['results']:
                        if business['business_status'] == 'OPERATIONAL':
                            writer.writerow([business['place_id'],business['name'], business['business_status']])  
            except Exception:
                pass
            

def get_place_details():
    url = 'https://maps.googleapis.com/maps/api/place/details/json'

    params = dict(
        key=os.environ['GOOGLE_API_KEY']
    )

    with open('outputs/TN/places_output.csv', 'r') as f, open('outputs/TN/places_details.csv', 'w', newline='') as w:
        reader = csv.reader(f)
        writer = csv.writer(w)
        next(reader, None)
        count = 0

        for row in reader:
            count += 1
            if count % 20 == 0:
                time.sleep(2)
                print('finished {} places'.format(count))
            try:
                params['place_id'] = row[0]

                resp = requests.get(url=url, params=params)
                data = resp.json() 

                # select data needed
                address = data['result']['formatted_address']
                phone = data['result']['formatted_phone_number']
                name = data['result']['name']
                maps_url = data['result']['url']
                try:
                    website = data['result']['website']
                except Exception:
                    website = ''
                writer.writerow([name, phone, address, maps_url, website])  
            except Exception:
                pass


if __name__ == '__main__':
    # get_place_ids()
    get_place_details()
