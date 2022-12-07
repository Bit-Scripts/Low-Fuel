import os
import re
import xml.etree.ElementTree as ET
import zipfile
from colorama import Fore

import wget
from geopy.geocoders import Nominatim
from haversine import haversine
from prettytable import PrettyTable

tableau = PrettyTable()

locator = Nominatim(user_agent="low-fuel")
address = ""
coordonees = 0, 0
filePath = 'info.gouv/PrixCarburants_instantane'
zip_path = filePath + '.zip'
xml_path = filePath + '.xml'
url = 'https://donnees.roulez-eco.fr/opendata/instantane'
Matched_Cordinates = []
GazolePrix = '●●●●●●●'
SP95Prix = '●●●●●●●'
E85Prix = '●●●●●●●'
GPLcPrix = '●●●●●●●'
E10Prix = '●●●●●●●'
SP98Prix = '●●●●●●●'
carburant = ""

if os.path.exists(zip_path):
    os.remove(zip_path)

print(Fore.WHITE + '\nRécupération des données :\n')

filename = wget.download(url, zip_path)

if filename == zip_path:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall('info.gouv/')
        tree = ET.parse(xml_path)
        root = tree.getroot()

while locator.geocode(address) is None:
    print(Fore.WHITE + '\n\nEntrer votre adresse postale :')
    address = input(Fore.GREEN)
    if locator.geocode(address) is None:
        print(Fore.WHITE + '\nVotre adresse postale n\'a pas été trouvée')
    else:
        location = locator.geocode(address)
        print(Fore.WHITE + '-------------------------------------')
        print('Coordonnées de votre adresse')
        print((location[1]))
        print('-------------------------------------')


if coordonees is not None:
    coordonees = tuple(float(s) for s in location[1])

    print(Fore.WHITE + '\nrayon d\'action en km')
    radius_input = input(Fore.GREEN)
    if not radius_input.isalpha():
        radius_previous = re.findall(r"[-+]?(?:\d*\,\d+|\d+)", radius_input)
        if radius_previous:
            radius = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", radius_previous[0])[0].replace(',', '.'))
    else:
        radius = 0

while carburant != 'Gazole' and carburant != 'SP98' and carburant != 'SP95' and carburant != 'GPLc' and carburant != 'E10' and carburant != 'E85':
    print(Fore.WHITE + '\nQuel est votre Carburant')
    print(Fore.WHITE + '(Gazole, SP98, SP95, GPLc, E10 ou E85)')
    carburant = input(Fore.GREEN)

print(Fore.WHITE + '\nRecherche de station...')

for pdv in root.findall('pdv'):
    latitudeStation = float(pdv.get('latitude')) / 100000
    longitudeStation = float(pdv.get('longitude')) / 100000
    Station = latitudeStation, longitudeStation
    domicile = location[1]
    a = haversine(domicile, Station)
    if a <= radius:
        location = locator.geocode(str(latitudeStation) + "," + str(longitudeStation))
        nom = str(location).split(',')[0]
        if type(nom) == int or type(nom) == float:
            nom = ''
        else:
            nom = str(location).split(',')[0] + ' '
        Adresse = pdv.find('adresse').text + ' ' + pdv.get('cp') + ' ' + pdv.find('ville').text
        for prix in list(pdv.iter("prix")):
            if prix.get("nom") == 'Gazole':
                GazolePrix = prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'SP95':
                SP95Prix = prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'E85':
                E85Prix = prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'GPLc':
                GPLcPrix = prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'E10':
                E10Prix = prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'SP98':
                SP98Prix = prix.get("valeur").replace(".", ",") + " €"
        Matched_Cordinates.append(
            {'Nom': nom, 'Adresse': Adresse, 'Gazole': GazolePrix, 'SP95': SP95Prix, 'E85': E85Prix, 'GPLc': GPLcPrix,
             'E10': E10Prix, 'SP98': SP98Prix})
if Matched_Cordinates:
    minGazole = 99
    minSP95 = 99
    minE85 = 99
    minGPLc = 99
    minE10 = 99
    minSP98 = 99
    for line_Cordinates in Matched_Cordinates:
        if line_Cordinates["Gazole"] != '●●●●●●●':
            interGazole = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["Gazole"])[0].replace(',', '.'))
            if interGazole < float(minGazole):
                minGazole = interGazole
                minGazoleEuro = line_Cordinates["Gazole"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if line_Cordinates["SP95"] != '●●●●●●●':
            interSP95 = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["SP95"])[0].replace(',', '.'))
            if interSP95 < float(minSP95):
                minSP95 = interSP95
                minSP95Euro = line_Cordinates["SP95"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if line_Cordinates["E85"] != '●●●●●●●':
            interE85 = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["E85"])[0].replace(',', '.'))
            if interE85 < float(minE85):
                minE85 = interE85
                minE85Euro = line_Cordinates["E85"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if line_Cordinates["GPLc"] != '●●●●●●●':
            interGPLc = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["GPLc"])[0].replace(',', '.'))
            if interGPLc < float(minGPLc):
                minGPLc = interGPLc
                minGPLcEuro = line_Cordinates["GPLc"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if line_Cordinates["E10"] != '●●●●●●●':
            interE10 = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["E10"])[0].replace(',', '.'))
            if interE10 < float(minE10):
                minE10 = interE10
                minE10Euro = line_Cordinates["E10"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if line_Cordinates["SP98"] != '●●●●●●●':
            interSP98 = float(re.findall(r"[-+]?(?:\d*\,\d+|\d+)", line_Cordinates["SP98"])[0].replace(',', '.'))
            if interSP98 < float(minSP98):
                minSP98 = interSP98
                minSP98Euro = line_Cordinates["SP98"] + " | disponible à " + line_Cordinates["Nom"] + line_Cordinates["Adresse"]

        if minGazole == 99:
            minGazoleEuro = "Carburant non disponible"
        if minSP95 == 99:
            minSP95Euro = "Carburant non disponible"
        if minE85 == 99:
            minE85Euro = "Carburant non disponible"
        if minGPLc == 99:
            minGPLcEuro = "Carburant non disponible"
        if minE10 == 99:
            minE10Euro = "Carburant non disponible"
        if minSP98 == 99:
            minSP98Euro = "Carburant non disponible"

    print('\n')
    tableau.field_names = ["Nom", "Adresse", "Gazole", "SP95", "E85", "GPLc", "E10", "SP98"]
    for line_Cordinates in Matched_Cordinates:
        tableau.add_row(
            [line_Cordinates["Nom"], line_Cordinates["Adresse"], line_Cordinates["Gazole"], line_Cordinates["SP95"], line_Cordinates["E85"],
             line_Cordinates["GPLc"], line_Cordinates["E10"], line_Cordinates["SP98"]])
    print(tableau)
    
    print(Fore.GREEN)
    if carburant=='Gazole':
        print("\nGazole le moins cher : " + str(minGazoleEuro))
    if carburant=='SP95':    
        print("\nSP95 le moins cher : " + str(minSP95Euro))
    if carburant=='E85': 
        print("\nE85 le moins cher : " + str(minE85Euro))
    if carburant=='GPLc':
        print("\nGPLc le moins cher : " + str(minGPLcEuro))
    if carburant=='E10':
        print("\nE10 le moins cher : " + str(minE10Euro))
    if carburant=='SP98':
        print("\nSP98 le moins cher : " + str(minSP98Euro))
    print('\n')
else:
    print(Fore.GREEN + "\npas de station à proximité dans le rayon définit")
print(Fore.WHITE)
