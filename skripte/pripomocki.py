import csv
import logging
import os

# ---------------------------------------------
# LOGGER
logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)

# Ustvari pomočnika za pisanje log-a v datoteko.

fh = logging.FileHandler('../log.txt')
fh.setLevel(logging.DEBUG)

# Ustvari pomočniga za pisanje log-a v konzolo.

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Format log-a in ostale nastavitve.

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)
# ---------------------------------------------


def uredi_podatke(podatki_iz_strani, vlaznost=True):
    urejeni_podatki = []
    if vlaznost:
        for cas, temperatura, vlaznost in podatki_iz_strani:
            urejeni_podatki.append((cas, float(temperatura), int(vlaznost)))
    else:
        for cas, temperatura in podatki_iz_strani:
            urejeni_podatki.append((cas, float(temperatura)))
    return urejeni_podatki


def dodaj_v_csv(podatki, ime_datoteke, vrste_podatkov):
    datoteka = os.path.join("../csv", ime_datoteke)
    logger.info("Zapisujem podatke v {}.".format(datoteka))
    with open(datoteka, 'a+') as csvdatoteka:
        csvdatoteka.seek(0)
        obstojeci_podatki = csv.reader(csvdatoteka)
        seznam_obstojecih_podatkov = []
        for podatek in obstojeci_podatki:
            seznam_obstojecih_podatkov.append(podatek)

        if len(seznam_obstojecih_podatkov) > 1:
            logger.info("CSV ni prazen, dodajam.")
            if len(vrste_podatkov) == 2:
                vlaznost = False
            else:
                vlaznost = True
            zadnji = uredi_podatke(seznam_obstojecih_podatkov[1:], vlaznost)[-1]
            try:
                podatki = podatki[podatki.index(zadnji)+1:]
            except ValueError:
                logger.info("Manjkajo vmesni podatki v {}.".format(datoteka))
                pass

        csv_pisi = csv.DictWriter(csvdatoteka, fieldnames=vrste_podatkov)
        if seznam_obstojecih_podatkov == []:
            csv_pisi.writeheader()
        stevec = 0
        if len(vrste_podatkov) == 3:
            for podatek in podatki:
                stevec += 1
                csv_pisi.writerow({'cas': podatek[0], 'temperatura': podatek[1], 'vlaznost': podatek[2]})
        else:
            for podatek in podatki:
                stevec += 1
                csv_pisi.writerow({'cas': podatek[0], 'temperatura': podatek[1]})

    logger.info("Podatki [{}] uspešno zapisani v {}.".format(stevec, datoteka))
