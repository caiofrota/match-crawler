# Web Soccer Match Crawler

## Overview
A web scraping tool that extracts soccer match schedules from [placardefutebol.com.br](https://www.placardefutebol.com.br/) and either create a .ics calendar file or sync with your google calendar.

## Google pre-configuration

1. Create Google Cloud Platform account.
2. Enable Google Calendar API on Google Cloud Platform.
   
    Please move to “APIs & Services” > “Dashboard”.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/a9ee137b-de31-4b65-937e-051b6b105580)
  
    Please move to “ENABLE APIS AND SERVICES”.
  
    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/9ae5e4bf-ba92-49b3-bec1-8a856a8a2337)

    Please type “Google Calendar API” in the search window and select “Google Calendar API”, and then enable Google Calendar API by clicking “ENABLE” button.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/cbd8840a-0970-44a7-9562-1803759674e4)

3. Create Service Account on Google Cloud Platform. Service Account is for non-human users.

    Please move to “APIs & Services” > “Service Accounts”.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/de658816-d35b-4fd6-80f0-7eb772dc6636)

    And then please click “CREATE SERVICE ACCOUNT”.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/6bb010e5-48a5-4f6d-b599-1729ab3986dc)

    Please input service account name and click “CREATE” button.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/18cdd819-a70a-42df-8eac-14c1fd3abc68)

    Other things are optional. So, I’ll skip inputting them because this time is just test. Please click “CONTINUE” and “DONE” buttons.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/04cb5f65-4f53-48cf-b5ec-d9b4ea0527ab)

4. Generate Service Account key.
   
    Please select “Actions” > “Manage keys” at Service Account page.
    
    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/64b46dae-3bb6-4014-bef2-c38494ca153f)

    Please click “ADD KEY” > “Create new key”.
    
    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/248211cd-fef8-43de-8e38-a4ab5a504283)

    Please click “CREATE” button with “JSON” key type. After that, you can see a dialog box for save and please save and keep your key. The key will be used by Python script.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/f4924f75-ced8-4f71-8222-435f9cf834bd)

5. Add Service Account to Google Calendar’s share member.

    Please copy Service Account email address.
    After that, Please open Google Calendar and move to “Settings and sharing”.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/b5e51854-aea2-45f4-bb67-80452a59023c)

    Please click “Add people” button at “Share with specific people”.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/ae90880c-824b-43da-87a4-50d6b3795f25)

    Please input your Service Account email address and click “Send” button.

    ![image](https://github.com/caiofrota/web-soccer-match-crawler/assets/9461960/5979eae3-dbc5-4e74-8636-00a124f90440)

## Installation

This example uses Python 3.10.12 and pip 22.0.2

1. Install required libs
   
    ```pip install bs4 lxml google-api-python-client google-auth```

2. Change the constants PRODID, CALNAME, CALDESC and TIMEZONE.

   SOURCE is the website you want to scrap (search for a team or a league in [placardefutebol.com.br](https://www.placardefutebol.com.br/)

   PRODID is the ics calendar id (free text)
   
   CALNAME is the ics calendar name (free text)

   CALDESC is the ics calendar description (free text)

   TIMEZONE is the time zone where you want to see in your calendar
      
3. Run:

   ```
   python3 crawler.py
   python3 crawler.py ics <website>
   python3 crawler.py gcalendar <website> <google-calendar-id>
   ```

4. Import the created ICS file in your web calendar!

### Support or contact
Contact me at caiofrota@gmail.com for questions and we'll help you sort it out.

### Issues
Find a bug or want to request a new feature? Please let us know by [submitting an issue](https://github.com/caiofrota/web-soccer-match-crawler/issues).

## Contributing
Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, please feel free to submit an issue or pull request.

Please read [CONTRIBUTING.md](https://gist.github.com/caiofrota/6e65a17fd3bf100d058cb48dcc780b21) for details on our code of conduct, and the process for submitting pull requests to us.

## License
Web Soccer Match Crawler is released under [MIT License](https://github.com/caiofrota/web-soccer-match-crawler/blob/main/LICENSE). Feel free to use, modify, and distribute the application as per the license terms.

## Disclaimer
This tool is intended for personal use. Users are responsible for adhering to the terms of service of the websites they scrape.
