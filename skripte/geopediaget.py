"""Pridobi podatke o napovedi temperature na vreme.geopedia.si in jih zapiše v CSV datoteko"""

import requests
import re
from skripte import pripomocki
import time


def pridobi_geopedia_podatke():
    pripomocki.logger.info("Pridobivam Geopedia podatke.")
    data = requests.get("http://vreme.geopedia.si/?locationId=15957")

    pripomocki.logger.info("Urejam Geopedia podatke.")
    data = data.text

    datum_danes = re.search(r'<h3>Danes \((.*)\)</h3>', data)
    datum_danes = time.strftime("%d.%m.%Y", time.strptime(datum_danes.group(1), "%d.%m.%Y"))
    datum_jutri = re.search(r'<h3>Jutri \((.*)\)</h3>', data)
    datum_jutri = time.strftime("%d.%m.%Y", time.strptime(datum_jutri.group(1), "%d.%m.%Y"))

    zacasni_podatki_danes = re.findall(r'<td>(\d\d:\d\d)</td>\s*\n\s*<td align="center"><img src=".*".*/></td>'
                               r'<td align="center"><b>(-?\d+.?\d*)</b>', data)
    zacasni_podatki_jutri = re.findall(r'<td>\s(\d\d:\d\d)</td>\s*\n\s*<td align="center"><img src=".*".*/></td>'
                               r'<td align="center"><b>(-?\d+.?\d*)</b>', data)
    podatki_danes = []
    for cas, temperatura in zacasni_podatki_danes:
        podatki_danes.append((datum_danes + " " + cas, temperatura))

    podatki_jutri = []
    for cas, temperatura in zacasni_podatki_jutri:
        podatki_jutri.append((datum_jutri + " " + cas, temperatura))

    podatki_danes = pripomocki.uredi_podatke(podatki_danes, False)
    podatki_jutri = pripomocki.uredi_podatke(podatki_jutri, False)

    pripomocki.logger.info("Geopedia podatki urejeni.")
    return [podatki_danes, podatki_jutri]
if __name__ == "__main__":
    danes, jutri = pridobi_geopedia_podatke()
    pripomocki.dodaj_v_csv(danes, "fmf_danes.csv", ["cas", "temperatura"])
    pripomocki.dodaj_v_csv(jutri, "fmf_jutri.csv", ["cas", "temperatura"])