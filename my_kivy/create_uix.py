from parsedata.parse_json import ParseJson
from domain.user import AddressUser
from domain.logic import address_to_coord
from domain.data import SellPoint
from my_kivy.my_widgets import ColoredLabel, SmoothButton
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage, Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapMarkerPopup
from kivy_garden.mapview import MapView
from kivy.clock import Clock
from kivy import utils
from uuid_extensions import uuid7str
from geopy import Nominatim
from typing import List
import os
import platform
import sys
import pgeocode
import random
import numpy as np

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


class kivyUi():
    def __init__(self, root):

        self.RootWidget = root

        # random position
        Nord = 51.08916667
        Sud = 42.33277778
        Est = 8.23055556
        Ouest = -4.79555556
        self.random_latitude = random.uniform(Sud, Nord)
        self.random_longitude = random.uniform(Ouest, Est)

        self.city_entry = ''
        self.city_btn_number = 0

        # let's add a Widget to this layout
        user_folder = os.path.expanduser("~")
        if platform.system() == 'Darwin':
            self.tmp_dir = user_folder + '/Library/Low-Fuel/'
        if platform.system() == 'Linux':
            self.tmp_dir = '/tmp/Low-Fuel/'
        if platform.system() == 'Windows':
            self.tmp_dir = user_folder + '\\AppData\\Local\\Temp\\Low-Fuel\\'

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
        self.gui_interface()

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def gui_interface(self):

        self.mapview = MapView(
            lat=self.random_latitude,
            lon=self.random_longitude,
            zoom=12, map_source="osm",
            size_hint=(1, 1),
            cache_dir=self.tmp_dir
        )

        self.street_label = ColoredLabel(
            text="    Numéro et\nNom de la Rue",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.248, .098),
            pos_hint={'x': 0.0005, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.street_entry = TextInput(
            size_hint=(.249, .05), pos_hint={'x': 0, 'y': .85})
        self.street_entry.bind(text=self.on_text)

        self.post_code_label = ColoredLabel(
            text=" Code\nPostal",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.082333333333, .098),
            pos_hint={'x': .25, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.post_code_entry = TextInput(
            size_hint=(.082333333333, .05),
            pos_hint={'x': .25, 'y': .85}
        )

        self.post_code_entry.bind(text=self.on_text_)

        self.city_label = ColoredLabel(
            text="Ville",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.16566667, .098),
            pos_hint={'x': .33333333, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.city_DropDown = DropDown()
        self.city_button_DropDown = SmoothButton(
            text="Entrer le CP",
            size_hint=(.165666667, .048),
            pos_hint={'x': .33333333, 'y': .851},
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(.906, .906, .906, 1),
            border_color=(0, 0, 0, 1),
            border_width=1
        )

        self.city_button_DropDown.bind(on_release=self.city_DropDown.open)
        self.city_DropDown.bind(on_select=lambda instance, x: setattr(
            self.city_button_DropDown, 'text', x))

        self.radius_label = ColoredLabel(
            text="     Rayon\nd'action(km)",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.165666667, .098),
            pos_hint={'x': .5, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.radius_entry = TextInput(
            size_hint=(.16566667, .05), pos_hint={'x': .5, 'y': .85})
        self.radius_entry.bind(text=self.on_text)

        self.addresse_label = ColoredLabel(
            text="Adresse Non trouvé",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.34509803921568627,
                              0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.essence_label = ColoredLabel(
            text="Type d'essence non correct",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.34509803921568627,
                              0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )

        self.fuel_DropDown = DropDown()
        self.btn_Gazole = SmoothButton(
            text='Gazole',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_Gazole.bind(
            on_release=lambda btn_Gazole: self.fuel_DropDown.select(self.btn_Gazole.text))
        self.btn_SP95 = SmoothButton(
            text='SP95',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_SP95.bind(
            on_release=lambda btn_SP95: self.fuel_DropDown.select(self.btn_SP95.text))
        self.btn_SP98 = SmoothButton(
            text='SP98',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_SP98.bind(
            on_release=lambda btn_SP98: self.fuel_DropDown.select(self.btn_SP98.text))
        self.btn_E85 = SmoothButton(
            text='E85',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_E85.bind(
            on_release=lambda btn_E85: self.fuel_DropDown.select(self.btn_E85.text))
        self.btn_E10 = SmoothButton(
            text='E10',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_E10.bind(
            on_release=lambda btn_E10: self.fuel_DropDown.select(self.btn_E10.text))
        self.btn_GPLc = SmoothButton(
            text='GPLc',
            size_hint_y=None,
            height=44,
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.btn_GPLc.bind(
            on_release=lambda btn_GPLc: self.fuel_DropDown.select(self.btn_GPLc.text))
        self.button_DropDown = SmoothButton(
            text="Carburant utilisé",
            size_hint=(.16666667, .1425),
            pos_hint={'x': .6666667, 'y': .855},
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )

        self.button_DropDown.bind(on_release=self.fuel_DropDown.open)
        self.fuel_DropDown.bind(on_select=lambda instance, x: setattr(
            self.button_DropDown, 'text', x))
        self.submitButton = SmoothButton(
            text="Mettre à jour",
            size_hint=(.16416667, .1425),
            pos_hint={'x': .833333333, 'y': .855},
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2)
        self.submitButton.bind(on_press=lambda instance: self.intermediate(self.street_entry.text, self.post_code_entry.text,
                               self.city_button_DropDown.text, self.radius_entry.text, self.button_DropDown.text, self.addresse_label, self.essence_label))

        self.gif = 'image/Logo_Bit-Scripts.gif'
        if platform.system() == 'Windows':
            self.gif = 'image\\logo_Bit-Scripts.gif'

        self.bit_scripts_logo = Image(
            source=self.resource_path(self.gif),
            size_hint=(.1, .1),
            pos_hint={'x': .01, 'y': .01},
            anim_delay=.5,
            anim_loop=0
        )

        self.RootWidget.add_widget(self.mapview)
        self.RootWidget.add_widget(self.submitButton)
        self.fuel_DropDown.add_widget(self.btn_Gazole)
        self.fuel_DropDown.add_widget(self.btn_SP98)
        self.fuel_DropDown.add_widget(self.btn_SP95)
        self.fuel_DropDown.add_widget(self.btn_E85)
        self.fuel_DropDown.add_widget(self.btn_E10)
        self.fuel_DropDown.add_widget(self.btn_GPLc)
        self.RootWidget.add_widget(self.button_DropDown)
        self.RootWidget.add_widget(self.street_label)
        self.RootWidget.add_widget(self.street_entry)
        self.RootWidget.add_widget(self.post_code_label)
        self.RootWidget.add_widget(self.post_code_entry)
        self.RootWidget.add_widget(self.city_label)
        self.RootWidget.add_widget(self.city_button_DropDown)
        self.RootWidget.add_widget(self.radius_label)
        self.RootWidget.add_widget(self.radius_entry)
        self.RootWidget.add_widget(self.bit_scripts_logo)
        self.locator = Nominatim(user_agent="low-fuel")
        self.locator = Nominatim(user_agent="low-fuel")

    def __enter__(self):
        return self.name

    def on_text(self, instance, value):
        pass

    def on_text_(self, instance, value):
        if value != '' and len(value) == 5 and (str(int(value)) == value or '0' + str(int(value)) == value):
            nomi = pgeocode.Nominatim('fr')
            city = nomi.query_postal_code(value)
            city = city.place_name
            city = str(city).split(', ')
            if len(city) == 1:
                self.btn_city = SmoothButton(
                    text=city[0],
                    size_hint_y=None,
                    height=22,
                    color=(0, 0, 0, 1),
                    background_normal='',
                    background_color=(.906, .906, .906, 1),
                    border=(0, 0, 0, 1),
                    border_color=(0, 0, 0, 1),
                    border_width=1
                )

                self.btn_city.bind(
                    on_release=lambda city_DropDown: self.city_DropDown.select(self.btn_city.text))
                self.city_DropDown.add_widget(self.btn_city)
            else:
                for index in range(len(city) - 1):
                    btn_city = SmoothButton(
                        text=f'{city[index]}',
                        size_hint_y=None,
                        height=22,
                        color=(0, 0, 0, 1),
                        background_normal='',
                        background_color=(.906, .906, .906, 1),
                        border=(0, 0, 0, 1),
                        border_color=(0, 0, 0, 1),
                        border_width=1
                    )
                    btn_city.bind(
                        on_release=lambda btn_city: self.city_DropDown.select(btn_city.text))
                    self.city_DropDown.add_widget(btn_city)
            self.city_DropDown.open(self.city_button_DropDown)
        else:
            self.city_DropDown.dismiss()
            self.city_DropDown.clear_widgets()

    def intermediate(
        self,
        street_entry,
        post_code_entry,
        city_DropDown,
        radius_entry,
        button_DropDown,
        addresse_label,
        essence_label
    ):

        self.download_data_label = ColoredLabel(
            text="Récupération des données",
            color=(0, 0, 0, 1),
            background_color=(0.34509803921568627,
                              0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        self.loading_label = ColoredLabel(
            text="Traitement des données",
            color=(0, 0, 0, 1),
            background_color=(0.34509803921568627,
                              0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1))
        self.RootWidget.add_widget(self.download_data_label)
        Clock.schedule_once(lambda dt: self.next_intermediate(
            street_entry,
            post_code_entry,
            city_DropDown,
            radius_entry,
            button_DropDown,
            addresse_label,
            essence_label
        ),
            0)

    def next_intermediate(
        self,
        street_entry,
        post_code_entry,
        city_entry,
        radius_entry,
        fuel_entry,
        addresse_label,
        essence_label
    ):

        self.RootWidget.remove_widget(self.addresse_label)
        self.RootWidget.remove_widget(self.essence_label)
        Clock.schedule_once(lambda dt: self.next_update(
            street_entry,
            post_code_entry,
            city_entry,
            radius_entry,
            fuel_entry,
            addresse_label,
            essence_label
        ),
            0)

    def next_update(
        self,
        street_entry,
        post_code_entry,
        city_entry,
        radius_entry,
        fuel_entry,
        addresse_label,
        essence_label
    ):

        self.street_entry_post = street_entry
        self.post_code_entry_post = post_code_entry
        self.city_entry_post = city_entry
        self.radius_entry_post = radius_entry
        self.fuel_entry_post = fuel_entry
        self.addresse_label = addresse_label
        self.essence_label = essence_label

        self.points = []

        self.address = f'{self.street_entry_post} {self.post_code_entry_post} {self.city_entry_post}'

        self.locator = Nominatim(user_agent="low-fuel")
        self.location = self.locator.geocode(self.address)

        if self.locator.geocode(self.address) is None or (self.street_entry_post == '' or self.post_code_entry_post == '' or self.city_entry_post == ''):
            self.RootWidget.remove_widget(self.download_data_label)
            self.RootWidget.add_widget(self.addresse_label)
            return None
        else:
            for c in list(self.RootWidget.children):
                if c == self.addresse_label:
                    self.RootWidget.remove_widget(self.addresse_label)
            if self.fuel_entry_post != 'Gazole' and self.fuel_entry_post != 'SP98' and self.fuel_entry_post != 'SP95' and self.fuel_entry_post != 'GPLc' and self.fuel_entry_post != 'E10' and self.fuel_entry_post != 'E85':

                self.RootWidget.remove_widget(self.download_data_label)
                self.RootWidget.add_widget(self.essence_label)
                return None
            else:
                for c in list(self.RootWidget.children):
                    if c == self.essence_label:
                        self.RootWidget.remove_widget(self.essence_label)

        self.idClient = uuid7str()

        self.user_address = AddressUser(
            self.idClient,
            str(self.street_entry_post),
            str(self.post_code_entry_post),
            str(self.city_entry_post),
            str(self.radius_entry_post)
        )

        self.location = address_to_coord(
            self.user_address.street + ' ' +
            self.user_address.post_code + ' ' + self.user_address.city
        )

        self.user_address = AddressUser(
            self.idClient,
            str(self.street_entry_post),
            str(self.post_code_entry_post),
            str(self.city_entry_post),
            str(self.radius_entry_post),
            self.location[0],
            self.location[1]
        )

        if self.location[1] > 0:
            self.location_1 = f'+{self.location[1]}'
        else:
            self.location_1 = str(self.location[1])
        self.radius = '+' + str(float(self.radius_entry_post) * 1000)

        self.url_data: str = f'https://data.economie.gouv.fr/explore/dataset/prix-carburants-fichier-instantane-test-ods-copie/download/?format=json&q=&refine.prix_nom={self.fuel_entry_post}&geofilter.distance={self.location[0]},{self.location_1},{self.radius}&timezone=Europe/Berlin&lang=fr'

        self.path_of_file: str = self.tmp_dir

        # TODO ajout irve : https://public.opendatasoft.com/api/records/1.0/search/?dataset=fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve&q=&lang=fr&rows=20&facet=n_enseigne&facet=nbre_pdc&facet=puiss_max&facet=accessibilite&facet=nom_epci&facet=commune&facet=nom_reg&facet=nom_dep&geofilter.distance=47.439%2C+0.699%2C+5000

        self.RootWidget.remove_widget(self.download_data_label)

        Clock.schedule_once(lambda dt: self.near_updateMapView(
            self.street_entry_post,
            self.post_code_entry_post,
            self.city_entry_post
        ),
            0
        )

    def near_updateMapView(
        self,
        street_entry,
        post_code_entry,
        city_entry
    ):

        self.RootWidget.add_widget(self.loading_label)
        Clock.schedule_once(lambda dt: self.updateMapView(
            street_entry,
            post_code_entry,
            city_entry
        ),
            0
        )

    def updateMapView(
        self,
        street_entry,
        post_code_entry,
        city_entry
    ):

        self.street_entry_post = street_entry
        self.post_code_entry_post = post_code_entry
        self.city_entry_post = city_entry
        self.parsejson = ParseJson(
            self.url_data,
            self.path_of_file,
            self.user_address
        )

        self.my_sell_points: List[SellPoint] = self.parsejson.station_list()

        self.sellpoint: SellPoint

        self.points.append(
            [self.location[0],
             self.location[1],
             f'[b]Point de départ[/b]\n{self.street_entry_post.title()}\n{self.post_code_entry_post} {self.city_entry_post.upper()}',
             utils.get_color_from_hex('#3BAECF')]
        )

        i = 0

        for self.sellpoint in self.my_sell_points:
            text1 = '[b]' + self.sellpoint.name + '[/b]'
            text2 = f'{self.sellpoint.address.street.title()}\n{self.sellpoint.address.post_code} {self.sellpoint.address.city.upper()}'
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
                        self.jour_en_lettre = str(
                            self.sellpoint.week_hours.day_hours[0][self.jour][0])
                        if self.sellpoint.week_hours.day_hours[0][self.jour][1]:
                            text5 += '\n' + self.jour_en_lettre + " pas d'horaire spécifiée"
                        else:
                            self.opening = self.sellpoint.week_hours.day_hours[0][self.jour][2][0]
                            self.closing = self.sellpoint.week_hours.day_hours[0][self.jour][2][1]
                            if self.opening.__len__() == 2:
                                text6 += '\n' + self.jour_en_lettre + " ouverture le matin de " + self.opening[0].replace('.', 'h') + " à " + self.opening[1].replace(
                                    '.', 'h') + " et l'après midi' de " + self.closing[0].replace('.', 'h') + " à " + self.closing[1].replace('.', 'h')

                            else:
                                text7 += '\n' + self.jour_en_lettre + " ouverture de " + \
                                    self.opening.replace(
                                        '.', 'h') + " à " + self.closing.replace('.', 'h')
            self.prices_txt: str = ""
            for price in self.sellpoint.prices:
                if price != []:
                    self.prices_txt += f'[b]\nCarburant {price.fuel_type} à {str(price.value).replace(".", ",")} €/L\nDernière mise à jour du prix :\n{price.last_updated}\n[/b]'
            proposed_services: str = ""
            key = 0
            for service in self.sellpoint.services:
                if key <= 4:
                    proposed_services += str(service) + ',\n'
                    key += 1
            text8 = "Station à " + \
                str(round(self.sellpoint.distance, 2)).replace('.', ',') + ' km'

            data_text = text1 + '\n' + text2 + '\n' + text3 + '\n' + text5 + '\n' + text6 + \
                '\n' + text7 + '\n' + self.prices_txt + '\n' + proposed_services + '\n' + text8

            if self.sellpoint.name == self.parsejson.get_low_price_name():
                self.color = utils.get_color_from_hex('#000000')
            elif self.sellpoint.name == self.parsejson.get_high_price_name():
                self.color = utils.get_color_from_hex('#000000')
            else:
                self.color = utils.get_color_from_hex('#000000')

            self.data_text = os.linesep.join(
                [s for s in data_text.splitlines() if s])

            self.points.append(
                [self.sellpoint.address.latitude,
                 self.sellpoint.address.longitude,
                 self.data_text,
                 self.color]
            )

        self.RootWidget.remove_widget(self.loading_label)
        Clock.schedule_once(lambda dt: self.end_of_update_mapview(), 0)
        self.list_low_price()

    def list_low_price(self):
        self.price_array = []
        for sellpoint in self.my_sell_points:
            if sellpoint.prices[0].fuel_type == self.button_DropDown.text:
                self.prices_txt_ = f'[b]\nCarburant {sellpoint.prices[0].fuel_type}\nà {str(sellpoint.prices[0].value).replace(".", ",")} €/L[/b]'
                if sellpoint.prices[0].fuel_type == self.button_DropDown.text:
                    price_list = {"prix":sellpoint.prices[0].value, "name":sellpoint.name, "address":f'{sellpoint.address.street}\n{sellpoint.address.post_code} {sellpoint.address.city}', "text":self.prices_txt_, "latitude":sellpoint.address.latitude, "longitude":sellpoint.address.longitude}
                    self.price_array.append(price_list)

        self.price_array = sorted(self.price_array, key=lambda d: d["prix"])
        points = []
        match len(self.price_array):
            case 0:
                y = .63
                moins_cher = ColoredLabel(
                    text='Pas de Station',
                    markup=True,
                    halign='center',
                    valign='center',
                    color=utils.get_color_from_hex('#000000'),
                    background_color=(0.45098, 0.64706, 0.45098, 1),
                    size_hint=(.18536667, .1435),
                    pos_hint={'x': .803333333, 'y': y},
                    border_width=1.5,
                    border_color=(0, 0, 0, 1)
                )
                self.RootWidget.add_widget(moins_cher)
            case 1 | 2 | 3 | 4 | 5:
                for index in range(len(self.price_array)):
                    y = .63 - (index * .14)

                    text = f'[size=10][b]{self.price_array[index].get("name")}[/b]\n{self.price_array[index].get("address")}\n{self.price_array[index].get("text")}\n[/size]'

                    if   index == 0: color=utils.get_color_from_hex('#00FF00')
                    elif index == 1: color=utils.get_color_from_hex('#99FF00')
                    elif index == 2: color=utils.get_color_from_hex('#FFFF00')
                    elif index == 3: color=utils.get_color_from_hex('#FF9900')
                    elif index == 4: color=utils.get_color_from_hex('#FF3300')
                    elif index == 4: color=utils.get_color_from_hex('#FF0000')

                    moins_cher = ColoredLabel(
                        text=text,
                        markup=True,
                        halign='center',
                        valign='center',
                        color=utils.get_color_from_hex('#000000'),
                        background_color=color,
                        size_hint=(.18536667, .1435),
                        pos_hint={'x': .803333333, 'y': y},
                        border_width=1.5,
                        border_color=(0, 0, 0, 1)
                    )
                    self.RootWidget.add_widget(moins_cher)
                    for point in range(len(self.points) - 1):
                        if self.points[point][0] == self.price_array[index].get("latitude") and self.points[point][1] == self.price_array[index].get("longitude"):
                            self.points[point][3] = color 
            case _:
                for index in range(5):
                    y = .63 - (index * .14)

                    text = f'[size=10][b]{self.price_array[index].get("name")}[/b]\n{self.price_array[index].get("address")}\n{self.price_array[index].get("text")}\n[/size]'

                    if   index == 0: color=utils.get_color_from_hex('#00FF00')
                    elif index == 1: color=utils.get_color_from_hex('#99FF00')
                    elif index == 2: color=utils.get_color_from_hex('#FFFF00')
                    elif index == 3: color=utils.get_color_from_hex('#FF9900')
                    elif index == 4: color=utils.get_color_from_hex('#FF3300')
                    elif index == 4: color=utils.get_color_from_hex('#FF0000')

                    moins_cher = ColoredLabel(
                        text=text,
                        markup=True,
                        halign='center',
                        valign='top',
                        color=utils.get_color_from_hex('#000000'),
                        background_color=color,
                        size_hint=(.18536667, .1435),
                        pos_hint={'x': .80333333, 'y': y},
                        border_width=1.5,
                        border_color=(0, 0, 0, 1)
                    )
                    self.RootWidget.add_widget(moins_cher)
                    for point in range(len(self.points) - 1):
                        if self.points[point][0] == self.price_array[index].get("latitude") and self.points[point][1] == self.price_array[index].get("longitude"):
                            self.points[point][3] = color 


    def end_of_update_mapview(self):
        self.points
        self.mapview
        self.createMarkerPopup(self.points)
        self.newLat = self.location[0]
        self.newLon = self.location[1]
        self.changeViewOfMap()

    def changeViewOfMap(self):
        self.mapview.center_on(self.newLat, self.newLon)

    def createMarkerPopup(self, points):
        self.points = points
        for point in self.points:
            mapMarkerPopup = MapMarkerPopup(
                lat=point[0],
                lon=point[1],
                popup_size=(600, 400),
                color=point[3]
            )

            bubble = Bubble()
            boxLayout = BoxLayout(
                orientation="horizontal",
                padding="5dp"
            )

            label = Label(text=point[2], markup=True, halign="center")

            asyncImage = AsyncImage(
                source="https://github.com/Bit-Scripts/Low-Fuel/raw/main/image/Fuel_gauge-250.jpg", mipmap=True)

            boxLayout.add_widget(asyncImage)
            boxLayout.add_widget(label)
            bubble.add_widget(boxLayout)
            mapMarkerPopup.add_widget(bubble)
            self.mapview.add_widget(mapMarkerPopup)

    def on_text(
        self,
        instance,
        value
    ):
        pass
