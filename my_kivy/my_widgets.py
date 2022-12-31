from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle, Line
from kivy.properties import ListProperty, NumericProperty

class ColoredBackgoundMixin:
    _color = None
    _rect = None
    background_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    border_color = ListProperty([0.0,0.0,0.0,1.0])
    border_width = NumericProperty(1.0)

    def __init__(self, *, background_color, border_color, border_width, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.background_color = background_color
            self._color = Color(*background_color)
            self._rect = Rectangle(size=self.size, pos=self.pos)
            self.border_color = border_color
            self._color_border = Color(*border_color)
            self.border_width = border_width
            self._width = self.border_width
            self._rectangle = (self.size[0], self.size[1], self.pos[0], self.pos[1])
            self._line = Line(rectangle=self._rectangle, width=self._width)
            self.bind(size=self._update_rect, pos=self._update_rect, background_color=self._update_rect, border_width=self._update_rect, border_color=self._update_rect)

    def _update_rect(self, instance, value):
        self._color.rgba = instance.background_color
        self._rect.pos = instance.pos
        self._rect.size = instance.size
        self._color_border.rgba = instance.border_color
        self._line.width = instance.border_width
        self._rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1])
        self._line.rectangle = self._rectangle


class ColoredLabel(ColoredBackgoundMixin, Label):
    pass



class SmoothButtonMixin:
    _color = None
    _rectangle = None
    _line = None
    border_color = ListProperty([0.0,0.0,0.0,1.0])
    border_width = NumericProperty(1.0)

    def __init__(self, *, border_color, border_width, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.border_color = border_color
            self._color = Color(*border_color)
            self.border_width = border_width
            self._width = self.border_width
            self._rectangle = (self.size[0], self.size[1], self.pos[0], self.pos[1])
            self._line = Line(rectangle=self._rectangle, width=self._width)
            self.bind(size=self._update_border, pos=self._update_border, border_width=self._update_border, border_color=self._update_border)     

    def _update_border(self, instance, value):
        self._color.rgba = instance.border_color
        self._line.width = instance.border_width
        self._rectangle = (instance.pos[0], instance.pos[1], instance.size[0], instance.size[1])
        self._line.rectangle = self._rectangle

class SmoothButton(SmoothButtonMixin, Button):
    pass



class GifImage(Image):
    frame_counter = 0
    frame_number = 9 # my example GIF had 36 frames

    def on_texture(self, instance, value):     
        if self.frame_counter == self.frame_number + 1:
            self.frame_counter = 0
        self.frame_counter += 1