import requests
import re
import time
import csv

def pridobi_arso_podatke():
    data = requests.get("http://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/"
                    "observationAms_PLANI-POD_history.html")
    data = data.text
    result = re.findall(r'<td class="meteoSI-th">\w*,\s(\d\d\.\d\d\.\d\d\d\d\s\d\d:\d\d).*id="t">(-?\d+.?\d*)</td>.*'
                    r'id="rh">(\d+)</td>.*</td>', data)
    podatki = uredi_podatke(result)
    podatki.reverse()
    return podatki


def uredi_podatke(podatki_iz_strani):
    urejeni_podatki = []
    for cas, temperatura, vlaznost in podatki_iz_strani:
        urejeni_podatki.append((cas, float(temperatura), int(vlaznost)))
    return urejeni_podatki


def pretvori_niz_v_cas(niz):
    return time.strptime(niz, "%d.%m.%Y %H:%M")


def pretvori_cas_v_niz(cas):
    return "{}.{}.{} {}:{}".format(cas.tm_mday, cas.tm_mon, cas.tm_year, cas.tm_hour, cas.tm_min)

def dodaj_v_csv(podatki):
    """Ustvari datoteko arso.csv, če ne obstaja in doda podatke, ki še niso v datoteki"""
    with open('arso.csv', 'a+') as csvdatoteka:
        csvdatoteka.seek(0)
        obstojeci_podatki = csv.reader(csvdatoteka)
        seznam_obstojecih_podatkov = []
        for podatek in obstojeci_podatki:
            seznam_obstojecih_podatkov.append(podatek)

        if seznam_obstojecih_podatkov != []:
            zadnji = uredi_podatke(seznam_obstojecih_podatkov)[-1]
            podatki = podatki[podatki.index(zadnji)+1:]

        vrste_podatkov = ['cas', 'temperatura', 'vlaznost']
        csv_pisi = csv.DictWriter(csvdatoteka, fieldnames=vrste_podatkov)
        for podatek in podatki:
            csv_pisi.writerow({'cas': podatek[0], 'temperatura': podatek[1], 'vlaznost': podatek[2]})

dodaj_v_csv(pridobi_arso_podatke())