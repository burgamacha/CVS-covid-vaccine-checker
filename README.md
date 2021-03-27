<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![MIT License][blog-shield]][blog-url]
<!-- ABOUT THE PROJECT -->
## About The CVS Vaccine Checker

This script checks for covid-19 vaccines near you. 

To run it, you'll need python 3.x installed on your computer, along with the packages requests, beepy, and time. See here for how to install those from code academy: https://www.codecademy.com/articles/install-python

Once you have those, save the script in a folder on your desktop. You'll need to open the script and do some very easy editing that I've marked out using `###`. There are instructions at the top for you too :) This should be easy enough for someone comfortable with technology. Ask for help on NextDoor - it's where I answer a lot of tech questions for my neighbors!

Once you've updated the script with your state and cities, navigate your command line from the tutorial above to that folder, and type `python3 vaccine.py`. Like magic, it will run!

## Usage

This script is for monitoring the appointment website without clicking refresh 1Billion times. It is not going to automatically book for you. And if you fork this and create an automated booking applet, I will personally send 1000 adolscent, chewing puppies to your house. And nobody wants that.  

### Google Maps API

To run the automated geolocation mapping, this script requires the use of the [`googlemaps` Python library][googlemaps], and a Google Maps API Key.

Google API Keys are described [here][api_keys] while the documentation for the `googlemaps` API is [here][googlemaps_docs], but all you need for your purposes is:

    pip install googlemaps

Once you have the API Key, you will need to make it available to the script via an environment variable:

    export GOOGLEMAPS_API_KEY = "AKzbSy...hi899"

### Running

With this, you can run the script as follows:

```shell
$ ./vaccine.py Oakland,CA

Running Vaccine appointment check for 3 hours, every 10 minutes
Looking for available locations within 100 miles of Oakland, CA
Fri Mar 26 18:22:23 2021
Nothing available at this time, there are 12 other locations with available appointments
----------- 
...
```

or:

```shell
$ ./vaccine.py --duration 1 --interval 5 --distance 20 Oakland,CA

Running Vaccine appointment check for 1 hours, every 5 minutes
Looking for available locations within 20 miles of Oakland, CA
Fri Mar 26 18:36:33 2021
Nothing available at this time, there are 12 other locations with available appointments
```


## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/burgamacha/CVS-vaccine-checker.svg?style=for-the-badge
[contributors-url]: https://github.com/burgamacha/CVS-vaccine-checker/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/burgamacha/CVS-vaccine-checker.svg?style=for-the-badge
[forks-url]: https://github.com/burgamacha/CVS-vaccine-checker/network/members
[stars-shield]: https://img.shields.io/github/stars/burgamacha/CVS-vaccine-checker.svg?style=for-the-badge
[stars-url]: https://github.com/burgamacha/CVS-vaccine-checker/stargazers
[license-shield]: https://img.shields.io/github/license/burgamacha/CVS-vaccine-checker.svg?style=for-the-badge
[license-url]: https://github.com/burgamacha/CVS-vaccine-checker/blob/master/LICENSE.txt
[blog-shield]: https://img.shields.io/badge/medium-Read%20about%20this%20on%20Medium-lightgrey.svg?style=for-the-badge
[blog-url]: https://python.plainenglish.io/how-i-built-a-cvs-vaccine-appointment-availability-checker-in-python-6beb379549e4
[googlemaps]: https://github.com/googlemaps/google-maps-services-python
[api_keys]: https://cloud.google.com/docs/authentication/api-keys
[googlemaps_docs]: https://googlemaps.github.io/google-maps-services-python/docs/index.html
