
from my_kivy import metier
from my_kivy import my_widgets
from my_kivy.create_uix import kivyUi
from kivy_garden.mapview import MapView
from kivy import utils
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
import platform


class uiStatic:
    def __init__(self, root_widget, tmp_dir):
        self.executing = False   
        self.RootWidget = root_widget
        self.tmp_dir = tmp_dir
        #Init de certain Methodes avec export vers la logique
        #------------------------------------------------------------------
        self.city_button_DropDown = self.cityButtonChoice()
        self.btn0 = self.btn0()
        self.mapview = self.mapView()
        self.button_DropDown_Fuel = self.buttonDropDownFuel()
        self.traitementText = self.traitementText()
        self.loadingText = self.loadingText()
        self.uiStatic = self
        self.floatLayout = FloatLayout(size_hint=(1,1), pos_hint={'x': 0, 'y': 0})

        #Envoi des infos dans la logic
        self.kU = kivyUi(self.RootWidget, self.city_button_DropDown, self.btn0, self.mapview, self.button_DropDown_Fuel, self.traitementText, self.loadingText, self.uiStatic, self.floatLayout)

        #Appel des méthodes de ma class:
        #------------------------------------------------------------------
        self.addresseStreet()
        self.codePost()
        self.codePost2()
        self.cityChoice()
        self.actionRadius()
        self.errorAddresse()
        self.errorFuel()
        self.errorRadius()
        self.fuelChoice()
        self.open_Menu()
        self.submitForm()
        self.logoGif()
        self.assemblageWidget()  
    
        #MapView:
        #------------------------------------------------------------------
    def mapView(self):
        self.mapview = MapView(
            lat=metier.random_coordonees()[0],
            lon=metier.random_coordonees()[1],
            zoom=12, map_source="osm",
            size_hint=(1, 1),
            cache_dir=str(self.tmp_dir)
        )
        return self.mapview

        #Street Address:
        #------------------------------------------------------------------
    def addresseStreet(self):
        self.street_label = my_widgets.ColoredLabel(
            text="    Numéro et\nNom de la Rue",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.248, .098),
            pos_hint={'x': 0.0005, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        self.street_entry = TextInput( 
            halign='center', multiline='false',
            size_hint=(.249, .05), pos_hint={'x': 0, 'y': .85})
        self.street_entry.bind(text=self.kU.on_text)

        #Post Code Address:
        #------------------------------------------------------------------
    def codePost(self):
        self.post_code_label = my_widgets.ColoredLabel(
            text=" Code\nPostal",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.082333333333, .098),
            pos_hint={'x': .25, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        
    def codePost2(self):
        self.post_code_entry = my_widgets.MaxLengthInput(
            halign='center', multiline='false',
            size_hint=(.082333333333, .05),
            pos_hint={'x': .25, 'y': .85}
        )
        self.post_code_entry.bind(text=self.kU.on_text_)
        return self.post_code_entry


        #City Name:
        #------------------------------------------------------------------
    def cityChoice(self):
        self.city_label = my_widgets.ColoredLabel(
            text="Ville",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.16566667, .098),
            pos_hint={'x': .33333333, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
    def btn0(self):
        self.btn_city0 = my_widgets.SmoothButton(
            text='vide',
            size_hint_y=None,
            height=22,
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(.906, .906, .906, 1),
            border=(0, 0, 0, 1),
            border_color=(0, 0, 0, 1),
            border_width=1
        )
        return self.btn_city0

    def btnN(self):
        return my_widgets.SmoothButton(
            text='vide',
            size_hint_y=None,
            height=22,
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(.906, .906, .906, 1),
            border=(0, 0, 0, 1),
            border_color=(0, 0, 0, 1),
            border_width=1
        )
        
    def cityButtonChoice(self):    
        self.city_button_DropDown = my_widgets.SmoothButton(
            text="Entrer le CP",
            size_hint=(.165666667, .048),
            pos_hint={'x': .33333333, 'y': .851},
            color=(0, 0, 0, 1),
            background_normal='',
            background_color=(.906, .906, .906, 1),
            border_color=(0, 0, 0, 1),
            border_width=1
        )
        return self.city_button_DropDown
        
            #Action Radius:
        #------------------------------------------------------------------
    def actionRadius(self):
        self.radius_label = my_widgets.ColoredLabel(
            text="     Rayon\nd'action(km)",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.165666667, .098),
            pos_hint={'x': .5, 'y': .9},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        self.radius_entry = TextInput(
            halign='center', multiline='false',
            size_hint=(.16566667, .05), pos_hint={'x': .5, 'y': .85})
        self.radius_entry.bind(text=self.kU.on_text) 

        #Error:
        #------------------------------------------------------------------ 
        #address :
    def errorAddresse(self):
        self.addresse_label_error = my_widgets.ColoredLabel(
            text="Adresse Non trouvé",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.34509803921568627,
                                0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        return self.addresse_label_error         
        #fuel choose: 
    def errorFuel(self):
        self.essence_label_error = my_widgets.ColoredLabel(
            text="Type d'essence non correct",
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.34509803921568627,
                                0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        return self.essence_label_error
        #action radius:
    def errorRadius(self):
        self.radius_label_error = my_widgets.ColoredLabel(
            text="Le rayon doit strictement\n        supérieur à zéro",
            color=(0, 0, 0, 1),
            background_color=(0.34509803921568627,
                                0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        return self.radius_label_error
        #DropDown Fuels:
        #------------------------------------------------------------------ 
    def fuelChoice(self):
        self.fuel_DropDown = DropDown()
        #Gazole
        self.btn_Gazole = my_widgets.SmoothButton(
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
        #SP95:
        self.btn_SP95 = my_widgets.SmoothButton(
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
        self.btn_SP98 = my_widgets.SmoothButton(
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
        #E85
        self.btn_E85 = my_widgets.SmoothButton(
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
        #E10
        self.btn_E10 = my_widgets.SmoothButton(
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
        #GPLc
        self.btn_GPLc = my_widgets.SmoothButton(
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
        
    def buttonDropDownFuel(self):
        self.button_DropDown_Fuel = my_widgets.SmoothButton(
            text="Carburant utilisé",
            size_hint=(.16666667, .1425),
            pos_hint={'x': .6666667, 'y': .855},
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2
        )
        return self.button_DropDown_Fuel
    def open_Menu(self):
        #DropDown
        self.button_DropDown_Fuel.bind(on_release=self.fuel_DropDown.open)
        self.fuel_DropDown.bind(on_select=lambda instance, x: setattr(self.button_DropDown_Fuel, 'text', x))
        
        #Submit Form
        #------------------------------------------------------------------         
    def traitementText(self):
        self.download_data_label = my_widgets.ColoredLabel(
            text="Récupération des données",
            color=(0, 0, 0, 1),
            background_color=(0.34509803921568627,
                                0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1)
        )
        return self.download_data_label

    def loadingText(self):
        self.loading_label = my_widgets.ColoredLabel(
            text="Traitement des données",
            color=(0, 0, 0, 1),
            background_color=(0.34509803921568627,
                                0.34509803921568627, 0.34509803921568627, .65),
            size_hint=(.4, .2),
            pos_hint={'x': .3, 'y': .4},
            border_width=1,
            border_color=(0, 0, 0, 1))
        return self.loading_label
        
        #Submit Form
        #------------------------------------------------------------------ 
    def submitForm(self):
        self.submitButton = my_widgets.SmoothButton(
            text="Mettre à jour",
            size_hint=(.16416667, .1425),
            pos_hint={'x': .833333333, 'y': .855},
            color=utils.get_color_from_hex('#000000'),
            background_normal='',
            background_color=(0.45098, 0.64706, 0.45098, 1),
            border_color=(0, 0, 0, 1),
            border_width=2)
        self.submitButton.bind(on_press=lambda instance: self.kU.intermediate(self.street_entry.text, self.post_code_entry.text,
                        self.city_button_DropDown.text, self.radius_entry.text, self.button_DropDown_Fuel.text, self.addresse_label_error, self.essence_label_error, self.radius_label_error))
        #Logo Gif
        #------------------------------------------------------------------ 
    def logoGif(self):
        gif = 'image/Logo_Bit-Scripts.gif'
        if platform.system() == 'Windows':
            gif = 'image\\Logo_Bit-Scripts.gif'
        r_p = metier.resource_path(gif)
        self.bit_scripts_logo = Image(
            source=r_p,
            size_hint=(.1, .1),
            pos_hint={'x': .01, 'y': .01},
            anim_delay=.5,
            anim_loop=0
        )
        
        #Attache All Elements to Root 
        #------------------------------------------------------------------ 
    def assemblageWidget(self):
        self.RootWidget.add_widget(self.mapview)
        self.RootWidget.add_widget(self.submitButton)
        self.fuel_DropDown.add_widget(self.btn_Gazole)
        self.fuel_DropDown.add_widget(self.btn_SP98)
        self.fuel_DropDown.add_widget(self.btn_SP95)
        self.fuel_DropDown.add_widget(self.btn_E85)
        self.fuel_DropDown.add_widget(self.btn_E10)
        self.fuel_DropDown.add_widget(self.btn_GPLc)
        self.RootWidget.add_widget(self.button_DropDown_Fuel)
        self.RootWidget.add_widget(self.street_label)
        self.RootWidget.add_widget(self.street_entry)
        self.RootWidget.add_widget(self.post_code_label)
        self.RootWidget.add_widget(self.post_code_entry)
        self.RootWidget.add_widget(self.city_label)
        self.RootWidget.add_widget(self.city_button_DropDown)
        self.RootWidget.add_widget(self.radius_label)
        self.RootWidget.add_widget(self.radius_entry)
        self.RootWidget.add_widget(self.bit_scripts_logo)

        #MapObject
        #------------------------------------------------------------------ 
    def stationPoint0(self):
        return my_widgets.ColoredLabel(
            text='Pas de Station',
            markup=True,
            halign='center',
            valign='center',
            color=utils.get_color_from_hex('#000000'),
            background_color=(0.45098, 0.64706, 0.45098, 1),
            size_hint=(.18536667, .1435),
            pos_hint={'x': .803333333, 'y': .63},
            border_width=1.5,
            border_color=(0, 0, 0, 1)
        )
    
    
    def stationPoints1(self):
        return my_widgets.ColoredLabel(
                text=' ',
                markup=True,
                halign='center',
                valign='center',
                color=utils.get_color_from_hex('#000000'),
                background_color=utils.get_color_from_hex('#FFFFFF'),
                size_hint=(.18536667, .1435),
                pos_hint={'x': .803333333, 'y': .63},
                border_width=1.5,
                border_color=(0, 0, 0, 1)
            )