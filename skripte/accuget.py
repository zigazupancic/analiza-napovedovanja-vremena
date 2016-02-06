"""Pridobi podatke o napovedi temperature in vlage na accuweather.com in jih zapiše v CSV datoteko"""

import requests
import re
from skripte import pripomocki
import time
import datetime


def pridobi_accuweather_podatke(dan):
    pripomocki.logger.info("Pridobivam AccuWeather podatke.")
    data = requests.get("http://m.accuweather.com/sl/si/planina-pod-golico/1562618/"
                        "hourly-weather-forecast/299198?day={}".format(dan))

    pripomocki.logger.info("Urejam AccuWeather podatke.")
    data = data.text

    # TODO: Uredi datum in iskanje datuma
    datum = re.search(r'<li class="date-span-label">... (\d.\d)</li>', data)
    datum = datum.group(1) + ".{}".format(datetime.datetime.now().year)
    datum = time.strftime("%d.%m.%Y", time.strptime(datum, "%d.%m.%Y"))

    # TODO: Uredi regularni izraz, da najde čas, temperaturo in vlago
    zacasni_podatki = re.findall(r'<li id="hour(\d*)"(.*\n){5}\s*<strong>(-?\d+.?\d*)&#176;</strong>(.*\n){16}\s*<li><b>.*</b> (\d+)%</li>', data)

    # TODO: Uredi zacasne podatke
    podatki = []
    for cas, temperatura, vlaga in zacasni_podatki:
        podatki.append((datum + " " + cas, temperatura, vlaga))

    podatki = pripomocki.uredi_podatke(podatki, True)

    pripomocki.logger.info("AccuWeather podatki urejeni.")
    return podatki

if __name__ == "__main__":
    # TODO: Dodaj dneve od 1 do 5 v CSV datoteko
    pridobi_accuweather_podatke(1)
    pripomocki.dodaj_v_csv(danes, "accu_dan_{}.csv".format(dan), ["cas", "temperatura", "vlaga"])