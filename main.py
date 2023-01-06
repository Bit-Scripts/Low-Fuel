import os

#os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["PYTHONPYCACHEPREFIX"] = "$TMPDIR"

from kivy.uix.floatlayout import FloatLayout

from kivy.app import App

from kivy.config import Config
Config.set('kivy', 'window_icon', os.path.join("omission", "resources", "icons", "petrol_pump.png"))

from my_kivy.create_uix import kivyUi

class RootWidget(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(RootWidget, self).__init__(**kwargs)
  
        kivyUi(self)

class Low_Fuel(App):
    def build(self):
        self.title = 'Low-Fuel'
        self.icon = os.path.join("omission", "resources", "icons", "petrol_pump.png")
        self.root = RootWidget()


if __name__ == '__main__':
    Low_Fuel().run()
