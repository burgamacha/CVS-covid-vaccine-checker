'''
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.
'''

import requests
import time

HAS_SOUND = True
try:
    import beepy
except ImportError:
    HAS_SOUND = False

def findAVaccine():
    hours_to_run = 3  ###Update this to set the number of hours you want the script to run.
    max_time = time.time() + hours_to_run * 60 * 60
    while time.time() < max_time:

        state = 'CA'  ###Update with your state abbreviation. Be sure to use all CAPS, e.g. RI

        response = requests.get(
            "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo".format(
                state.lower()),
            headers={"Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"})
        payload = response.json()

        mappings = {}
        for item in payload["responsePayloadData"]["data"][state]:
            mappings[item.get('city').lower()] = item.get('status')

        print(time.ctime())
        cities = [c.lower() for c in ["San Francisco", "Berkeley", "Oakland",
                                      "Emeryville",
                                      "San Leandro", "San Rafael", "Mill Valley", "San Mateo",
                                      "Redwood City", "Daly City", "Walnut Creek", "San Ramon",
                                      "Fremont", "Vallejo", "Richmond", "Martinez", "Concord",
                                      "Danville", "Hayward", "Union City", "San Jose", "Milpitas",
                                      "Cupertino", "Palo Alto", "Alameda", "Dublin", "Pleasanton", "Los Gatos"]]

        found = False
        print(time.ctime())
        for city in cities:
            if city not in mappings:
                print(f">>> Missing: {city}")
            else:
                if mappings[city] != 'Fully Booked':
                    if HAS_SOUND:
                        beepy.beep(sound='coin')
                    print(f"****************  {city}")
                    found = True
        if not found:
            if HAS_SOUND:
                beepy.beep(sound='error')
            print("Nothing available :(")
            count = 0
            for city, status in mappings.items():
                if status != 'Fully Booked':
                    count += 1
            print(f"Available elsewhere: {count}")

        time.sleep(600)
        print('----------- \n')


if __name__ == "__main__":
    findAVaccine()
