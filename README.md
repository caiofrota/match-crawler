# Web Soccer Match Crawler

## Overview
A web scraping tool that extracts soccer match schedules from from [placardefutbol.com.br](https://www.placardefutebol.com.br/) and create a .ics calendar file.

## Installation

This example uses Python 3.10.12 and pip 22.0.2

1. Install required libs
   
    ```pip install bs4 lxml```

2. Change the constants PRODID, CALNAME, CALDESC and TIMEZONE.

   SOURCE is the website you want to scrap (search for a team or a league in [placardefutbol.com.br](https://www.placardefutebol.com.br/)

   PRODID is the ics calendar id (free text)
   
   CALNAME is the ics calendar name (free text)

   CALDESC is the ics calendar description (free text)

   TIMEZONE is the time zone where you want to see in your calendar
      
3. python3 crawler.py
4. Import the created ICS file in your web calendar!

## Contributing
Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to submit an issue or pull request.

## License
Web Soccer Match Crawler is released under MIT License. Feel free to use, modify, and distribute the application as per the license terms.

## Disclaimer
This tool is intended for personal use. Users are responsible for adhering to the terms of service of the websites they scrape.
