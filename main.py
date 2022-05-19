import csv
import os
import geocoder
import time

def main():
    with open('data/raw_traffic.csv', 'r') as f, open('outputs/output2.csv', 'w', newline='') as w:
        reader = csv.reader(f)
        writer = csv.writer(w)
        next(reader, None)
        count = 0
        for row in reader:
            if count % 20 == 0:
                time.sleep(2)
                print('added {} records'.format(count))
            if int(row[4]) >= 10000 and int(row[4]) <= 40000:
                try:
                    latitude = row[2].split(',')[0]
                    longitude = row[2].split(',')[1].replace(' ', '')
                    g = geocoder.mapquest([latitude, longitude], method='reverse', key=os.environ['GEOCODER_KEY'])
                    out = g.json
                    address = out['address']
                    city = out['city']
                    county = out['county']
                    latlong = row[2].replace(' ', '')
                    writer.writerow([address, city, county, latlong, int(row[4])])
                    count += 1
                except Exception:
                    pass
if __name__ == "__main__":
    main()