'''
This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations commented below.

If you receive an error that says something is not installed, type

pip install requests
etc.

Happy vaccination!
'''
import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def send(message, thetime, state):
    carriers = {
        'att':      '@mms.att.net',
        'tmobile':  '@tmomail.net',
        'verizon':  '@vtext.com',
        'sprint':   '@page.nextel.com',
        'gmail':    '@gmail.com'
    }
    # Replace the receivernumber, senderaddr, and senderpass with your own
    # Consider using a list for multiple recievers.
    # To use gmail, you need to allow less secure apps to connect
    # Also, probably a good idea to set up a burner gmail for the sending
    to_number = f"RECEIVERNUMBER{carriers['tmobile']}" # ", ".join() for multiple
    sender = f"SENDERADDR{carriers['gmail']}" 
    password = 'SENDERPASS'
    subject = f"CVS Availability in {state}"
    # prepend thetime
    message.insert(0, thetime.strftime("%m/%d/%Y, %H:%M %p"))
    # append the link
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
    timer = 3600
    init_time = datetime.now()
    hours_to_run = 3 ###Update this to set the number of hours you want the script to run.
    max_time = init_time + timedelta(hours=hours_to_run)

    state = 'CA' ###Update with your state abbreviation. Be sure to use all CAPS, e.g. RI
    cvs_url = f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{state.lower()}.json?vaccineinfo"
    header = "https://www.cvs.com/immunizations/covid-19-vaccine"

    ###Update with your cities nearby
    cities = ['ALAMEDA', 'ALAMO', 'ALBANY', 'ANTIOCH', 'BERKELEY', 'CHICO', 'COLMA', 'CUPERTINO', 'DALY CITY', 'DAVIS',
    'EAST PALO ALTO', 'HAYWARD', 'LAFAYETTE', 'LATHROP', 'LIVERMORE', 'LOS GATOS', 'DANVILLE', 'DIXON', 'DUBLIN', 'EL CERRITO',
    'ELK GROVE', 'EMERYVILLE' 'FAIRFIELD', 'FREMONT', 'MENLO PARK', 'SAN FRANCISCO', 'OAKLAND', 'WOODLAND', 'SACRAMENTO',
    'STOCKTON', 'VACAVILLE', 'VALLEJO', 'WALNUT CREEK', 'MILL VALLEY', 'MORAGA', 'NEWARK', 'NOVATO', 'ORINDA', 'PITTSBURG',
    'PINOLE', 'PLEASANT HILL', 'REDWOOD CITY', 'RICHMOND', 'SAN ANSELMO', 'SAN BRUNO', 'SAN CARLOS', 'SAN LEANDRO', 'SAN MATEO',
    'SAN RAFAEL', 'SAN RAMON', 'SAUSALITO', 'SARATOGA'
    ]

    previousmessage = []

    while datetime.now() < max_time:

        thetime = datetime.now()
        message = []

        response = requests.get(cvs_url, headers={"Referer":header})
        payload = response.json()

        print(thetime)    

        for item in payload["responsePayloadData"]["data"][state]:

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
            send(message, thetime, state)
        
        # This runs every 300 seconds (5 minutes)
        # Email will be sent every hour, or when a change is detected
        time.sleep(300)

if __name__ == '__main__':
    try:
        findAVaccine()
    except KeyboardInterrupt:
        print('Exiting...')
