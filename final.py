import csv
import requests
from bs4 import BeautifulSoup

response = requests.get("https://iot.cpe.ku.ac.th/daq/task2/data/39")
soup = BeautifulSoup(response.text, "html.parser")

name_values = [s.text for s in soup.select("td:nth-of-type(2)")]
country_values = [s.text for s in soup.select("td:nth-of-type(3)")]
sport_values = [s.text for s in soup.select("td:nth-of-type(1)")]
gold_values = [s.text for s in soup.select("td:nth-of-type(4)")]
silver_values = [s.text for s in soup.select("td:nth-of-type(5)")]
bronze_values = [s.text for s in soup.select("td:nth-of-type(6)")]

head = ["athlete's name", "country", "sport", "gold", "silver", "bronze"]
rows = []

for name, country, sport, gold, silver, bronze in zip(
        name_values, country_values, sport_values, gold_values, silver_values,
        bronze_values):
    rows.append([name, country, sport, gold, silver, bronze])

with open('athlete.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(head)
    write.writerows(rows)