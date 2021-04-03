'''
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install requests

in your terminal.
'''
import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils

def send(message, state):
    carriers = {
        'att':      '@mms.att.net',
        'tmobile':  '@tmomail.net',
        'verizon':  '@vtext.com',
        'sprint':   '@page.nextel.com',
        'gmail':    '@gmail.com'
    }
    # Replace the receivernumber, sender, and password with your own, and consider using an argument\dict for multiple senders.
    # To use gmail, you need to allow less security apps to connect
    to_number = f"RECEIVERNUMBER{carriers['tmobile']}" # ", ".join() for multiple
    sender = 'SENDER' 
    password = 'PASSWORD'
    subject = f"CVS Availability in {state}"
    # Append link
    if len(message) == 1:
        message.append('No new appointments available.')
    else:
        message.append('https://www.cvs.com/vaccine/intake/store/covid-screener/covid-qns')

    port = 587 # 587 for starttls, 465 for SSL and use ssl
    smtp_server = "smtp.gmail.com"
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
    hours_to_run = 3 ###Update this to set the number of hours you want the script to run.
    max_time = time.time() + hours_to_run*60*60
    while time.time() < max_time:

        state = 'CA' ###Update with your state abbreviation. Be sure to use all CAPS, e.g. RI

        ###Update with your cities nearby
        cities = ['ALAMEDA', 'ALBANY', 'BERKELEY', 'CHICO', 'COLMA', 'DALY CITY', 'DAVIS', 'DANVILLE', 'DIXON', 'EL CERRITO', 'FAIRFIELD', 'SAN FRANCISCO', 'OAKLAND', 'WOODLAND', 'SACRAMENTO']

        message = []

        response = requests.get(f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{state.lower()}.json?vaccineinfo", headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
        payload = response.json()

        thetime = time.ctime()
        print(thetime)
        message.append(thetime)

        for item in payload["responsePayloadData"]["data"][state]:

            city = item.get('city')
            status = item.get('status')

            if (city in cities) and (status != 'Fully Booked'):
                message.append(f"{city}, {state} -- {status}")
                print(f"{city}, {state} -- {status}")

        print('\n')
        send(message, state)
        time.sleep(3600) ##This runs every 1 hour (in seconds). Update here if you'd like it to go every 10min (600sec)

findAVaccine() ###this final line runs the function. Your terminal will output the cities every 60seconds
