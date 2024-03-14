from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import re
import requests
import sys

SOURCE = "https://www.placardefutebol.com.br/champions-league"
PRODID = "//Caio Frota//Match Crawler v1.0//EN"
CALNAME = "Match Crawler"
CALDESC = "Match Crawler"
TIMEZONE = "America/Fortaleza"

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = "credentials.json"

def convert_to_datetime(date_str, time_str, format):
  parsed_date = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
  return (parsed_date + timedelta(hours=3)).strftime(format)

def fetch(url):
  url = url
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "lxml")
  return soup

def get_calendar_service():
  credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
  service = build("calendar", "v3", credentials=credentials)
  return service

def parse(url):
  match = fetch(url)
  d = dict()
  
  d["league"] = match.find("h2", {"class": "match__league-name"}).getText() if match.find("h2", {"class": "match__league-name"}) else ""
  d["group"] = re.sub(r"\s+", " ", match.find("p", {"class": "match-group"}).getText().replace("\n", "").strip()) if match.find("p", {"class": "match-group"}) else ""
  d["home"] = match.find_all("h4", {"class": "team_link"})[0].getText()
  d["away"] = match.find_all("h4", {"class": "team_link"})[1].getText()
  
  details = match.find("div", {"class": "match-details"}).find_all("p")
  d["date"] = ""
  d["time"] = ""
  d["comments"] = ""
  d["location"] = ""
  for detail in details:
    if detail.find("img", title="Local da partida"): d["location"] = detail.getText()
    if detail.find("img", title="Transmissão"): d["comments"] = detail.getText()
    if detail.find("img", title="Data da partida"):
      datetime = detail.getText().split(" às ")
      d["date"] = datetime[0]
      d["time"] = datetime[1]
  
  return d

def ics(url):
  f = open("calendar.ics", "w")
  f.write("BEGIN:VCALENDAR\n")
  f.write("VERSION:2.0\n")
  f.write(f"PRODID:-{PRODID}\n")
  f.write("CALSCALE:GREGORIAN\n")
  f.write("METHOD:PUBLISH\n")
  f.write(f"X-WR-CALNAME:{CALNAME}\n")
  f.write(f"X-WR-TIMEZONE:{TIMEZONE}\n")
  f.write(f"X-WR-CALDESC:{CALDESC}\n")
  
  soup = fetch(url)
  matches = soup.find("div", {"id": "main"})
  if soup.find("div", {"id": "next_matches"}):
    matches = soup.find("div", {"id": "next_matches"})
  
  for match in matches.find_all("a"):
    try:
      if any(cls.startswith('match__') for cls in match['class']):
        details = parse(match["href"])
        
        start_date = convert_to_datetime(details['date'], details['time'], "%Y%m%dT%H%M00Z")
        end_date = (datetime.strptime(start_date, "%Y%m%dT%H%M00Z") + timedelta(hours=2)).strftime("%Y%m%dT%H%M00Z")
        
        f.write("BEGIN:VEVENT\n")
        f.write(f"DTSTART:{start_date}\n")
        f.write(f"DTEND:{end_date}\n")
        f.write(f"DTSTAMP:{start_date}\n")
        f.write(f"UID:{details['league']}|{details['group']}|{details['home']}|{details['away']}\n")
        f.write(f"CREATED:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}\n")
        f.write(f"DESCRIPTION:{details['league']} - {details['group']}<br/>{details['comments']}\n")
        f.write(f"LAST-MODIFIED:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}\n")
        f.write(f"SEQUENCE:0\n")
        f.write(f"STATUS:CONFIRMED\n")
        f.write(f"LOCATION:{details['location']}\n")
        f.write(f"SUMMARY:{details['home']} x {details['away']}\n")
        f.write(f"TRANSP:OPAQUE\n")
        f.write("END:VEVENT\n")
        
        print(f"{details['league']} | {details['group']} | {details['home']} x {details['away']} - {details['date']} às {details['time']} | {details['comments']}")
    except Exception as e: print(e)
    
  f.write("END:VCALENDAR")
  f.close()

def gcalendar(url, calId):
  service = get_calendar_service()
  
  soup = fetch(url)
  matches = soup.find("div", {"id": "main"})
  if soup.find("div", {"id": "next_matches"}):
    matches = soup.find("div", {"id": "next_matches"})
  
  for match in matches.find_all("a"):
    try:
      if any(cls.startswith('match__') for cls in match['class']):
        details = parse(match["href"])
        
        start_date = convert_to_datetime(details['date'], details['time'], "%Y-%m-%dT%H:%M:00Z")
        end_date = (datetime.strptime(start_date, "%Y-%m-%dT%H:%M:00Z") + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:00Z")
        
        id = f"{details['league']}|{details['group']}|{details['home']}|{details['away']}"
        found = service.events().list(calendarId=calId, iCalUID=id, showDeleted=True).execute().get("items")
        
        if found:
          service.events().update(
            calendarId=calId,
            eventId=found[0]["id"],
            body={
              "summary": f"{details['home']} x {details['away']}",
              "description": f"{details['league']} - {details['group']}<br/>{details['comments']}",
              "start": {"dateTime": f"{start_date}", "timeZone": TIMEZONE},
              "end": {"dateTime": f"{end_date}", "timeZone": TIMEZONE},
              "location": details['location']
            }
          ).execute()
          print(f"{details['league']} | {details['group']} | {details['home']} x {details['away']} - {details['date']} às {details['time']} | {details['comments']}", "updated")
        else:
          service.events().insert(calendarId=calId,
            body={
              "summary": f"{details['home']} x {details['away']}",
              "description": f"{details['league']} - {details['group']}<br/>{details['comments']}",
              "start": {"dateTime": f"{start_date}", "timeZone": TIMEZONE},
              "end": {"dateTime": f"{end_date}", "timeZone": TIMEZONE},
              "location": details['location'],
              "iCalUID": id
            }
          ).execute()
          print(f"{details['league']} | {details['group']} | {details['home']} x {details['away']} - {details['date']} às {details['time']} | {details['comments']}", "created")
    
    except Exception as e: print(e)

def pre_ics():
  url = sys.argv[2] if len(sys.argv) > 2 else input("Crawler URL (eg. https://www.placardefutebol.com.br/champions-league): ")
  if (url):
    ics(url)
  else: print("Invalid URL")

def pre_gcalendar():
  url = sys.argv[2] if len(sys.argv) > 2 else input("Crawler URL (eg. https://www.placardefutebol.com.br/champions-league): ")
  if (url):
    calId = sys.argv[3] if len(sys.argv) > 3 else input(f"Google Calendar Id: ")
    if (calId):
      gcalendar(url, calId)
    else: print("Invalid Calendar Id")
  else: print("Invalid URL")

def main():
  if len(sys.argv) > 1:
    if sys.argv[1] == "ics":
      option = "1"
    elif sys.argv[1] == "gcalendar":
      option = "2"
    else:
      option = "3"
  else: 
    print("[1] - Create ICS file")
    print("[2] - Sync Google Calendar")
    print("[3] - Exit")
    option = input("Choose an option: ")
  
  if option == "1":
    pre_ics()
  elif option == "2":
    pre_gcalendar()
  elif option == "3":
    None
  else:
    print("invalid option")
    main()
  
main()
