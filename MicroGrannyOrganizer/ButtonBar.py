from MgButton import MgButton
from CanvasButton import CanvasButton
from CanvasButton import SwitchModes

class ButtonBar(object):
    """Holds several MgButtons and aligns them in a row. also displays the settings-parameter spread on the different LEDs"""
    buttons = [] ## 6 MgButtons
    x=0 ##x-position
    y=0 ##y-position
    root = 0
    canvas = 0
    spacing = 114

    current_btn = 0

    new_slot_callback = 0 ## is called when a new slot is selected

    def __init__(self, *args, **kwargs):
        self.canvas=kwargs.pop('canvas')
        self.root=kwargs.pop('root')
        self.x=kwargs.pop('x')
        self.y=kwargs.pop('y')
        self.init_buttons()
        return super().__init__(*args, **kwargs)

    def init_buttons(self):
        self.buttons = []
        for i in range(6):
            btn = CanvasButton(canvas=self.canvas, root=self.root, x=self.x+self.spacing*i, y=self.y, label="Button"+str(i), switch_mode=SwitchModes.switch_until_released)
            btn.value_change_callback=self.btn_val_change
            self.buttons.append(btn)
        self.buttons[0].set_on()

    def btn_val_change(self, value, label):
        print(label+" clicked. Now: "+str(value))