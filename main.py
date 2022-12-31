import os
import sys
import pgeocode
import pathlib

#os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "$TMPDIR"

from kivy.resources import resource_add_path, resource_find
from kivy.uix.floatlayout import FloatLayout

from domain.data import SellPoint
from domain.logic import address_to_coord
from domain.user import AddressUser
from parsedata.parse_json import ParseJson

from typing import List

from geopy import Nominatim

import random

import platform

from kivy.app import App

from my_kivy.create_uix import kivyUi

class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
  
        kivyUi(self)

class Low_Fuel(App):
    def build(self):
        self.title = 'Low-Fuel'
        if platform.system() == 'Darwin':
            if hasattr(sys, '_MEIPASS'):
                self.icon = '../Resources/petrol_pump.icns'
            else:
                self.icon = 'image/petrol_pump.icns'
        if platform.system() == 'Linux':
            self.icon = 'image/petrol_pump.png'
        if platform.system() == 'Windows':
            self.icon = 'image/petrol_pump.ico'
        self.root = RootWidget()

if __name__ == '__main__':
    Low_Fuel().run()
