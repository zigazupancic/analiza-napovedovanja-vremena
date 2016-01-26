import requests
import re
import time


def pridobi_arso_podatke():
    data = requests.get("http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/"
                    "observationAms_PLANI-POD_history.html")
    data = data.text
    result = re.findall(r'<td class="meteoSI-th">\w*,\s(\d\d\.\d\d\.\d\d\d\d\s\d\d:\d\d).*id="t">(-?\d+.?\d*)</td>.*'
                    r'id="rh">(\d+)</td>.*</td>', data)
    return result


def uredi_podatke(podatki_iz_strani):
    urejeni_podatki = []
    for cas, temperatura, vlaznost in podatki_iz_strani:
        urejeni_podatki.append((cas, float(temperatura), int(vlaznost)))
    return urejeni_podatki


def pretvori_niz_v_cas(niz):
    return time.strptime(niz, "%d.%m.%Y %H:%M")


def pretvori_cas_v_niz(cas):
    return "{}.{}.{} {}:{}".format(cas.tm_mday, cas.tm_mon, cas.tm_year, cas.tm_hour, cas.tm_min)
