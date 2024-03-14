# Web Soccer Match Crawler

## Overview
A web scraping tool that extracts soccer match schedules from [placardefutebol.com.br](https://www.placardefutebol.com.br/) and either create a .ics calendar file or sync with your google calendar.

## Google pre-configuration

1. Create Google Cloud Platform account.
2. Enable Google Calendar API on Google Cloud Platform.
   
    Please move to “APIs & Services” > “Dashboard”.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/b61f1a03-ed4e-4fc3-b9ff-e8b22d1e9e63)
  
    Please move to “ENABLE APIS AND SERVICES”.
  
    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/bf08fbf3-a573-4f01-989e-ed93bf812857)

    Please type “Google Calendar API” in the search window and select “Google Calendar API”, and then enable Google Calendar API by clicking “ENABLE” button.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/c462c006-5c55-450f-9f2d-3c491a76f77e)


3. Create Service Account on Google Cloud Platform. Service Account is for non-human users.

    Please move to “APIs & Services” > “Service Accounts”.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/f0e28c6c-27a6-4ae8-9207-4c1cc6742339)

    And then please click “CREATE SERVICE ACCOUNT”.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/ad8f6f40-c0e9-456b-b49c-3ad59810c187)

    Please input service account name and click “CREATE” button.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/6afe705f-bb8e-4af3-ad95-2901acdc284a)
   
    Other things are optional. So, I’ll skip inputting them because this time is just test. Please click “CONTINUE” and “DONE” buttons.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/2eb02142-9f16-4808-b319-08fa21b2b809)

6. Generate Service Account key.
   
    Please select “Actions” > “Manage keys” at Service Account page.
    
    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/290ea921-3fe4-4eae-932d-3b89628c4829)
    
    Please click “ADD KEY” > “Create new key”.
    
    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/0579e9ec-5e55-42fc-a37f-ba4df64b6d03)

    Please click “CREATE” button with “JSON” key type. After that, you can see a dialog box for save and please save and keep your key. The key will be used by Python script.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/00d47657-c88c-42e6-902f-94d9d532e930)

7. Add Service Account to Google Calendar’s share member.

    Please copy Service Account email address.
    After that, Please open Google Calendar and move to “Settings and sharing”.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/cc49ee3a-fb8d-4c6a-8a16-0301aa25789a)

    Please click “Add people” button at “Share with specific people”.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/fe4e4d7d-2b31-461c-bb85-ac94eb6cf6f8)

    Please input your Service Account email address and click “Send” button.

    ![image](https://github.com/caiofrota/pdf-scraper/assets/9461960/da55d9ff-4129-4444-9289-40902b1a508e)

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
