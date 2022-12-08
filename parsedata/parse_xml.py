import os
import sys
import zipfile
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim
import wget
from haversine import haversine

# setting path

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from domain.user import *
from domain.data import *

locator = Nominatim(user_agent="low-fuel")


class ParseXml:
    def __init__(self, data_url: str, path: str, client_location: AddressUser):
        self.url : str = data_url
        self.filePath : str = path
        self.zip_path : str = self.filePath + '.zip'
        self.xml_path : str = self.filePath + '.xml'
        self.domicile : client_location
        self.coord_domicile = (client_location.latitude, client_location.longitude)
        self.radius = client_location.radius
        self.remove_old_source() #func
        self.filename = self.download_source() #func
        self.unzip_source() #func
        self.latitudeStation = "" #func 
        self.longitudeStation = "" #func
        self.station_list() #func


    def remove_old_source(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)


    def download_source(self):
        return wget.download(self.url, self.zip_path)


    def unzip_source(self):
        if self.filename == self.zip_path:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.filePath.split('/')[0] + '/')
                tree = ET.parse(self.xml_path)
                self.root = tree.getroot()


    def station_list(self):
        sell_points = [SellPoint]
        for pdv in self.root.findall('pdv'):
            self.latitudeStation = float(pdv.get('latitude')) / 100000
            self.longitudeStation = float(pdv.get('longitude')) / 100000
            self.station = (self.latitudeStation, self.longitudeStation)
            a = haversine(self.coord_domicile, self.station)
            if a <= self.radius:
                self.location = locator.geocode(str(self.latitudeStation) + ', ' + str(self.longitudeStation))
                nom = str(self.location).split(',')[0]
                if nom is not None:
                    if type(nom) == int or type(nom) == float:
                        nom = 'Nom Station non indiqué'
                Address = pdv.find('adresse').text + ' ' + pdv.get('cp') + ' ' + pdv.find('ville').text
                week_hours_args_1 = (pdv.find('automate-24-24') == "1")
                week_hours_args_2 : DayHours = []
                week_hours_2 = pdv.findall('jour')
                week_hours_args_weekday = []
                for week_hours_arg_2 in week_hours_2:
                    if week_hours_arg_2.get('ferme') == "1":
                        week_hours_args_2.append(week_hours_arg_2.get('nom'), week_hours_arg_2.get('ferme') == "1", ["00:00","00:00"])
                    else:
                        week_hours_args_2.append(week_hours_arg_2.get('nom'), week_hours_arg_2.get('ferme') == "1", [week_hours_arg_2.find('horaire').get('ouverture'),week_hours_arg_2.find('horaire').get('fermeture')])               
                    week_hours_args_weekday.append(week_hours_args_2)
                week_hours = WeekHours(week_hours_args_1, week_hours_args_weekday)
                prices = pdv.findall('prix')
                list_of_prices : List[Price] = []
                for price in prices:
                    list_of_prices.append((price.get('id'), price.get('nom'), price.get('maj'), price.get('valeur')))
                ensemble_services = []
                services = pdv.find('services').findall('service')
                for service in services:
                    ensemble_services.append(service.text)
                sell_point = SellPoint(pdv.get('id'), nom, Address, week_hours , list_of_prices, ensemble_services) # object to return
                print('\n')
                print(str(sell_point.id) + '\n' + sell_point.name + '\n' + sell_point.address + '\n' + str(sell_point.week_hours) + '\n' + str(sell_point.prices) + '\n' + str(sell_point.services))
                print('\n')
                sell_points.append(sell_point)
        return sell_points