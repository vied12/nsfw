import requests
import csv
import datetime
import json
import sys


def retrieve(date, state=None):
    print
    params = {
        'pollutant': 'PM1',
        'date': date.strftime('%Y%m%d'),
        'state': state or '',
    }
    resp = requests.get('https://www.umweltbundesamt.de/en/luftdaten/stations/locations.csv?\
    pollutant={pollutant}&data_type=1TMW&date={date}\
    &hour=12&statename=&state={state}'.format(**params))
    content = resp.content.decode('utf8')
    data = {
        'date': date.strftime('%Y/%m/%d'),
        'state': state,
        'stations': {}
    }
    for row in list(csv.reader(content.splitlines(), delimiter=';'))[1:]:
        data['stations'][row[0]] = {'PM1': row[2], 'location_name': row[1]}
    return data

if __name__ == '__main__':
    if len(sys.argv) > 1:
        date = tuple(map(lambda _: int(_), sys.argv[1].split('/')))
        date = datetime.date(*date)
    else:
        date = datetime.datetime.now().date()
    state = None
    if len(sys.argv) > 2:
        state = sys.argv[2]
    data = retrieve(date, state)
    print(json.dumps(data))
