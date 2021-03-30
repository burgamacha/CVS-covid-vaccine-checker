"""
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.
"""


import requests
import time
import beepy


def find_a_vaccine(hours_to_run: int = 3, refresh: int = 60, state: str = 'IL', cities: list[str] = ['Chicago']):
    state = state.upper()
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
              "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    if (state not in states) or (state.length() != 2):
        print("Please enter a valid state abbreviation.")
        return
    elif cities.length < 1:
        print("Please enter at least one city.")
        return
    else:
        max_time = time.time() + hours_to_run*60*60
        while time.time() < max_time:

            response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo"
                                    .format(state.lower()), headers={"Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"})
            payload = response.json()

            mappings = {}
            for item in payload["responsePayloadData"]["data"][state]:
                mappings[item.get('city')] = item.get('status')

            print(time.ctime())
            for city in cities:
                print(city, mappings[city])

            for key in mappings.keys():
                if (key in cities) and (mappings[key] != 'Fully Booked'):
                    beepy.beep(sound='coin')
                    break
                else:
                    pass

            time.sleep(refresh)
            print('\n')


# this final line runs the function
# your terminal will output the Chicago, IL every 60 seconds for 3 hours by default if no arguments are passed
find_a_vaccine(3, 60, 'ny', ['Rye', 'White Plains'])

