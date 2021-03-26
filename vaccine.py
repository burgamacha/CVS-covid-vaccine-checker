#!/usr/bin/env python3
#
"""
This script scrapes the CVS website looking for vaccine appointments in the cities you list.

Usage: ./vaccine.py --state [STATE] --cities [CITIES] --duration [HOURS]

Required arguments:

    STATE       the two-letter abbreviation for your state (e.g., IL, CA, etc.)
    CITIES      a JSON file containing an array of strings, which list all the cities
                you are willing to travel to for a vaccination.

Optional (default will be used if not specified):

    HOURS       how long should this script run for (default: 3)
    INTERVAL    how often to run the check in minutes (default: 10)

"""

import requests
import time

HAS_SOUND = True
try:
    import beepy
except ImportError:
    HAS_SOUND = False

# TODO: Read this from a configuration file
# TODO: Even better, derive it automatically from the user's location and a --distance in miles.
CITIES = [
    "Alameda",
    "Berkeley",
    "Concord",
    "Cupertino",
    "Daly City",
    "Danville",
    "Dublin",
    "Emeryville",
    "Fremont",
    "Hayward",
    "Los Gatos",
    "Martinez",
    "Mill Valley",
    "Milpitas",
    "Oakland",
    "Palo Alto",
    "Pleasanton",
    "Redwood City",
    "Richmond",
    "San Francisco",
    "San Jose",
    "San Leandro",
    "San Mateo",
    "San Rafael",
    "San Ramon",
    "Union City",
    "Vallejo",
    "Walnut Creek",
]


def find_vaccine(hours, interval, state, cities):
    """ Scrapes the CVS website looking for available appointments in one of the `cities`

    :param hours: how long to run this script for
    :param interval: how often to run it (in minutes)
    :param state: a two-letter State abbreviation
    :param cities: a list of cities to look up

    :return: if an available appointment is found, a map of where to go book it
    """

    # When to stop, with duration (given in hours) converted to seconds.
    max_time = time.time() + hours * 60 * 60

    # How often to run the check, in minutes.
    interval = interval * 60

    while time.time() < max_time:
        print(time.ctime())
        result = scrape(state, cities)
        if HAS_SOUND:
            beepy.beep(sound='coin') if result["found"] else beepy.beep(sound='error')
        if result["found"]:
            print(f"Available in {result['available']}")
        else:
            print(f"Nothing available at this time, there are {len(result['others'])} "
                  f"other locations with available appointments")
        print('----------- \n')
        time.sleep(interval)


def scrape(state, cities):
    cities = [c.lower() for c in cities]
    response = requests.get(
        f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{state.lower()}"
        ".json?vaccineinfo",
        headers={"Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"})
    payload = response.json()
    mappings = {}
    for item in payload["responsePayloadData"]["data"][state]:
        mappings[item.get('city').lower()] = item.get('status')

    result = {
        "found": False,
        "missing": [],
        "available": [],
        "others": []
    }
    for city in cities:
        if city not in mappings:
            result["missing"].append(city)
        else:
            if mappings[city] != 'Fully Booked':
                result["available"].append(city)
                result["found"] = True
    if not result["found"]:
        for city, status in mappings.items():
            if status != 'Fully Booked':
                result["others"].append(city)
    return result


if __name__ == "__main__":
    # TODO: read these from parse_args
    hours = 3
    state = 'CA'
    interval = 10

    print(f"Running Vaccine appointment check for {hours} hours, every {interval} minutes")
    print(f"Checking against a list of {len(CITIES)} cities")
    find_vaccine(hours=hours, interval=interval, state=state, cities=CITIES)
