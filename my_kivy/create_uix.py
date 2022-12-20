import os
import sys

# setting path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from typing import List

from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy.uix.widget import Widget
from kivy.uix.bubble import Bubble
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label

class kivyUi():
    def __init__(self, points: List[tuple], root: Widget, mapview: MapView, newLat: float = None, newLon: float= None):
        self.points = points
        self.root = root
        self.mapview = mapview
        self.newLat = newLat
        self.newLon = newLon
        self.createMarkerPopup(self.points)


    def changeViewOfMap(self):
        self.mapview.center_on(self.newLat, self.newLon)


    def createMarkerPopup(self, points):
        self.points = points
        for point in self.points:
            mapMarkerPopup = MapMarkerPopup(lat=point[0], lon=point[1], popup_size=(600, 400), color=point[3])     
            bubble = Bubble()
            boxLayout = BoxLayout(orientation="horizontal", padding="5dp")
            label = Label(text=point[2], markup=True, halign="center")
            asyncImage = AsyncImage(source="https://github.com/Bit-Scripts/Low-Fuel/raw/main/image/Fuel_gauge-250.jpg", mipmap=True)
            
            boxLayout.add_widget(asyncImage)
            boxLayout.add_widget(label)
            bubble.add_widget(boxLayout)
            mapMarkerPopup.add_widget(bubble)
            self.mapview.add_widget(mapMarkerPopup)

    def on_text(self, instance, value):
        pass
