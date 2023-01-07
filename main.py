import os

os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "$TMPDIR"

from kivy.uix.floatlayout import FloatLayout

from kivy.app import App

from kivy.config import Config
Config.set('kivy', 'window_icon', os.path.join("omission", "resources", "icons", "petrol_pump.png"))

from my_kivy.ui_object import uiStatic
from my_kivy.metier import tmp_dir

class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
        self.tmp_dir = tmp_dir()
        uiStatic(self, self.tmp_dir)
        

class Low_Fuel(App):
    def build(self):
        self.title = 'Low-Fuel'
        self.icon = os.path.join("omission", "resources", "icons", "petrol_pump.png")
        self.root = RootWidget()


if __name__ == '__main__':
    Low_Fuel().run()
