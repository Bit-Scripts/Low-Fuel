from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import ListProperty

class ColoredBackgoundMixin:
    _color = None
    _rect = None
    background_color = ListProperty([0.0, 0.0, 0.0, 1.0])

    def __init__(self, *, background_color, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.background_color = background_color
            self._color = Color(*background_color)
            self._rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect, background_color=self._update_rect)

    def _update_rect(self, instance, value):
        self._color.rgba = instance.background_color
        self._rect.pos = instance.pos
        self._rect.size = instance.size


class ColoredLabel(ColoredBackgoundMixin, Label):
    pass