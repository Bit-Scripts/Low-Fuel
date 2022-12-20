import os
import sys
import uuid
import pgeocode
from kivy.resources import resource_add_path, resource_find

from domain.data import SellPoint
from domain.logic import address_to_coord, colorHtmlToKivy
from domain.user import AddressUser
from parsedata.parse_json import ParseJson

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from typing import List

from geopy import Nominatim

import random

import kivy
from kivy.app import App
from kivy.config import Config
from kivy_garden.mapview import MapView
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.resources import resource_add_path, resource_find

from my_kivy.create_uix import kivyUi
from my_kivy.coloredlabel import ColoredLabel
from domain.logic import colorHtmlToKivy
from kivy.config import Config
from kivy.app import App

class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)

        # random position
        Nord  = 51.08916667 
        Sud   = 42.33277778
        Est   =  8.23055556
        Ouest = -4.79555556
        random_latitude = random.uniform(Sud, Nord)
        random_longitude = random.uniform(Ouest, Est)
        
        # let's add a Widget to this layout
        self.mapview = MapView(lat=random_latitude, lon=random_longitude, zoom=12, map_source="osm", size_hint=(1, 1))
        self.add_widget(self.mapview)
        self.street_label = ColoredLabel(text="    Numéro et\nNom de la Rue", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.249,.098), pos_hint={'x': 0, 'y': .9})
        self.street_entry = TextInput(size_hint=(.249,.05), pos_hint={'x': 0, 'y': .85})
        self.street_entry.bind(text=self.on_text)

        self.post_code_label = ColoredLabel(text=" Code\nPostal", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.082333333333,.098), pos_hint={'x': .25, 'y': .9})
        self.post_code_entry = TextInput(size_hint=(.082333333333,.05), pos_hint={'x': .25, 'y': .85})
        self.post_code_entry.bind(text=self.on_text_)

        self.city_label = ColoredLabel(text="Ville", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.16566667,.098), pos_hint={'x': .33333333, 'y': .9})
        self.city_entry = TextInput(size_hint=(.16566667,.05), pos_hint={'x': .33333333, 'y': .85})
        self.city_entry.bind(text=self.on_text)

        self.radius_label = ColoredLabel(text="     Rayon\nd'action(km)", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.165666667,.098), pos_hint={'x': .5, 'y': .9})
        self.radius_entry = TextInput(size_hint=(.16566667,.05), pos_hint={'x': .5, 'y': .85})
        self.radius_entry.bind(text=self.on_text)

        self.addresse_label = ColoredLabel(text="Adresse Non trouvé", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
        self.essence_label = ColoredLabel(text="Type d'essence non correct", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})

        self.fuel_DropDown = DropDown()
        self.btn_Gazole = Button(text='Gazole', size_hint_y=None, height=44)
        self.btn_Gazole.bind(on_release=lambda btn_Gazole: self.fuel_DropDown.select(self.btn_Gazole.text))
        self.btn_SP95 = Button(text='SP95', size_hint_y=None, height=44)
        self.btn_SP95.bind(on_release=lambda btn_SP95: self.fuel_DropDown.select(self.btn_SP95.text))
        self.btn_SP98 = Button(text='SP98', size_hint_y=None, height=44)
        self.btn_SP98.bind(on_release=lambda btn_SP98: self.fuel_DropDown.select(self.btn_SP98.text))
        self.btn_E85 = Button(text='E85', size_hint_y=None, height=44)
        self.btn_E85.bind(on_release=lambda btn_E85: self.fuel_DropDown.select(self.btn_E85.text))
        self.btn_E10 = Button(text='E10', size_hint_y=None, height=44)
        self.btn_E10.bind(on_release=lambda btn_E10: self.fuel_DropDown.select(self.btn_E10.text))
        self.btn_GPLc = Button(text='GPLc', size_hint_y=None, height=44)
        self.btn_GPLc.bind(on_release=lambda btn_GPLc: self.fuel_DropDown.select(self.btn_GPLc.text))
        self.button_DropDown = Button(text="Carburant utilisé", size_hint=(.16666667, .15), pos_hint={'x': .66666667, 'y': .85})
        self.button_DropDown.bind(on_release=self.fuel_DropDown.open)
        self.fuel_DropDown.bind(on_select=lambda instance, x: setattr(self.button_DropDown, 'text', x))

        self.submitButton = Button(text="Mettre à jour", size_hint=(.16666667, .15), pos_hint={'x': .833333333, 'y': .85}) 
        self.submitButton.bind(on_press=lambda instance: self.updateMapView(self.street_entry.text, self.post_code_entry.text, self.city_entry.text, self.radius_entry.text, self.button_DropDown.text, self.addresse_label, self.essence_label))
        self.download_data_label = ColoredLabel(text="Récupération des données", color=(1,1,1,1), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
        self.loading_label = ColoredLabel(text="Traitement des données", color=(1,1,1,1), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
        

        self.add_widget(self.submitButton)
        self.fuel_DropDown.add_widget(self.btn_Gazole)
        self.fuel_DropDown.add_widget(self.btn_SP98)
        self.fuel_DropDown.add_widget(self.btn_SP95)
        self.fuel_DropDown.add_widget(self.btn_E85)
        self.fuel_DropDown.add_widget(self.btn_E10)
        self.fuel_DropDown.add_widget(self.btn_GPLc)
        self.add_widget(self.button_DropDown)
        self.add_widget(self.street_label)
        self.add_widget(self.street_entry)
        self.add_widget(self.post_code_label)
        self.add_widget(self.post_code_entry)
        self.add_widget(self.city_label)
        self.add_widget(self.city_entry)
        self.add_widget(self.radius_label)
        self.add_widget(self.radius_entry)
        self.locator = Nominatim(user_agent="low-fuel")
        
    def on_text(self, instance, value):
        pass

    def on_text_(self, instance, value):
        if value != '' and len(value) == 5 and str(int(value)) == value:
            nomi = pgeocode.Nominatim('fr')
            city = nomi.query_postal_code(value)
            city = city.place_name
            city = str(city)
            self.city_entry.text = city
        else:
            self.city_entry.text = ''

    def updateMapView(self, street_entry, post_code_entry, city_entry, radius_entry, fuel_entry, addresse_label, essence_label):
        self.remove_widget(self.addresse_label)
        self.remove_widget(self.essence_label)

        self.add_widget(self.download_data_label)
        
        self.street_entry_post = street_entry
        self.post_code_entry_post = post_code_entry
        self.city_entry_post = city_entry
        self.radius_entry_post = radius_entry
        self.fuel_entry_post = fuel_entry
        self.addresse_label_post = addresse_label
        self.essence_label_post = essence_label

        self.points = []

        self.address=f'{self.street_entry_post} {self.post_code_entry_post} {self.city_entry_post}'

        self.locator = Nominatim(user_agent="low-fuel")
        self.location = self.locator.geocode(self.address)
        
        if self.locator.geocode(self.address) is None or (self.street_entry_post == '' or self.post_code_entry_post == '' or self.city_entry_post == ''):
            self.remove_widget(self.download_data_label)
            self.add_widget(self.addresse_label)
            return None
        else:
            for c in list(self.children):
                if c == self.addresse_label: self.remove_widget(self.addresse_label)
            if self.fuel_entry_post != 'Gazole' and self.fuel_entry_post != 'SP98' and self.fuel_entry_post != 'SP95' and self.fuel_entry_post!= 'GPLc' and self.fuel_entry_post != 'E10' and self.fuel_entry_post != 'E85':
                self.remove_widget(self.download_data_label)
                self.add_widget(self.essence_label)
                return None
            else:
                for c in list(self.children):
                    if c == self.essence_label: self.remove_widget(self.essence_label)

        self.idClient = uuid.uuid1()

        self.user_address = AddressUser(self.idClient, str(self.street_entry_post),  str(self.post_code_entry_post), str(self.city_entry_post), str(self.radius_entry_post))
        self.location = address_to_coord(self.user_address.street + ' ' + self.user_address.post_code + ' ' + self.user_address.city) 
        self.user_address = AddressUser(self.idClient, str(self.street_entry_post),  str(self.post_code_entry_post), str(self.city_entry_post), str(self.radius_entry_post), self.location[0],self.location[1])

        if self.location[1] > 0:
            self.location_1 = f'+{self.location[1]}' 
        else:
            self.location_1 = str(self.location[1])
        self.radius = '+' + str(float(self.radius_entry_post) * 1000) 
        self.url_data : str = f'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&refine.prix_nom={self.fuel_entry_post}&geofilter.distance={self.location[0]},{self.location_1},{self.radius}&timezone=Europe/Berlin&lang=fr'
        self.path_of_file : str = 'info.gouv/prix-carburants.json'
        # TODO ajout irve : https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&lang=fr&rows=20&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep&geofilter.distance=47.439%2C+0.699%2C+5000
        self.remove_widget(self.download_data_label)

        self.add_widget(self.loading_label)

        self.parsejson = ParseJson(self.url_data, self.path_of_file, self.user_address)

        self.my_sell_points: List[SellPoint] = self.parsejson.station_list()

        self.sellpoint: SellPoint

        self.points.append((self.location[0], self.location[1], f'[b]Point de départ[/b]\n{self.street_entry_post.title()}\n{self.post_code_entry_post} {self.city_entry_post.upper()}' , colorHtmlToKivy('#00FF00')))

        i = 0

        for self.sellpoint in self.my_sell_points:
            text1 = '[b]' + self.sellpoint.name + '[/b]'
            text2 = str(self.sellpoint.address[0]).title() + '\n' + str(self.sellpoint.address[1]) + ' ' + str(self.sellpoint.address[2]).upper()
            text3 = ""
            text5 = ""
            text6 = ""
            text7 = ""
            if self.sellpoint.week_hours.is_24_24:
                text3 = "pompe(s) ouverte(s) 24h/24"
            else:
                if self.sellpoint.week_hours.day_hours[0][0][0] == "horaire non précisé":
                    text3 = "horaire non précisé"
                else:
                    text5 = ""
                    text6 = ""
                    text7 = ""
                    for self.jour in range(0, 6):
                        self.jour_en_lettre = str(self.sellpoint.week_hours.day_hours[0][self.jour][0])
                        if self.sellpoint.week_hours.day_hours[0][self.jour][1]:
                            text5 +=  '\n' + self.jour_en_lettre + " pas d'horaire spécifiée"
                        else:
                            self.opening = self.sellpoint.week_hours.day_hours[0][self.jour][2][0]
                            self.closing = self.sellpoint.week_hours.day_hours[0][self.jour][2][1]
                            if self.opening.__len__() == 2:
                                text6 += '\n' + self.jour_en_lettre + " ouverture le matin de " + self.opening[0].replace('.', 'h') + " à " + self.opening[1].replace('.', 'h') + " et l'après midi' de " + self.closing[0].replace('.', 'h') + " à " + self.closing[1].replace('.', 'h')
                                
                            else:
                                text7 += '\n' + self.jour_en_lettre + " ouverture de " + self.opening.replace('.', 'h') + " à " +self.closing.replace('.', 'h')
            prices_txt: str = ""
            for price in self.sellpoint.prices:
                if price != []:
                    prices_txt += "[b]\nCarburant " + str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\nDernière mise à jour du prix :" + "\n" + str(price[2]) + "\n[/b]"          
            proposed_services: str = ""
            key = 0
            for service in self.sellpoint.services:
                if key <=4:
                    proposed_services += str(service) + ',\n'
                    key += 1
            text8 = "Station à " + str(round(self.sellpoint.distance,2)).replace('.', ',') + ' km'

            data_text = text1 + '\n' + text2 + '\n' + text3 + '\n' + text5 + '\n' + text6 + '\n' + text7 + '\n' + prices_txt + '\n' + proposed_services + '\n' + text8

            if self.sellpoint.name == self.parsejson.get_low_price_name():
                self.color = colorHtmlToKivy('#736A7C')
            else:
               self.color = colorHtmlToKivy('#FF0000')

        
            self.data_text = os.linesep.join([s for s in data_text.splitlines() if s])

            self.points.append((self.sellpoint.address[3], self.sellpoint.address[4], self.data_text, self.color))
        
        self.remove_widget(self.loading_label)

        kivy = kivyUi(self.points, self, self.mapview)
        kivy.createMarkerPopup(self.points)
        kivy.newLat = self.location[0]
        kivy.newLon = self.location[1]
        kivy.changeViewOfMap()


class Low_Fuel(App):
    def build(self):
        self.title = 'Low-Fuel'
        self.icon = 'image/petrol_pump.png'
        self.root = RootWidget()
 

if __name__ == '__main__' and __package__ is None:
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    Low_Fuel().run()