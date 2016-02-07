"""Pridobi podatke o trenutni temperaturi in vlagi na meteo.arso.gov.si in jih zapise v CSV datoteko"""

import requests
import re
from skripte import pripomocki


def pridobi_arso_podatke():
    pripomocki.logger.info("Pridobivam ARSO podatke.")
    data = requests.get("http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/"
                        "observationAms_PLANI-POD_history.html")

    pripomocki.logger.info("Urejam ARSO podatke.")
    data = data.text
    result = re.findall(r'<td class="meteoSI-th">.*,\s(\d\d\.\d\d\.\d\d\d\d\s\d+:00).*id="t">(-?\d+.?\d*)</td>.*'
                        r'id="rh">(\d+)</td>.*</td>', data)
    podatki = pripomocki.uredi_podatke(result)
    podatki.reverse()
    pripomocki.logger.info("ARSO podatki urejeni.")
    return podatki

if __name__ == "__main__":
    pripomocki.dodaj_v_csv(pridobi_arso_podatke(), "izmerjeni_podatki.csv", ["cas", "temperatura", "vlaznost"])
