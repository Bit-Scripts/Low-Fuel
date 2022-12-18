import os
import sys
import uuid
from Kivy.create_uix import kivyUi
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

from kivy_garden.mapview import MapView
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle


from Kivy.coloredlabel import ColoredLabel
from domain.logic import colorHtmlToKivy

if __name__ == '__main__' and __package__ is None:
    from os import path

    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


locator = Nominatim(user_agent="low-fuel")

# creating markers
points: List[any] = []

def on_text(instance, value):
    print('The widget', instance, 'have:', value)

# random position
Nord  = 51.08916667 
Sud   = 42.33277778
Est   =  8.23055556
Ouest = -4.79555556
random_latitude = random.uniform(Sud, Nord)
random_longitude = random.uniform(Ouest, Est)

root = FloatLayout()

mapview = MapView(lat=random_latitude, lon=random_longitude, zoom=12, map_source="osm", size_hint=(1, 1))

root.add_widget(mapview)

street_label = ColoredLabel(text="    Numéro et\nNom de la Rue", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.249,.098), pos_hint={'x': 0, 'y': .9})
street_entry = TextInput(size_hint=(.249,.05), pos_hint={'x': 0, 'y': .85})
street_entry.bind(text=on_text)

post_code_label = ColoredLabel(text=" Code\nPostal", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.082333333333,.098), pos_hint={'x': .25, 'y': .9})
post_code_entry = TextInput(size_hint=(.082333333333,.05), pos_hint={'x': .25, 'y': .85})
post_code_entry.bind(text=on_text)

city_label = ColoredLabel(text="Ville", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.16566667,.098), pos_hint={'x': .33333333, 'y': .9})
city_entry = TextInput(size_hint=(.16566667,.05), pos_hint={'x': .33333333, 'y': .85})
city_entry.bind(text=on_text)

radius_label = ColoredLabel(text="     Rayon\nd'action(km)", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,1), size_hint=(.165666667,.098), pos_hint={'x': .5, 'y': .9})
radius_entry = TextInput(size_hint=(.16566667,.05), pos_hint={'x': .5, 'y': .85})
radius_entry.bind(text=on_text)

addresse_label = ColoredLabel(text="Adresse Non trouvé", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
essence_label = ColoredLabel(text="Type d'essence non correct", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})

fuel_DropDown = DropDown()
btn_Gazole = Button(text='Gazole', size_hint_y=None, height=44)
btn_Gazole.bind(on_release=lambda btn_Gazole: fuel_DropDown.select(btn_Gazole.text))
btn_SP95 = Button(text='SP95', size_hint_y=None, height=44)
btn_SP95.bind(on_release=lambda btn_SP95: fuel_DropDown.select(btn_SP95.text))
btn_SP98 = Button(text='SP98', size_hint_y=None, height=44)
btn_SP98.bind(on_release=lambda btn_SP98: fuel_DropDown.select(btn_SP98.text))
btn_E85 = Button(text='E85', size_hint_y=None, height=44)
btn_E85.bind(on_release=lambda btn_E85: fuel_DropDown.select(btn_E85.text))
btn_E10 = Button(text='E10', size_hint_y=None, height=44)
btn_E10.bind(on_release=lambda btn_E10: fuel_DropDown.select(btn_E10.text))
btn_GPLc = Button(text='GPLc', size_hint_y=None, height=44)
btn_GPLc.bind(on_release=lambda btn_GPLc: fuel_DropDown.select(btn_GPLc.text))
button_DropDown = Button(text="Carburant utilisé", size_hint=(.16666667, .15), pos_hint={'x': .66666667, 'y': .85})
button_DropDown.bind(on_release=fuel_DropDown.open)
fuel_DropDown.bind(on_select=lambda instance, x: setattr(button_DropDown, 'text', x))

submitButton = Button(text="Mettre à jour", size_hint=(.16666667, .15), pos_hint={'x': .833333333, 'y': .85}) 
submitButton.bind(on_press=lambda instance: updateMapView(street_entry.text, post_code_entry.text, city_entry.text, radius_entry.text, button_DropDown.text, addresse_label, essence_label))

root.add_widget(submitButton)
fuel_DropDown.add_widget(btn_Gazole)
fuel_DropDown.add_widget(btn_SP98)
fuel_DropDown.add_widget(btn_SP95)
fuel_DropDown.add_widget(btn_E85)
fuel_DropDown.add_widget(btn_E10)
fuel_DropDown.add_widget(btn_GPLc)
root.add_widget(button_DropDown)
root.add_widget(street_label)
root.add_widget(street_entry)
root.add_widget(post_code_label)
root.add_widget(post_code_entry)
root.add_widget(city_label)
root.add_widget(city_entry)
root.add_widget(radius_label)
root.add_widget(radius_entry)

def updateMapView(street_entry, post_code_entry, city_entry, radius_entry, fuel_entry, addresse_label, essence_label):
    
    download_data_label = ColoredLabel(text="Récupération des données", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
    root.add_widget(download_data_label)

    points = []

    address=f'{street_entry} {post_code_entry} {city_entry}'

    locator = Nominatim(user_agent="low-fuel")
    location = locator.geocode(address)

    
    if locator.geocode(address) is None or (street_entry == '' or post_code_entry == '' or city_entry == ''):
        root.remove_widget(download_data_label)
        root.add_widget(addresse_label)
        return None
    else:
        for c in list(root.children):
            if c == addresse_label: root.remove_widget(addresse_label)
        if fuel_entry != 'Gazole' and fuel_entry != 'SP98' and fuel_entry != 'SP95' and fuel_entry != 'GPLc' and fuel_entry != 'E10' and fuel_entry != 'E85':
            root.remove_widget(download_data_label)
            root.add_widget(essence_label)
            return None
        else:
            for c in list(root.children):
                if c == essence_label: root.remove_widget(essence_label)

    root.remove_widget(download_data_label)
    loading_label = ColoredLabel(text="Traitement des données", color=colorHtmlToKivy('#ffffff'), background_color=(0.34509803921568627,0.34509803921568627,0.34509803921568627,.65), size_hint=(.4,.2), pos_hint={'x': .3, 'y': .4})
    root.add_widget(loading_label)

    idClient = uuid.uuid1()

    user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry))
    location = address_to_coord(user_address.street + ' ' + user_address.post_code + ' ' + user_address.city) 
    user_address = AddressUser(idClient, str(street_entry),  str(post_code_entry), str(city_entry), str(radius_entry), location[0],location[1])

    if location[1] > 0:
        location_1 = f'+{location[1]}' 
    else:
        location_1 = str(location[1])
    radius = '+' + str(float(radius_entry) * 1000) 
    url_data : str = f'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&refine.prix_nom={fuel_entry}&geofilter.distance={location[0]},{location_1},{radius}&timezone=Europe/Berlin&lang=fr'
    path_of_file : str = 'info.gouv/prix-carburants.json'

    parsejson = ParseJson(url_data, path_of_file, user_address)

    my_sell_points: List[SellPoint] = parsejson.station_list()

    sellpoint: SellPoint

    points.append((location[0], location[1], f'[b]Point de départ[/b]\n{street_entry.title()}\n{post_code_entry} {city_entry.upper()}' , colorHtmlToKivy('#00FF00')))

    i = 0

    for sellpoint in my_sell_points:
        text1 = '[b]' + sellpoint.name + '[/b]'
        text2 = str(sellpoint.address[0]).title() + '\n' + str(sellpoint.address[1]) + ' ' + str(sellpoint.address[2]).upper()
        text3 = ""
        text5 = ""
        text6 = ""
        text7 = ""
        if sellpoint.week_hours.is_24_24:
            text3 = "pompe(s) ouverte(s) 24h/24"
        else:
            if sellpoint.week_hours.day_hours[0][0][0] == "horaire non précisé":
                text3 = "horaire non précisé"
            else:
                text5 = ""
                text6 = ""
                text7 = ""
                for jour in range(0, 6):
                    jour_en_lettre = str(sellpoint.week_hours.day_hours[0][jour][0])
                    if sellpoint.week_hours.day_hours[0][jour][1]:
                        text5 +=  '\n' + jour_en_lettre + " pas d'horaire spécifiée"
                    else:
                        opening = sellpoint.week_hours.day_hours[0][jour][2][0]
                        closing = sellpoint.week_hours.day_hours[0][jour][2][1]
                        if opening.__len__() == 2:
                            text6 += '\n' + jour_en_lettre + " ouverture le matin de " + opening[0].replace('.', 'h') + " à " + opening[1].replace('.', 'h') + " et l'après midi' de " + closing[0].replace('.', 'h') + " à " + closing[1].replace('.', 'h')
                            
                        else:
                            text7 += '\n' + jour_en_lettre + " ouverture de " + opening.replace('.', 'h') + " à " + closing.replace('.', 'h')
        prices_txt: str = ""
        for price in sellpoint.prices:
            if price != []:
                prices_txt += "[b]\nCarburant " + str(price[1]) + " à " + str(price[3]).replace('.', ',') + "€/L\nDernière mise à jour du prix :" + "\n" + str(price[2]) + "\n[/b]"          
        proposed_services: str = ""
        key = 0
        for service in sellpoint.services:
            if key <=4:
                proposed_services += str(service) + ',\n'
                key += 1
        text8 = "Station à " + str(round(sellpoint.distance,2)).replace('.', ',') + ' km'

        data_text = text1 + '\n' + text2 + '\n' + text3 + '\n' + text5 + '\n' + text6 + '\n' + text7 + '\n' + prices_txt + '\n' + proposed_services + '\n' + text8

        if sellpoint.name == parsejson.get_low_price_name():
            color = colorHtmlToKivy('#736A7C')
        else:
            color = colorHtmlToKivy('#FF0000')

       
        data_text = os.linesep.join([s for s in data_text.splitlines() if s])

        points.append((sellpoint.address[3], sellpoint.address[4], data_text, color))
    
    root.remove_widget(loading_label)

    kivy.createMarkerPopup(points)
    kivy.newLat = location[0]
    kivy.newLon = location[1]
    kivy.changeViewOfMap()

kivy = kivyUi(points, root, mapview)

runTouchApp(kivy.root)
