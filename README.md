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
[![Blog][blog-shield]][blog-url]
<!-- ABOUT THE PROJECT -->
## About The CVS Vaccine Checker

This script checks for covid-19 vaccines near you. 

## Installation
1. Install Python. 
2. Run `pip install -r requirements.txt` to install all of the required
packages (`requests` and `beepy`). 
3. If you use [conda](https://conda.io), run `conda env create -f environment.yaml` and then activate the conda environment using `conda activate vacdev` before running the script.

This should be easy enough for someone comfortable with technology. Ask for help on NextDoor or Reddit - it's where I answer a lot of tech questions for my neighbors!

## Usage

Run the script with your chosen state and list of cities. For example, to search for appointments in NJ in the cities of Princeton and Plainsboro, run

```bash
python vaccine.py python vaccine.py --state NJ --cities princeton plainsboro
```

You will see output like this:

```
Tue Mar 30 12:43:37 2021
PLAINSBORO Fully Booked
PRINCETON Fully Booked
```

By default, the script will check for appointments every minute and run for a total of 3 hours after which it will exit. To change these values, you can use specify `--total` and `--refresh` options respectively. Run `python vaccine.py --help` for details.

This script is for monitoring the appointment website without clicking refresh 1 Billion times. It is not going to automatically book for you. And if you fork this and create an automated booking applet, I will personally send 1000 adolscent, chewing puppies to your house. And nobody wants that. Speaking of contributing...

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
[blog-shield]: https://img.shields.io/badge/medium-Read%20about%20this%20on%20Medium-lightgrey.svg?style=for-the-badge
[blog-url]: https://python.plainenglish.io/how-i-built-a-cvs-vaccine-appointment-availability-checker-in-python-6beb379549e4
