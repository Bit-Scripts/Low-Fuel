import os
import zipfile
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim
import wget
from domain import data, logic, user


class ObtainXml:
    def __init__(self):
        self.locator = Nominatim(user_agent="low-fuel")
        self.nom = None
        self.domicile = self.client_location
        self.Station = None
        self.longitudeStation = None
        self.latitudeStation = None
        self.root = None
        self.filePath = 'info.gouv/PrixCarburants_instantane'
        self.zip_path = self.filePath + '.zip'
        self.xml_path = self.filePath + '.xml'
        self.url = 'https://donnees.roulez-eco.fr/opendata/instantane'
        self.remove_old_source()
        self.filename = self.download_source()

    def remove_old_source(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)

    def download_source(self):
        return wget.download(self.url, self.zip_path)

    def unzip_source(self):
        if self.filename == self.zip_path:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall('info.gouv/')
                tree = ET.parse(self.xml_path)
                self.root = tree.getroot()

    def station_list(self):
        for pdv in self.root.findall('pdv'):
            self.latitudeStation = float(pdv.get('latitude')) / 100000
            self.longitudeStation = float(pdv.get('longitude')) / 100000

            self.locator = self.locator.geocode(self.latitudeStation + "," + self.longitudeStation)
            self.nom = str(self.location).split(',')[0]
            if type(int(self.nom)) == int or type(float(self.nom)) == float:
                print('Nom non indiqué')
            else:
                print(str(self.location).split(',')[0])
