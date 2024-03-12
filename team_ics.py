from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import re

SOURCE = "https://www.placardefutebol.com.br/champions-league"
PRODID = "//Caio Frota//Match Crawler v1.0//EN"
CALNAME = "Match Crawler"
CALDESC = "Match Crawler"
TIMEZONE = "America/Fortaleza"


def convert_to_datetime(date_str, time_str):
  parsed_date = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
  return (parsed_date + timedelta(hours=3)).strftime("%Y%m%dT%H%M00Z")

def fetch(url):
  url = url
  r = requests.get(url)
  soup = BeautifulSoup(r.text, "lxml")
  return soup

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

def ics():
  f = open("calendar.ics", "w")
  f.write("BEGIN:VCALENDAR\n")
  f.write("VERSION:2.0\n")
  f.write(f"PRODID:-{PRODID}\n")
  f.write("CALSCALE:GREGORIAN\n")
  f.write("METHOD:PUBLISH\n")
  f.write(f"X-WR-CALNAME:{CALNAME}\n")
  f.write(f"X-WR-TIMEZONE:{TIMEZONE}\n")
  f.write(f"X-WR-CALDESC:{CALDESC}\n")
  
  soup = fetch(SOURCE)
  matches = soup.find("div", {"id": "main"})
  if soup.find("div", {"id": "next_matches"}):
    matches = soup.find("div", {"id": "next_matches"})
  
  for match in matches.find_all("a"):
    try:
      if any(cls.startswith('match__') for cls in match['class']):
        details = parse(match["href"])
        
        start_date = convert_to_datetime(details['date'], details['time'])
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

def main():
  ics()
  
main()
