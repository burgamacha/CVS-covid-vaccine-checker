'''
Forked from https://github.com/burgamacha/CVS-covid-vaccine-checker

This script scrapes the CVS website looking for vaccine appointments in the cities you list.

There are three required files, vaccine2.py, init_builder.py, and config.json
THESE MUST BE IN THE SAME DIRECTORY OR YOU WILL HAVE PAIN AND SUFFERING

To change the configuration, please use the init_builder.py script
Changes to config.json will be updated on the next pass

This script requires the requests module, which you can install with:

pip install requests

Happy vaccination!
'''
import requests
import time
import smtplib
import json
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def send(message, thetime, state, cdata):
    to_number = cdata['recipients']['to'][0] # ", ".join() for multiple
    sender = cdata['sender']['from']
    password = cdata['sender']['pass']
    subject = f"CVS Availability in {state}"
    # prepend thetime
    message.insert(0, thetime.strftime("%m/%d/%Y, %H:%M %p"))
    # append the link
    if len(message) == 1:
        message.append('No new appointments available.')
    else:
        message.append('https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns')

    port = cdata['sender']['port']
    smtp_server = cdata['sender']['smtp']
    msg_body = ", ".join(message)

    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = to_number
    msg['subject'] = subject
    part = MIMEText(msg_body, 'plain', 'UTF-8')
    msg.attach(part)
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( smtp_server, port )
    server.starttls()
    server.login(sender, password)

	# Send text message through SMS gateway of destination number
    server.sendmail( sender, to_number, msg.as_string())
    server.quit()

def findAVaccine():
    cdata = get_cdata()
    init_time = datetime.now()
    timer = cdata['timers']['timer']
    hours_to_run = cdata['timers']['hours_to_run']
    max_time = init_time + timedelta(hours=hours_to_run)

    state = cdata['states']['state']
    cvs_url = cdata['curlstuff']['cvs_url']
    header = cdata['curlstuff']['header']

    cities = cdata['cities']

    previousmessage = []

    while datetime.now() < max_time:

        thetime = datetime.now()
        message = []

        response = requests.get(cvs_url, headers={"Referer":header})
        payload = response.json()

        print(thetime)

        # Use .get() method on JSON from APIs for error handling. Though we do nothing here :D
        for item in payload.get('responsePayloadData').get('data').get(state):

            city = item.get('city')
            status = item.get('status')

            if (city in cities) and (status == 'Available'):
                message.append(f"{city}, {state} -- {status}")
                print(f"{city}, {state} -- {status}")

        print()

        # Decouple the checking to sending alerts
        # if no change for an hour, just send a message that there's no change
        if (message != previousmessage) or ((thetime - init_time).total_seconds() > timer):
            # set previous to this new one
            previousmessage = message[:]
            # reset the timer
            init_time = datetime.now()
            # send the email!
            print('Sending status update...')
            send(message, thetime, state, cdata)
        
        # This runs every 300 seconds (5 minutes)
        # Email will be sent every hour, or when a change is detected
        time.sleep(cdata['timers']['sleeptimer'])

        # Check for new config
        # Kinda boneheaded, I'm too stupid/hungover to figure out how 
        # to track changes to a file using Path('config.json').stats().ts_mtime
        # and reload only if there's a change in the file
        d = get_cdata()
        if cdata['modified']:
            print('Oh, hey, new config... applying.')
            d['modified'] = False
            cdata = d
            # Write out the changes, so we know
            with open("config.json", "w") as outfile:
                json.dump(d, outfile)
            # Go on
            max_time = init_time + timedelta(hours=cdata['timers']['hours_to_run'])
            timer = cdata['timers']['timer']
            hours_to_run = cdata['timers']['hours_to_run']
            max_time = init_time + timedelta(hours=hours_to_run)

            state = cdata['states']['state']
            cvs_url = cdata['curlstuff']['cvs_url']
            header = cdata['curlstuff']['header']
            # I'd hazard a guess only the cities that CVS offers gets updated
            cities = cdata['cities']
            print('Done.')

def get_cdata():
    if Path('config.json').exists():
        # Get the config file
        with open('config.json') as config_file:
            cdata = json.load(config_file)
            return cdata
    else:
        print(f"Could not open or read file: {Path.cwd()}. Did you forget to run init_builder.py?")
        exit()

if __name__ == '__main__':

    try:
        # Main loop
        findAVaccine()
    except KeyboardInterrupt:
        print('Exiting...')
