# CVS Vaccine Checker - 
##### _Powershell Revision_

Like the main branch, this script will be able to check CVS scheduling availablity for the covid-19 vaccine but basically re-writing burgamacha's python methods in powershell.  This version also includes the following:
 - Parameter 1: Lookup Zip (mandatory)
 - Parameter 2: Radius Distance in km (default 40)
 - Parameter 3: Stop in n Hours (default 3)
 - Parameter 4: Refresh interval Seconds (default 300)


## Usage
Save the included files in a folder on any Windows 10 system.  The cvs_checker.ps1 file and uszips.csv file are both required.  This can be run from within a powershell console window.  The checker will output to screen as well as create a log file with results called CVS_checker.txt in the same folder.

#### Execute with defaults:
```sh
.\cvs_checker.ps1 <zipcode>
```
#### Execute with parameters:
```sh
.\cvs_checker.ps1 -lookupzip <zipcode> -radiusdistkm <radiusinkm> -stopinhrs <stopinhrs> -refreshintsec <refreshintsec>
```
#### Example Run:
```sh
PS D:\Support> .\cvs_checker.ps1 -lookupzip 24540 -radiusdistkm 300
Starting CVS Checker at 6:50 PM
Zip code database provided by https://simplemaps.com/data/us-zips

Localities within 300km:
DANVILLE
CHATHAM
COVINGTON
MARTINSVILLE
SOUTH BOSTON

Checking until 9:50 PM - availability as of 6:50 PM:
CHATHAM Fully Booked
COVINGTON Fully Booked
DANVILLE Available
MARTINSVILLE Fully Booked
SOUTH BOSTON Fully Booked
```

## Automation
This script can be added to Windows 10 Task Scheduler so it can begin checking at a specified time or schedule. Creating a new task set the Action to Run a Program: "powershell"
And add additional flags "-File C:\folder\cvs_checker.ps1 -lookupzip 24540 -radiusdistkm 40"

## Supplemental
The script utilizes simplemaps.com's us-zip.csv file to perform zip code lookups and convert them to latitude/longitude coordinates which are then submitted to freemaptools to retrieve a list of localities within the radius variable provided.

 - https://simplemaps.com/data/us-zips
 - https://freemaptools.com/dint-cities-and-towns-inside-raidus.htm
