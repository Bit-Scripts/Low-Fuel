import os
import sys
from geopy.geocoders import Nominatim
import wget
import json 

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from domain.user import *
from domain.data import *
from domain.logic import *

locator = Nominatim(user_agent="low-fuel")
list_of_prices = []


class ParseJson:
    def __init__(self, data_url: str, path: str, client_location: AddressUser):
        self.location = None
        self.station = None
        self.url: str = data_url
        self.filePath: str = path
        self.domicile: client_location
        self.coord_domicile = (client_location.latitude, client_location.longitude)
        self.radius = client_location.radius
        self.remove_old_source()  # func
        self.fuel_json = self.download_source()  # func
        self.latitudeStation = ""  # func
        self.longitudeStation = ""  # func
        self.station_list()  # func
        self.sell_points: List[SellPoint] = list()  # valeur retourné

    def remove_old_source(self):
        if os.path.exists(self.filePath):
            os.remove(self.filePath)

    def download_source(self):
        downloaded_file = open(wget.download(self.url, self.filePath))
        print('\n')
        json_file = json.load(downloaded_file)
        return json_file

    def station_list(self):
        self.sell_points: List[SellPoint] = []
        for first_data in range(0, self.fuel_json.__len__() - 1):
            self.latitudeStation = self.fuel_json[first_data]["fields"]["geom"][0]
            self.longitudeStation = self.fuel_json[first_data]["fields"]["geom"][1]
            self.station = (self.latitudeStation, self.longitudeStation)
            list_of_prices = []

            if near_stations(self.coord_domicile[0], self.coord_domicile[1], self.radius, self.fuel_json[first_data]["fields"]["id"], self.latitudeStation, self.longitudeStation):
                
                nom = coord_to_store_name(self.latitudeStation, self.longitudeStation)
                
                if nom is not None:
                    if type(nom) == int or type(nom) == float:
                        nom = 'Nom Station non trouvé'
                address = self.fuel_json[first_data]["fields"]["adresse"] + ' ' + self.fuel_json[first_data]["fields"]["cp"] + ' ' + self.fuel_json[first_data]["fields"]["com_name"]
                
                
                week_hours_args_1 = (self.fuel_json[first_data]["fields"]["horaires_automate_24_24"] == "Oui")
                week_hours_args_2: DayHours = []
                week_hours_args_weekday = []
                if "horaire" in list(self.fuel_json[first_data]["fields"].keys()):
                    week_hours_2 = self.fuel_json[first_data]["fields"]["horaires"]["jour"]["horaire"]
                    week_hours_args_weekday = []

                    for w_h_arg_2 in range(0, week_hours_2.__len__() - 1):
                        if week_hours_2[w_h_arg_2]["@ferme"] is not None:
                            week_hours_args_2.append(week_hours_2[w_h_arg_2]["@nom"], 
                                                        True, 
                                                        ["00:00", "00:00"])
                        else:
                            week_hours_args_2.append(week_hours_2[w_h_arg_2]["@nom"], 
                                                        False, 
                                                        [week_hours_2[w_h_arg_2]["@ouverture"], 
                                                        week_hours_2[w_h_arg_2]["@fermeture"],])
                else:                                        
                    week_hours_args_2 = "horaire non précisé"
                week_hours_args_weekday.append(week_hours_args_2)
                week_hours = WeekHours(week_hours_args_1, week_hours_args_weekday)
                if "prix_id" in list(self.fuel_json[first_data]["fields"].keys()):
                    price: Price = (self.fuel_json[first_data]["fields"]["prix_id"], 
                                    self.fuel_json[first_data]["fields"]["prix_nom"], 
                                    self.fuel_json[first_data]["fields"]["prix_maj"], 
                                    self.fuel_json[first_data]["fields"]["prix_valeur"])
                else:
                    price = "Pas de Carburant proposé"
                list_of_prices.append(price)
                ensemble_services = []
                if "services_service" in list(self.fuel_json[first_data]["fields"].keys()):
                    services = self.fuel_json[first_data]["fields"]["services_service"]
                    for service in services.split('//'):
                        ensemble_services.append(service)
                else:
                    ensemble_services.append("Pas de service particuliers proposé")               

                sell_point = SellPoint(self.fuel_json[first_data]["fields"]["id"], 
                                       nom, 
                                       address, 
                                       week_hours, 
                                       list_of_prices,
                                       ensemble_services)  # object to return
                print("Please wait... is loading")

                self.sell_points.append(sell_point)
        return self.sell_points