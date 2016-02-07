"""Pridobi podatke o napovedi temperature in vlage na accuweather.com in jih zapise v CSV datoteko"""

import requests
import re
from skripte import pripomocki
import time
import datetime


def pridobi_accuweather_podatke(dan):
    pripomocki.logger.info("Pridobivam AccuWeather podatke.")
    data = requests.get("http://m.accuweather.com/en/si/planina-pod-golico/1562618/"
                        "hourly-weather-forecast/299198?ptab=o&day={}".format(dan))

    pripomocki.logger.info("Urejam AccuWeather podatke.")
    data = data.text

    meseci = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
              'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    datum = re.search(r'<h2 class="grey">\w{3} (\w{3}) (\d+)</h2>', data)
    datum = "{}.{}.{}".format(datum.group(2), meseci[datum.group(1)], datetime.datetime.now().year)
    datum = time.strftime("%d.%m.%Y", time.strptime(datum, "%d.%m.%Y"))

    zacasni_podatki = re.findall(r'<div name="hour_(\d\d)" class="wx-cell">\s*\n.*\n.*\n.*\n.*\n.*\n\s*<td class="temp"'
                                 r'>(-?\d+.?\d*)&.*(\n.*){13}\n\s*<p>Humidity <b>(\d+).*</b></p>', data)

    podatki = []
    for cas, temperatura, _, vlaga in zacasni_podatki:
        cas = "{}:00".format(int(cas))
        podatki.append((datum + " {}".format(cas), temperatura, vlaga))

    podatki = pripomocki.uredi_podatke(podatki, True)

    pripomocki.logger.info("AccuWeather podatki urejeni.")
    return podatki

if __name__ == "__main__":
    for n in range(1, 5):
        pripomocki.dodaj_v_csv(pridobi_accuweather_podatke(n), "accu_dan_{}.csv".format(n),
                               ["cas", "temperatura", "vlaznost"])
