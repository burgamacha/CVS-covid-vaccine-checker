"""
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.

To use with a Discord webhook, save the webhook in your .env as webhook="<your url here>"
"""


from typing import List
from os import environ
import sys
import requests
import time
import beepy
from discord import Webhook, RequestsWebhookAdapter
from flask import Flask
from threading import Thread

# code to keep got awake when being web-hosted on Repl.it
app = Flask('')


@app.route('/')
def main():
    return "Your webhook is ready"


def run():
    app.run(host="0.0.0.0", port=8000)


def keep_alive():
    server = Thread(target=run)
    server.start()


def find_a_vaccine(discord: bool = False, hours_to_run: int = 3, refresh: int = 60, state: str = 'IL',
                   cities: List[str] = ['Chicago']):
    state = state.upper()
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
              "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    if (state not in states) or (len(state) != 2):
        print("Please enter a valid state abbreviation.")
        return
    elif len(cities) < 1:
        print("Please enter at least one city.")
        return
    else:
        max_time = time.time() + hours_to_run*60*60
        while time.time() < max_time:  # change to True to run indefinitely after deployed with Flask

            response = requests.get("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo"
                                    .format(state.upper()), headers={"Referer": "https://www.cvs.com/immunizations/covid-19-vaccine"})
            payload = response.json()

            mappings = {}
            for item in payload["responsePayloadData"]["data"][state]:
                mappings[item.get('city')] = item.get('status')

            print(time.ctime())
            for city in cities:
                print(city + ":", mappings[city.upper()])

            for key in mappings.keys():
                if (key.capitalize() in cities) and (mappings[key] != 'Fully Booked'):
                    if discord:
                        webhook = Webhook.from_url(environ['webhook'], adapter=RequestsWebhookAdapter())
                        webhook.send(key.capitalize() + " has an opening!")
                    else:
                        beepy.beep(sound='coin')
                    break
                else:
                    pass

            time.sleep(refresh)
            print('Checking the internets.\n')


# this will run Flask and let UptimeRobot keep the webhooks going
keep_alive()

# this final line runs the function
# your terminal will output the Chicago, IL every 60 seconds for 3 hours by default if no arguments are passed
# find_a_vaccine(True,3,60,'NY',['Elmsford','Harrison','Larchmont','Mamaroneck','Rye','Rye Brook','White Plains'])
a = sys.argv
n = len(a)
if n > 1:
    c = a[5:n]
    find_a_vaccine(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], c)
else:
    find_a_vaccine()
