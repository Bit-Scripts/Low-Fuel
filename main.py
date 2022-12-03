import wget
from datetime import datetime,timedelta
import zipfile
import os
import xml.etree.ElementTree as ET
from haversine import haversine, Unit
from geopy.geocoders import Nominatim
from prettytable import PrettyTable
tableau = PrettyTable()

filePath = 'info.gouv/PrixCarburants_instantane.zip'

if os.path.exists(filePath):
    os.remove(filePath)

url = 'https://donnees.roulez-eco.fr/opendata/instantane'

filename = wget.download(url, 'info.gouv/PrixCarburants_instantane.zip')

if (filename == 'info.gouv/PrixCarburants_instantane.zip'):
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('info.gouv/')
        tree = ET.parse('info.gouv/PrixCarburants_instantane.xml')
        root = tree.getroot()
        print (root)

locator = Nominatim(user_agent="low-fuel")

print('Entrer votre adresse postale :')
adresse=input()

location = locator.geocode(adresse)

print('Coordonnées de votre adresse')
print((location.latitude, location.longitude))

Matched_Cordinates=[]

print('rayon d\'action en km')
radius = float(input()) # in km

for pdv in root.findall('pdv'):
    latitudeStation = float(pdv.get('latitude')) / 100000
    longitudeStation = float(pdv.get('longitude')) / 100000
    Station = latitudeStation,longitudeStation
    domicile = location.latitude,location.longitude
    a = haversine(domicile, Station)
    if a <= radius:
        Adresse = pdv.find('adresse').text + ' ' + pdv.get('cp') + ' ' + pdv.find('ville').text
        GazolePrix='●●●●●●●'
        SP95Prix='●●●●●●●'
        E85Prix='●●●●●●●'
        GPLcPrix='●●●●●●●'
        E10Prix='●●●●●●●'
        SP98Prix='●●●●●●●'
        for prix in list(pdv.iter("prix")):
            if prix.get("nom") == 'Gazole':
                GazolePrix=prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'SP95':
                SP95Prix=prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'E85':
                E85Prix=prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'GPLc':
                GPLcPrix=prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'E10':
                E10Prix=prix.get("valeur").replace(".", ",") + " €"
            if prix.get("nom") == 'SP98':
                SP98Prix=prix.get("valeur").replace(".", ",") + " €"
        Matched_Cordinates.append({'Adresse':Adresse, 'Gazole':GazolePrix,'SP95':SP95Prix,'E85':E85Prix,'GPLc':GPLcPrix,'E10':E10Prix,'SP98':SP98Prix})

tableau.field_names = ["Adresse", "Gazole", "SP95", "E85", "GPLc", "E10", "SP98"]

for line_Cordinates in Matched_Cordinates:
    tableau.add_row([line_Cordinates["Adresse"], line_Cordinates["Gazole"], line_Cordinates["SP95"], line_Cordinates["E85"], line_Cordinates["GPLc"], line_Cordinates["E10"], line_Cordinates["SP98"]])

print(tableau)