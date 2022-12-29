import os
import sys
import tempfile
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
        self.sell_points: List[SellPoint] = list()  # valeur retourné
        self.low_price_name: str = ""
        self.high_price_name: str = ""

    def remove_old_source(self):
        pass
        #with os.scandir(self.filePath) as entries:
        #    for entry in entries:
        #        file = str(entry)
        #        if file.endswith('*.json'):
        #            os.remove(entry)
        
        

    def download_source(self):
        downloaded_file = open(wget.download(self.url, out=(self.filePath + '/essence.json')))
        json_file = json.load(downloaded_file)
        return json_file

    def station_list(self):
        low_price: float = 99.9
        high_price: float = 0.0
        price: Price = ()
        list_of_prices: List[Price] = []
        self.sell_points: List[SellPoint] = []
        for first_data in range(0, self.fuel_json.__len__()):
            self.latitudeStation = self.fuel_json[first_data]["fields"]["geom"][0]
            self.longitudeStation = self.fuel_json[first_data]["fields"]["geom"][1]
            self.station = (self.latitudeStation, self.longitudeStation)
              
            nom = coord_to_store_name(self.latitudeStation, self.longitudeStation)
            
            if nom is not None:
                if type(nom) == int or type(nom) == float:
                    nom = 'Nom Station non trouvé'
            address:Address = (self.fuel_json[first_data]["fields"]["adresse"], self.fuel_json[first_data]["fields"]["cp"], self.fuel_json[first_data]["fields"]["com_name"], self.latitudeStation, self.longitudeStation)
            
            
            week_hours_args_1 = (self.fuel_json[first_data]["fields"]["horaires_automate_24_24"] == "Oui")
            week_hours_args_2: DayHours = []
            week_hours_args_weekday: List[DayHours] = []

            if "horaires" in list(self.fuel_json[first_data]["fields"].keys()):
                partial_json = self.fuel_json[first_data]["fields"]["horaires"].replace("\\", "")
                partial_json_dumps = str(json.dumps(partial_json)[1:][:-1].replace("\\", ""))
                fuel_json_loads = json.loads(partial_json_dumps)
                if "jour" in list(fuel_json_loads.keys()):
                    week_hours_2 = fuel_json_loads["jour"]
                    week_hours_args_weekday: List[DayHours] = []

                    for w_h_arg_2 in range(0, week_hours_2.__len__()):
                        week_hours_json = week_hours_2[w_h_arg_2]
                        week_hours_json_dumps = str(json.dumps(week_hours_json))
                        week_hours_json_loads = json.loads(week_hours_json_dumps)
                        if "horaire" in list(week_hours_json_loads.keys()):
                            closed: DayHours.closed = False
                            if "@ouverture" in week_hours_json_loads["horaire"]:
                                closed: False
                                opening: Hour.opening = week_hours_json_loads["horaire"]["@ouverture"]
                                closing: Hour.closing = week_hours_json_loads["horaire"]["@fermeture"]
                            else:
                                horaire = week_hours_json_loads["horaire"]
                                closed: False
                                opening = (horaire[0]["@ouverture"], horaire[0]["@fermeture"]) 
                                closing = (horaire[1]["@ouverture"], horaire[1]["@fermeture"])
                        elif "@ferme" in list(week_hours_json_loads.keys()):
                            closed: DayHours.closed = True
                            opening: Hour.opening = "00:00"
                            closing: Hour.opening = "00:00"
                        day: WeekDay = week_hours_json_loads["@nom"]
                        week_hours_args_2.append((day, 
                                                closed, 
                                                [opening, 
                                                closing]))                     
            else:                                        
                day: WeekDay = "horaire non précisé"
                closed: DayHours.closed = True
                opening: Hour.opening = "00:00"
                closing: Hour.opening = "00:00"
                week_hours_args_2.append((day, 
                                            closed, 
                                            [opening, 
                                            closing]))
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
            if self.fuel_json[first_data]["fields"]["prix_valeur"] < low_price:
                self.low_price_name = nom
                low_price = self.fuel_json[first_data]["fields"]["prix_valeur"]
            if self.fuel_json[first_data]["fields"]["prix_valeur"] > high_price:
                self.high_price_name = nom
            ensemble_services = []
            if "services_service" in list(self.fuel_json[first_data]["fields"].keys()):
                services = self.fuel_json[first_data]["fields"]["services_service"]
                for service in services.split('//'):
                    ensemble_services.append(service)
            else:
                ensemble_services.append("Pas de service particuliers proposé")               
            distance = distance_between(self.coord_domicile[0], self.coord_domicile[1], self.latitudeStation, self.longitudeStation)
            
            sell_point = SellPoint(self.fuel_json[first_data]["fields"]["id"], 
                                        nom, 
                                        address, 
                                        week_hours, 
                                        list_of_prices,
                                        ensemble_services, 
                                        distance)
            self.sell_points.append(sell_point)
            list_of_prices = []
        return self.sell_points
    
    def get_low_price_name(self):
        return self.low_price_name
    
    def get_high_price_name(self):
        return self.high_price_name