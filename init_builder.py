#! Python3
# This handy-dandy script builds a JSON config file for vaccine2.py
# Make all your config changes here, vaccine2.py will check config.json for
# changes.
# Run $ python init_builder.py from your repo folder for best results
# You'll want to update these fields:
# Recipients, sender, state, and cities
# All other variables are optional

import json
import time
from pathlib import Path

# Add more carriers by using this list:
# https://github.com/typpo/textbelt/blob/master/lib/carriers.js
# carriers also used for sender email address
# Add more for your email sender
wtf = {
    'really': True
}
carriers = {
    'att':      '@mms.att.net',
    'tmobile':  '@tmomail.net',
    'verizon':  '@vtext.com',
    'sprint':   '@page.nextel.com',
    'gmail':    '@gmail.com'
}
# Recipients of the SMS/email.
# cc and bcc are not used, but can be by adding
# ", ".join() on the variable assignment
recipients = {
    'to': [f"RECIPADDR{carriers['tmobile']}"],
    'cc': [],
    'bcc': []
}
# Sending from address. I set up a burner Gmail account
# to send. If you're using your own SMTP server, make
# sure you have a domain, SPF, and everything square
sender = {
    'from': f"SENDERADDR{carriers['gmail']}",
    'pass': 'SENDERPASS',
    'smtp': 'smtp.gmail.com',
    'port': 587
}
# Used for... things
timers = {
    'timer': 3600,
    'hours_to_run': 3,
    'sleeptimer': 10
}
# There can be only one
states = {
    'state': 'CA'
}
# Some towns and cities near me
# https://www.freemaptools.com/find-usa-cities-inside-radius.htm
# Enter a zip, 94116 in this case, and copy and paste the CSV output
# Also added a few cities that I'm willing to drive to
# There's a .upper() at the end
maplist = 'Davis,Dixon,Fairfield,Woodland,Winters,Sacramento,Lathrop,Antioch,San Francisco,Daly City,Brisbane,South San Francisco,Sausalito,Pacifica,San Bruno,Belvedere Tiburon,Millbrae,Oakland,Mill Valley,Alameda,Emeryville,Piedmont,Corte Madera,Berkeley,Larkspur,San Quentin,Richmond,Burlingame,Montara,Moss Beach,Albany,Greenbrae,Stinson Beach,Ross,Kentfield,El Cerrito,San Mateo,El Granada,Canyon,Bolinas,Fairfax,San Leandro,San Anselmo,Orinda,San Pablo,Belmont,El Sobrante,Half Moon Bay,San Rafael,Woodacre,San Lorenzo,Castro Valley,Moraga,Pinole,San Geronimo,San Carlos,Forest Knolls,Hayward,Hercules,Lagunitas,Lafayette,Nicasio,Rodeo,Martinez,Point Reyes Station,Crockett,Redwood City,Walnut Creek,Atherton,Menlo Park,Fremont,Olema,Union City,Port Costa,San Ramon,Pleasant Hill,Vallejo,Novato,Danville,Alamo,Stanford,Newark,Palo Alto,Diablo,Portola Valley,Concord'.upper()
cities = sorted(maplist.split(","))

curlstuff = {
    'cvs_url': f"https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{states['state'].lower()}.json?vaccineinfo",
    'header': "https://www.cvs.com/immunizations/covid-19-vaccine"
}
# if the file is not there, we are not modifying the config
modified = Path('config.json').exists()
# Final list of data
data = {
    'wtf': wtf,
    'carriers': carriers,
    'recipients': recipients,
    'sender': sender,
    'timers': timers,
    'states': states,
    'cities': cities,
    'curlstuff': curlstuff,
    'modified': modified
}

# Write the file
if modified:
    data['modified'] = True
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)
else:
    with open("config.json", "w") as outfile:
        json.dump(data, outfile)

# Just F*n with your brain, just wanted to use the not operator
if not modified:
    print(f"File config.json created in {Path.cwd()}")
    print(f"With a creation date of {time.ctime(Path('config.json').stat().st_ctime)}")
else:
    print(f"File config.json modified in {Path.cwd()}")
    print(f"File modified on {time.ctime(Path('config.json').stat().st_mtime)}")