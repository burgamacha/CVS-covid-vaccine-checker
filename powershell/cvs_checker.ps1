# https://simplemaps.com/data/us-zips

param (
    [Parameter(Mandatory)]$lookupzip,
    $radiusdistkm = "40",
    [int]$stopinhrs = 3,
    [int]$refreshintsec = 300
    )

$now = get-date
$stopat = $now.addhours($stopinhrs)

$runlog = $PSScriptRoot+"\CVS_checker.txt"

write-output "Starting CVS Checker at $($now.ToShortTimeString())" | Tee-Object -FilePath $runlog
write-output "Zip code database provided by https://simplemaps.com/data/us-zips`n"

$zipcodelist = get-content "$PSScriptRoot\uszips.csv" | convertfrom-csv

$latfromzip = [math]::round(($zipcodelist | where-object { $_.zip -eq $lookupzip }).lat,3)
$lngfromzip = [math]::round(($zipcodelist | where-object { $_.zip -eq $lookupzip }).lng,3)
$stfromzip = ( $zipcodelist | where-object { $_.zip -eq $lookupzip } ).state_id

$header = @{
    "Referer" = "https://www.freemaptools.com/find-cities-and-towns-inside-radius.htm"
    "path" = "/ajax/get-all-cities-inside.php?lat=$($latfromzip)&lng=$($lngfromzip)&sortaplha=0&radius=$radiusdist"
    }

$allLocalities = Invoke-RestMethod -uri "https://www.freemaptools.com/ajax/get-all-cities-inside.php?lat=$($latfromzip)&lng=$($lngfromzip)&sortaplha=0&radius=$radiusdistkm" -method get -headers $header

$cvsheader = @{
    'referer' = "https://www.cvs.com/immunizations/covid-19-vaccine"
    }

do {
    $loopstarttime = Get-Date
    $response = Invoke-RestMethod -Method Get "https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.$stfromzip.json?vaccineinfo" -headers $cvsheader
    $availabilitylist = $response.responsepayloaddata.data.$stfromzip
    $eligiblecities = (compare-object $availabilitylist.city $allLocalities.cities.city.name -excludedifferent -includeequal).inputobject
    if ( $loopstarttime.subtract($now).seconds -le 15 ) {
        write-output "Localities within $($radiusdistkm)km:" | tee-object -FilePath $runlog -Append
        write-output $eligiblecities | tee-object -FilePath $runlog -Append
        }

    write-output "`nChecking until $($stopat.ToShortTimeString()) - availability as of $($loopstarttime.ToShortTimeString()):" | Tee-Object -FilePath $runlog -Append
    
    foreach ( $city in $availabilitylist ) {
        if ( $eligiblecities -contains $city.city ) {
            write-output "$($city.city) $($city.status)" | Tee-Object -FilePath $runlog -Append
            if ( $city.status -match "Available" ) {
                [console]::beep(500,300)
                }
            }
        }

    start-sleep -s $refreshintsec

    }
until ($loopstarttime -ge $stopat)

write-output "`nStop Time Reached" | Tee-Object -FilePath $runlog -Append