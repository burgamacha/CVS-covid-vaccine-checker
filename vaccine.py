#!/usr/bin/env python3
#
"""
This script scrapes the CVS website looking for vaccine appointments in the cities you list.

Usage: ./vaccine.py [--distance MILES] [--duration HOURS] [--interval INTERVAL] LOCATION

Required arguments:

    LOCATION    comma-separated {City, State} pair; the State is the two-letter abbreviation for
                your state (e.g., IL, CA, etc.). For example, Chicago,IL.

                NOTE: do not use space around the comma (or use quotes).

                If the city contains spaces, or you need to use spaces around the comma, surround
                the argument with quotes:
                    "San Jose, CA"

Optional (default will be used if not specified):

    MILES       how far are you willing to travel from your LOCATION, in miles (default: 100)
    HOURS       how long should this script run for (default: 3)
    INTERVAL    how often to run the check in minutes (default: 10)

"""

import argparse
import geoloc
import requests
import time

HAS_SOUND = True
try:
    import beepy
except ImportError:
    HAS_SOUND = False


def find_vaccine(hours, interval, city, state, distance):
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
        result = scrape(city, state, distance)
        if HAS_SOUND:
            beepy.beep(sound='coin') if result["found"] else beepy.beep(sound='error')
        if result["found"]:
            print(f"Available in {result['available']}")
        else:
            print(f"Nothing available at this time, there are {len(result['others'])} "
                  f"other locations with available appointments")
        print('----------- \n')
        time.sleep(interval)


def scrape(city, state, distance):
    # cities = [c.lower() for c in cities]
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
    for dest, status in mappings.items():
        if status != 'Fully Booked':
            how_far = geoloc.get_distance(city, dest, miles=True)
            if how_far <= distance:
                result["available"].append(dest)
                result["found"] = True
            else:
                result["others"].append(dest)
    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--distance", type=int, default=100,
        help="how far are you willing to travel from your LOCATION, in miles (default: 100)"
    )
    parser.add_argument(
        "--duration", type=int, default=3,
        help="how long should this script run for (default: 3)"
    )
    parser.add_argument(
        "--interval", type=int, default=10,
        help="how often to run the check in minutes (default: 10)"
    )
    parser.add_argument(
        "LOCATION",
        help="comma-separated {City, State} pair; the State is the two-letter abbreviation for; "
             "your state (e.g., IL, CA, etc.). For example, Chicago,IL.\n"
             "NOTE: do not use space around the comma (or use quotes).\n"
             "If the city contains spaces, or you need to use spaces around the comma, surround; "
             "the argument with quotes: --where \"San Jose, CA\""
    )

    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    city, state = options.LOCATION.split(",")

    print(f"Running Vaccine appointment check for {options.duration} hours, every "
          f"{options.interval} minutes")
    # print(f"Checking against a list of {len(CITIES)} cities")

    print(f"Looking for available locations within {options.distance} miles of {city}, {state}")

    find_vaccine(
        hours=options.duration,
        interval=options.interval,
        city=city,
        state=state,
        distance=options.distance
    )
