import json
import requests
from skripte import pripomocki


def pridobi_wunderground_podatke():
    pripomocki.logger.info("Pridobivam Wunderground podatke.")
    data = requests.get("http://api.wunderground.com/api/0ed343f63bce1e0b/hourly10day/q/locid:SIXX1180;loctype:1.json")

    pripomocki.logger.info("Urejam Wunderground podatke.")
    data = data.text

    vsi_podatki = json.loads(data)
    napoved = vsi_podatki['hourly_forecast']
    koncni_podatki = []
    for podatek in napoved:
        cas = podatek['FCTTIME']
        datum = "{}.{}.{} {}:00".format(cas['mday_padded'], cas['mon_padded'], cas['year'], cas['hour'])

        koncni_podatki.append((datum, podatek['temp']['metric'], podatek['humidity']))
    koncni_podatki = pripomocki.uredi_podatke(koncni_podatki, True)
    koncni_podatki = razvrsti_po_dnevih(koncni_podatki)
    pripomocki.logger.info("Wunderground podatki urejeni.")
    return koncni_podatki


def razvrsti_po_dnevih(podatki):
    razvrsceni_podatki = []
    temp = []
    for podatek in podatki:
        if temp != []:
            if podatek[0][:10] == temp[-1][0][:10]:
                temp.append(podatek)
            else:
                razvrsceni_podatki.append(temp)
                temp = [podatek]
        else:
            temp.append(podatek)
    return razvrsceni_podatki

if __name__ == "__main__":
    for n, dan in enumerate(pridobi_wunderground_podatke()):
        pripomocki.dodaj_v_csv(dan, "wunder_dan_{}.csv".format(n), ["cas", "temperatura", "vlaznost"])
