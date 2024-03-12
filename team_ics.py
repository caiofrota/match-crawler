from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

SOURCE = "https://www.placardefutebol.com.br/time/ceara/proximos-jogos"
PRODID = "//Caio Frota//Jogos do Ceará v1.0//EN"
CALNAME = "Jogos do Ceará"
CALDESC = "Jogos do Ceará"
TIMEZONE = "America/Fortaleza"

def fetch_matches():
    url = SOURCE
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def convert_to_datetime(date_str, time_str):
  # Parse date string
  date_format = "%d/%m"
  parsed_date = datetime.strptime(date_str, date_format)

  # Parse time string
  time_format = "%H:%M"
  parsed_time = datetime.strptime(time_str, time_format).time()

  # Get current date for reference
  current_date = datetime.now()

  # Determine the nearest future date for the provided month and day
  future_date = datetime(current_date.year, parsed_date.month, parsed_date.day)
  if future_date < current_date:
    future_date = datetime(current_date.year + 1, parsed_date.month, parsed_date.day)

  # Combine the future date and parsed time
  result_datetime = datetime.combine(future_date.date(), parsed_time)

  # Format the result as a string
  result_str = (result_datetime + timedelta(hours=3)).strftime("%Y%m%dT%H%M00Z")

  return result_str

def main():
  f = open("calendar.ics", "w")
  f.write("BEGIN:VCALENDAR\n")
  f.write("VERSION:2.0\n")
  f.write(f"PRODID:-{PRODID}\n")
  f.write("CALSCALE:GREGORIAN\n")
  f.write("METHOD:PUBLISH\n")
  f.write(f"X-WR-CALNAME:{CALNAME}\n")
  f.write(f"X-WR-TIMEZONE:{TIMEZONE}\n")
  f.write(f"X-WR-CALDESC:{CALDESC}\n")
  
  soup = fetch_matches()
  matches = soup.find_all("a", {"class": "match__lg"})
  for match in matches:
    league = match.find("div", {"class": "match__lg_card--league"}).string
    home_team = match.find("div", {"class": "match__lg_card--ht-name"}).string
    away_team = match.find("div", {"class": "match__lg_card--at-name"}).string
    date = match.find("div", {"class": "match__lg_card--datetime"}).get_text().replace(" ", "").strip().split("\n")[0].split(",")[1]
    time = match.find("div", {"class": "match__lg_card--datetime"}).get_text().replace(" ", "").strip().split("\n")[1]
    start_date = convert_to_datetime(date, time)
    end_date = (datetime.strptime(start_date, "%Y%m%dT%H%M00Z") + timedelta(hours=2)).strftime("%Y%m%dT%H%M00Z")
    
    f.write("BEGIN:VEVENT\n")
    f.write(f"DTSTART:{start_date}\n")
    f.write(f"DTEND:{end_date}\n")
    f.write(f"DTSTAMP:{start_date}\n")
    f.write(f"UID:cf2024:{league}{home_team}x{away_team}\n")
    f.write(f"CREATED:{start_date}\n")
    f.write(f"DESCRIPTION:{home_team} x {away_team}\n")
    f.write(f"LAST-MODIFIED:{start_date}\n")
    f.write(f"SEQUENCE:0\n")
    f.write(f"STATUS:CONFIRMED\n")
    f.write(f"LOCATION:{league}\n")
    f.write(f"SUMMARY:{home_team} x {away_team}\n")
    f.write(f"TRANSP:OPAQUE\n")
    f.write("END:VEVENT\n")
    
  f.write("END:VCALENDAR")
  f.close()
    
main()
