<LowFuelView>:
    result_label:result_label
    answer_input:answer_input
    BoxLayout:
        orientation: "vertical"
        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                source: "Fuel_gauge_indev.jpg"
        BoxLayout:
            orientation: "vertical"
            padding: 100, 30, 100, 30
        Label:
            id: result_label
            text: "Find the number"
            font_size: 60
        TextInput:
            id: answer_input
            padding: 20, 20, 20, 20
            size_hint: 1, 0.5
            font_size: 42
            input_type: "number"
            multiline: False
        Button:
            text: "Validate"
            size_hint: 1, 0.5
            bold: True
            background_color: "#0065EF"
            on_press: root.check_number()
