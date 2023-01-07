from parsedata.parse_json import ParseJson
from domain.user import AddressUser
from domain.logic import address_to_coord
from domain.data import SellPoint
from my_kivy.metier import tmp_dir
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy_garden.mapview import MapMarkerPopup
from kivy.clock import Clock
from kivy import utils
from uuid_extensions import uuid7str
from geopy import Nominatim
from typing import List
import os
import sys
import pgeocode

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class kivyUi():
    def __init__(self, root, city_button_DropDown, btn0, mapView, button_DropDown_Fuel, loadingText, traitementText, uiStatic, floatLayout):
                        
        self.RootWidget = root
        
        self.tmp_dir = tmp_dir()
        
        self.city_button_DropDown = city_button_DropDown
        self.btn0 = btn0
        self.mapview = mapView
        self.button_DropDown_Fuel = button_DropDown_Fuel
        self.loadingText = loadingText
        self.traitementText = traitementText
        self.uiStatic = uiStatic
        self.floatLayout = floatLayout
        
        self.city_entry = ''
        self.city_btn_number = 0
        
        self.address_error_bool = False
        self.essence_error_bool = False
        self.radius_error_bool = False

        self.mapview_exist_bool = False

        self.array_moins_cher_points = []
        
        self.city_DropDown = DropDown()
        
               
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)
        
    #CALLING 
    #------------------------------------------------------------------        
        self.gui_interface()
        ''' 
        self.on_text() Call from uiStatic
        self.on_text_() Call from uiStatic
        self.intermediate() Call from uiStatic.submit button
        Tempo entre les deux
        self.next_intermediate() Call from self.intermediate()
        Tempo entre les deux
        self.next_update() Call from self.next_intermediate()
        Tempo entre les deux	     
        self.near_updateMapView() Call from self.next_update()
        Tempo entre les deux	          
        self.updateMapView() Call from self.near_updateMapView()
        
        1# self.updateMapView() premier d'une nouvelle méthode
        self.updateMapView() Call from self.near_updateMapView()
        self.list_low_price() Call from self.updateMapview()
        self.createMarkerPopup() Call from self.list_low_price()
        
        2# updateMapView() deuxième d'une nouvelle méthode
        Tempo entre les deux	
        self.end_of_update_mapview()
        self.changeViewOfMap()
       ''' 
        
    def gui_interface(self):
        self.locator = Nominatim(user_agent="low-fuel") 
        
    def __enter__(self):
        return self.name

    def on_text(self, instance, value):
        pass
    
    def on_text_(self, instance, value):
        if value != '' and len(value) == 5 and (str(int(value)) == value or '0' + str(int(value)) == value):
            nomi = pgeocode.Nominatim('fr')
            self.city = nomi.query_postal_code(value)
            self.city = self.city.place_name
            self.city = str(self.city).split(', ')
            if len(self.city) == 1:
                self.btn_city = self.btn0
                self.btn_city.text = self.city[0]
                self.btn_city.bind(
                    on_release=lambda city_DropDown: self.city_DropDown.select(self.btn_city.text))
                self.city_DropDown.add_widget(self.btn_city)
            else:
                for self.index in range(len(self.city)):
                    self.btn_city = self.uiStatic.btnN()
                    self.btn_city.text = f'{self.city[self.index]}'
                    self.btn_city.bind(
                        on_release=lambda btn_city: self.city_DropDown.select(btn_city.text))
                    self.city_DropDown.add_widget(self.btn_city)
            self.city_DropDown.open(self.city_button_DropDown)
        else:
            self.city_DropDown.dismiss()
            self.city_DropDown.clear_widgets()
            
        self.city_button_DropDown.bind(on_release=self.city_DropDown.open)
        self.city_DropDown.bind(on_select=lambda instance, x: setattr(self.city_button_DropDown, 'text', x))
    
    def intermediate(
        self,
        street_entry,
        post_code_entry,
        city_DropDown,
        radius_entry,
        button_DropDown,
        addresse_label_error,
        essence_label_error,
        radius_label_error
    ):
        if self.mapview_exist_bool:
            for child in self.floatLayout.children:
                child.clear_widgets()
            self.floatLayout.clear_widgets()   
            self.RootWidget.remove_widget(self.floatLayout)
            for child in self.mapview.children:
                child.clear_widgets()
            self.mapview_exist_bool = False
        self.download_data_label = self.loadingText
        self.loading_label = self.traitementText
        self.RootWidget.add_widget(self.download_data_label)
        Clock.schedule_once(lambda dt: self.next_intermediate(
            street_entry,
            post_code_entry,
            city_DropDown,
            radius_entry,
            button_DropDown,
            addresse_label_error,
            essence_label_error,
            radius_label_error
        ),
            0)

    def next_intermediate(
        self,
        street_entry,
        post_code_entry,
        city_entry,
        radius_entry,
        fuel_entry,
        addresse_label_error,
        essence_label_error,
        radius_label_error
    ):
        if self.address_error_bool:
            self.RootWidget.remove_widget(addresse_label_error)
            self.address_error_bool = False
        if self.essence_error_bool:
            self.RootWidget.remove_widget(essence_label_error)
            self.essence_error_bool = False
        if self.radius_error_bool:
            self.RootWidget.remove_widget(radius_label_error)
            self.radius_error_bool = False
        Clock.schedule_once(lambda dt: self.next_update(
            street_entry,
            post_code_entry,
            city_entry,
            radius_entry,
            fuel_entry,
            addresse_label_error,
            essence_label_error,
            radius_label_error
        ),
            0.5)        

    def next_update(
        self,
        street_entry,
        post_code_entry,
        city_entry,
        radius_entry,
        fuel_entry,
        addresse_label_error,
        essence_label_error,
        radius_label_error
    ):

        self.street_entry_post = street_entry
        self.post_code_entry_post = post_code_entry
        self.city_entry_post = city_entry
        self.radius_entry_post = radius_entry
        self.fuel_entry_post = fuel_entry
        self.addresse_label_error = addresse_label_error
        self.essence_label_error = essence_label_error
        self.radius_label_error = radius_label_error

        self.points = []

        self.address = f'{self.street_entry_post} {self.post_code_entry_post} {self.city_entry_post}'

        self.locator = Nominatim(user_agent="low-fuel")
        self.location = self.locator.geocode(self.address)

        if self.locator.geocode(self.address) is None or (self.street_entry_post == '' or self.post_code_entry_post == '' or self.city_entry_post == ''):
            self.RootWidget.remove_widget(self.download_data_label)
            self.RootWidget.add_widget(self.addresse_label_error)
            self.address_error_bool = True
            return

        if self.fuel_entry_post not in {'Gazole', 'SP98', 'SP95', 'GPLc', 'E10', 'E85'}:
            self.RootWidget.remove_widget(self.download_data_label)
            self.RootWidget.add_widget(self.essence_label_error)
            self.essence_error_bool = True
            return

        if float(self.radius_entry_post.replace('','0').replace('km','').replace(' km','')) <= 0:
            self.RootWidget.remove_widget(self.download_data_label)
            self.RootWidget.add_widget(self.radius_label_error)
            self.radius_error_bool = True
            return
                         
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
            if sellpoint.prices[0].fuel_type == self.button_DropDown_Fuel.text:
                self.prices_txt_ = f'[b]\nCarburant {sellpoint.prices[0].fuel_type}\nà {str(sellpoint.prices[0].value).replace(".", ",")} €/L[/b]'
                if sellpoint.prices[0].fuel_type == self.button_DropDown_Fuel.text:
                    price_list = {"prix":sellpoint.prices[0].value, "name":sellpoint.name, "address":f'{sellpoint.address.street}\n{sellpoint.address.post_code} {sellpoint.address.city}', "text":self.prices_txt_, "latitude":sellpoint.address.latitude, "longitude":sellpoint.address.longitude}
                    self.price_array.append(price_list)
      
        self.price_array = sorted(self.price_array, key=lambda d: d["prix"])
        
        if len(self.price_array) == 0:
            self.stationPoint = self.uiStatic.stationPoint0()
            self.floatLayout.add_widget(self.stationPoint)
        else :
            for index in range(min(len(self.price_array), 5)):
                y = .63 - (index * .14)

                text = f'[size=10][b]{self.price_array[index].get("name")}[/b]\n{self.price_array[index].get("address")}\n{self.price_array[index].get("text")}\n[/size]'

                if   index == 0: color=utils.get_color_from_hex('#00FF00')
                elif index == 1: color=utils.get_color_from_hex('#99FF00')
                elif index == 2: color=utils.get_color_from_hex('#FFFF00')
                elif index == 3: color=utils.get_color_from_hex('#FF9900')
                elif index == 4: color=utils.get_color_from_hex('#FF0000')

                self.stationPoint = self.uiStatic.stationPoints1()
                self.stationPoint.text=text
                self.stationPoint.pos_hint.update({'x': 0.803333333, 'y': y})
                self.stationPoint.background_color=color
                self.floatLayout.add_widget(self.stationPoint)
                for point in range(len(self.points)):
                    if self.points[point][0] == self.price_array[index].get("latitude") and self.points[point][1] == self.price_array[index].get("longitude"):
                        self.points[point][3] = color 
        
        self.RootWidget.add_widget(self.floatLayout)
        self.createMarkerPopup(self.points)


    def end_of_update_mapview(self):
        self.points
        self.mapview
        self.newLat = self.location[0]
        self.newLon = self.location[1]
        self.changeViewOfMap()
        

    def changeViewOfMap(self):
        self.mapview.center_on(self.newLat, self.newLon)

    def createMarkerPopup(self, points):
        self.points = points
        for point in self.points:
            self.mapMarkerPopup = MapMarkerPopup(
                lat=point[0],
                lon=point[1],
                popup_size=(600, 400),
                color=point[3]
            )

            self.bubble = Bubble()
            self.boxLayout = BoxLayout(
                orientation="horizontal",
                padding="5dp",
            )

            self.label = Label(text=point[2], markup=True, halign="center")

            self.asyncImage = AsyncImage(
                source="https://github.com/Bit-Scripts/Low-Fuel/raw/main/image/Fuel_gauge-250.jpg", mipmap=True)

            self.boxLayout.add_widget(self.asyncImage)
            self.boxLayout.add_widget(self.label)
            self.bubble.add_widget(self.boxLayout)
            self.mapMarkerPopup.add_widget(self.bubble)
            self.mapview.add_widget(self.mapMarkerPopup)
        self.mapview_exist_bool = True